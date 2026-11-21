# Technical Validation

## Schema validation

[TBD: validation results]

## Consistency with the source tool outputs

We checked that the converters carry the identifications and intensities of the tool outputs
into the QPX views unchanged. For each of the three output formats of the corpus workflows
(DIA-NN reports, OpenMS consensusXML files and quantms MSstats input tables) and for MaxQuant
and FragPipe, we converted a complete output of a public dataset and compared the QPX views with
the source tables, parsed independently of the `qpx` package. Rows were paired by peptidoform,
charge, run and label, and protein groups by their member accessions and run; intensities
counted as equal when their relative difference was below 10^-6^
(`scripts/validation/converter_agreement.py`; the results of every comparison are in
`data/validation/converter_agreement.csv`). In the DIA-NN report that the submitters of
PXD041421 deposited for its 48 diaPASEF runs [@ds_PXD041421], all 5,059,793 precursor rows, with
135,439 precursors and 114,824 peptidoforms, and the 418,030 quantities of 10,285 protein groups
matched; the five precursor quantities of zero, with which DIA-NN marks a precursor it did not
quantify, are null in QPX. In the OpenMS consensusXML of the PXD007683 benchmark of
Supplementary Fig. S1 [@ds_PXD007683], all 542,403 PSMs, the 573,203 features with their
intensities and the 9,424 protein groups matched; the consensusXML holds no protein-group
abundance, so the protein-group intensities that the converter derives from the features have no
source to compare with. In the quantms MSstats input tables, the 518,248 features of the same
benchmark and the 1,391,060 channel intensities of the TMT dataset PXD014145 [@ds_PXD014145],
including its 269,710 zeros, matched; the converter combines the channels of a precursor into
one feature row, giving 126,460 rows for PXD014145. In the MaxQuant output deposited with
PXD014145, the 95,187 PSMs and 107,260 features left after removing reverse and contaminant hits
matched, as did the 582,972 non-zero reporter intensities of these features in the eight TMT
channels the search was set up with. The search names no experiments, so its protein groups hold
the totals of one experiment, the twelve fractions of the plex, which the converter assigns to
these twelve runs; after removing reverse, contaminant and only-identified-by-site groups, the
51,344 intensities of 6,693 protein groups matched. In the FragPipe output deposited with
PXD041421, the 67,775 PSMs of one complete run, the 2,231,022 features of the 48 runs, with 96,288 precursors and 78,461 peptidoforms, and
the 253,323 intensities of 7,290 protein groups matched; for the 5,141 of the 101,738 ions whose
`Assigned Modifications` leave out a modification given in `Modified Sequence`, the converter
takes it from `Modified Sequence`. Where intensities matched, the largest relative difference
between paired values was 6 × 10^-8^, the precision of the 32-bit floating-point values QPX
stores. The conversions used QPX development commit f8fde490. [TBD: rerun with the QPX 1.4.0 release]

## Storage and query performance

On the label-free analysis of Supplementary Fig. S1 (11 runs, 542,403 PSMs), DuckDB answered
each of four PSM queries on the `psm` view in 15 to 46 ms, with peak resident memory rising by at
most 109 MiB, whereas pandas took 2.4 to 2.9 s and 1.5 GiB to answer them from the PSM section of
the mzTab, with the same answers. The three feature queries took 15 to 22 ms on the `feature`
view and 0.27 to 0.31 s on the MSstats input table, with pandas or DuckDB. Relayout reduced the
`psm` view from 22.6 to 12.1 MB and the `feature` view from 19.8 to 12.1 MB; on this small
dataset, read from a local disk, it changed the query times by less than 3 ms. The benchmark used
QPX development commit 2dadc0e1. [TBD: rerun with the QPX 1.4.0 release]

The layout matters when files are read over a network, where every row group read costs requests
and transfer. We served the feature and pg views of the DIA-NN analysis of PXD041421 (5,059,793
features in 41 row groups, 547 MB) over a simulated link with 50 ms latency and 100 Mbit/s
bandwidth and queried them with DuckDB (Supplementary Fig. S3). Reading the 1,516 features of one
protein transferred 47.7 MB in 199 requests and took 4.3 s as written; after relayout, which
stores them in one row group, it transferred 1.7 MB in 7 requests and took 0.7 s. Queries that
read whole columns, such as the ten proteins with the largest summed intensity, transferred 43 to
45 MB and took about 4 s with either layout, and a lookup by a column that the sort order does not
follow became slower: as written, the rows of one run lie in 9 of the 41 row groups and its
intensities took 1.3 s, against 4.0 s after relayout. Downloading the whole feature view took
45 s, or 31 s after relayout. On a file of the quantms portal, the simulated link read the same
bytes as DuckDB did over the internet and, set to the latency and bandwidth measured for that
connection, took 0.6 to 0.7 times as long, so the simulated times underestimate those of a real
connection. The conversion used QPX development commit f8fde490 and relayout commit 0f39b844.
[TBD: rerun with the QPX 1.4.0 release]

## Comparison with the originally reported results


Seven datasets of the corpus were reanalysed or released as resources in earlier work that
reports identification and quantification results: PXD000672, PXD003497 and PXD003539 in the DIA
reanalysis of Walzer et al. [@Walzer_2022], PXD002395 and PXD004452 in the cancer cell line
reanalysis of Jarnuczak et al. [@Jarnuczak_2021], PXD042233 in the HeLa resource of Webel et al.
[@Webel_2024] and PXD028735 in the label-free quantification benchmark of Van Puyvelde et al. [@Van_Puyvelde_2022].
For the five of them processed with DIA-NN or OpenMS we compare the protein groups and peptides
identified at 1% FDR with the numbers reported there and in the original publications and,
following Walzer et al., the coefficient of variation and the correlation of protein-group
intensities between repeated measurements of a sample. PXD004452 and PXD028735 belong to the
identification-only subset, which has no protein groups or quantities; for them we compare the
identified peptides. [TBD: comparison results]

## Identification quality

For datasets whose PSMs carry q-values, `scripts/validation/psm_metrics.py` counts the target
PSMs accepted at q-value thresholds up to the threshold at which the workflow exported its
results, and, for PSMs with peak arrays, the fraction of the MS2 ion current in peaks annotated
as b or y ions, as Wen and Noble did for their benchmark [@Wen_2024]. Their acceptance rate,
the fraction of MS2 spectra accepted at 1% FDR, cannot be computed, because the views do not
record the number of MS2 spectra of a run. [TBD: results]

## Quality metrics across the corpus

Identification and quantification statistics were computed for each dataset from its QPX views
(Fig. 3): the distinct target peptidoforms per run, the protein groups quantified per
quantification unit, the completeness of the protein group by unit matrix and the median
precursor mass error. Because the pipelines export results at different thresholds, rows with
a q-value above 0.01 were dropped where the views carry q-values. [TBD: description of the distributions] `scripts/validation/quant_metrics.py` also bins the protein groups of each
dataset by their median log2 intensity and reports the fraction of missing values per bin, as
Webel et al. did for the HeLa runs [@Webel_2024], to show whether missing values concentrate at
low abundance. [TBD: figure]

## Comparison with earlier versions

For datasets that the quantms portal also holds in an older specification,
`scripts/validation/compare_versions.py` compares the deposited version with the older one: the
target records (for protein groups, one quantity per protein group, run or unit and label, so
that the two layouts are comparable), the overlap of peptide sequences and protein groups, and the agreement of
feature and protein-group intensities, matched on sequence, charge, run and label because the
peptidoform strings and row identifiers changed. [TBD: results]
