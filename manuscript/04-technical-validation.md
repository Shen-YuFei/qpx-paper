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

[TODO: for selected datasets, compare identification numbers and quantities from the
reprocessing with those reported in the original publications.]

## Quality metrics across the corpus

[TODO: distribution of pmultiqc metrics across datasets (Fig. 3), once reports exist for the
deposited datasets.]
