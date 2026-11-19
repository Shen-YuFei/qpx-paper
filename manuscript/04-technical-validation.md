# Technical Validation

## Schema validation

[TBD: validation results]

## Consistency with the source tool outputs

We checked that the converters carry the identifications and intensities of the tool outputs
into the QPX views unchanged. For each of the three tools behind the corpus and for MaxQuant and
FragPipe, we converted a complete output of a public dataset and compared the QPX views with the
source tables, parsed independently of the `qpx` package. Rows were paired by peptidoform,
charge, run and label, and protein groups by their member accessions and run; intensities
counted as equal when their relative difference was below 10^-6^
(`scripts/validation/converter_agreement.py`; the results of every comparison are in
`data/validation/converter_agreement.csv`). In the DIA-NN report of the 48 diaPASEF runs of
PXD041421 [@ds_PXD041421], all 5,059,793 precursor rows, with 135,439 precursors and 114,824
peptidoforms, and the 418,030 quantities of 10,285 protein groups matched; the five precursor
quantities of zero, with which DIA-NN marks a precursor it did not quantify, are null in QPX. In
the OpenMS consensusXML of the PXD007683 benchmark of Supplementary Fig. S1 [@ds_PXD007683], all
542,403 PSMs, the 573,203 features with their intensities and the 9,424 protein groups matched;
the consensusXML holds no protein-group abundance, so the protein-group intensities that the
converter derives from the features have no source to compare with. In the quantms MSstats input
tables, the 518,248 features of the same benchmark and the 1,391,060 channel intensities of the
TMT dataset PXD014145 [@ds_PXD014145], including its 269,710 zeros, matched; the converter
combines the channels of a precursor into one feature row, giving 126,460 rows for PXD014145. In
the MaxQuant output deposited with PXD014145, the 95,187 PSMs and 107,260 features left after
removing reverse and contaminant hits matched; the protein groups of this output sum the twelve
fractions of the plex into one unnamed experiment, cannot be assigned to runs, and are rejected
by the converter. [TBD: MaxQuant reporter intensities] In the FragPipe output deposited with
PXD041421, the 67,775 PSMs of one complete run and the 253,323 intensities of 7,290 protein
groups matched. [TBD: FragPipe feature identities] Where intensities matched, the largest
relative difference between paired values was 6 × 10^-8^, the precision of the 32-bit
floating-point values QPX stores. The conversions used QPX development commit 2dadc0e1. [TBD:
rerun with the QPX 1.4.0 release]

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
