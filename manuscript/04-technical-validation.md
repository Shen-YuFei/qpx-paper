# Technical Validation

## Schema validation

[TODO: run `qpxc validate` on every deposited dataset with the cited QPX release and report
the result. In the 29 October 2026 snapshot, all 1,198 Parquet files in the 181 QPX folders
(719 in the 103 latest versions) could be opened and their footers read, but 78 of the 103 latest versions record `qpx_version` 1.0.1 or 1.0.2
(the package version written by the qpx 1.0.x releases, read as specification 1.0) and are not
expected to pass the current schemas; the 25 written with 1.1 have not been checked. The
deposited files are to be converted again with QPX 1.4.0, or migrated where the tool outputs
are no longer available.]

## Consistency with the source tool outputs

[TODO: for a set of datasets per converter (MaxQuant, FragPipe, DIA-NN, OpenMS), compare the
number of PSMs, precursors, peptides and protein groups and the intensities in the QPX views
with the original tool outputs, and report the agreement.]

## Comparison with the originally reported results

Seven datasets of the corpus were reanalysed or released as resources in earlier work that
reports identification and quantification results: PXD000672, PXD003497 and PXD003539 in the DIA
reanalysis of Walzer et al. [@Walzer_2022], PXD002395 and PXD004452 in the cancer cell line
reanalysis of Jarnuczak et al. [@Jarnuczak_2021], PXD042233 in the HeLa resource of Webel et al.
[@Webel_2024] and PXD028735 in the LFQ benchmark of Van Puyvelde et al. [@Van_Puyvelde_2022].
For these datasets we compare the protein groups and peptides identified at 1% FDR with the
numbers reported there and in the original publications and, following Walzer et al., the
coefficient of variation and the correlation of protein-group intensities between repeated
measurements of a sample. [TODO: collect the reported numbers with their sources and report the
comparison after regeneration; `scripts/validation/quant_metrics.py` computes the replicate
metrics.]

## Identification quality

For datasets whose PSMs carry q-values, `scripts/validation/psm_metrics.py` counts the target
PSMs accepted at q-value thresholds up to the threshold at which the workflow exported its
results, and, for PSMs with peak arrays, the fraction of the MS2 ion current in peaks annotated
as b or y ions, as Wen and Noble did for their benchmark [@Wen_2024]. Their acceptance rate,
the fraction of MS2 spectra accepted at 1% FDR, cannot be computed, because the views do not
record the number of MS2 spectra of a run. [TODO: report after regeneration. In the trial
conversions, the identification-only PSMs of PXD028735 carry peak arrays with annotated b and y
ions (a median of 24% of the ion current over 20,000 PSMs) but no q-values or decoys, and the
PSMs of PXD014145 and PXD036643 carry q-values up to 0.05 and 0.01.]

## Quality metrics across the corpus

Identification and quantification statistics were computed for each dataset from its QPX views
(Fig. 3): the distinct target peptidoforms per run, the protein groups quantified per
quantification unit, the completeness of the protein group by unit matrix and the median
precursor mass error. Because the pipelines export results at different thresholds, rows with
a q-value above 0.01 were dropped where the views carry q-values. [TODO: describe the distributions once the
corpus is regenerated.] `scripts/validation/quant_metrics.py` also bins the protein groups of each
dataset by their median log2 intensity and reports the fraction of missing values per bin, as
Webel et al. did for the HeLa runs [@Webel_2024], to show whether missing values concentrate at
low abundance. [TODO: figure after regeneration. In the trial conversion of the TMT dataset
PXD014145, protein groups are quantified for each of the 12 fractions of the plex rather than
once per plex, which inflates the missing values and makes fractions look like repeated
measurements; check the converter.]

## Comparison with earlier versions

For datasets that the quantms portal also holds in an older specification,
`scripts/validation/compare_versions.py` compares the deposited version with the older one: the
target records, the overlap of peptide sequences and protein groups, and the agreement of
feature and protein-group intensities, matched on sequence, charge, run and label because the
peptidoform strings and row identifiers changed. [TODO: run on the deposited record. On the two
trial datasets migrated from qpx 1.0.x files, PXD014145 and PXD028735, the sets agree exactly and
the intensities are identical, as expected from a migration.]
