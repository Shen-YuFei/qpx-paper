# Technical Validation

## Schema validation

[TBD: validation results]

## Consistency with the source tool outputs

[TBD: comparison results]

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
