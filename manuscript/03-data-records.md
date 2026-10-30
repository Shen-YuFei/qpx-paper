# Data Records

[TODO: repository and DOI of the deposited record, e.g. PRIDE or Zenodo, cited as a data
citation.] The corpus is currently served at https://browse.quantms.org/quantms/datasets/,
with one folder per dataset accession. Each dataset folder holds one or more subfolders
named by a hash of their content, so a reprocessed version of a dataset appears as a new
subfolder next to the earlier ones. A QPX subfolder contains the views of that
version, named `{accession}.{view}.parquet`, a `provenance.json` file describing how and when
the version was produced and, for 23 datasets, a MuData export (`.h5mu`) of the
quantification results. The SDRF and the earlier quantms outputs (mzTab and MSstats input
tables) are kept in separate subfolders of the same dataset. [TODO: decide which version of
each dataset is deposited; 19 datasets currently have more than one QPX version.]

Table 1 summarises the corpus [TODO: provisional numbers from the 29 October 2026 snapshot,
latest QPX version of each dataset; update after regeneration]. In total it holds 23,204
samples, 51,023 MS runs, 568 million PSM records, 435 million peptide feature records and 47
million protein-group quantity records, in 1.54 TB of files. Within each dataset, the
protein-group records correspond to 398,420 distinct protein groups. The 57
identification-only datasets account for most of the PSM records (499 million) and of the
volume (1.44 TB). The 46 quantitative datasets account for nearly all feature and
protein-group records, and their files total 96 GB.

Table 1: Summary of the QPX corpus by processing workflow. ID only: identification-only
datasets from the `quantms-msnet` recipe; DIA-NN: DIA datasets processed with DIA-NN;
OpenMS: label-free and TMT DDA datasets processed with the OpenMS-based quantms workflows.
PSMs, Features and PGs (protein-group records) in millions; GB, total file size.
Provisional: latest QPX version of each dataset on browse.quantms.org on 29 October 2026.

| Subset | Datasets | Samples | Runs | PSMs | Features | PGs | GB |
|---|--:|--:|--:|--:|--:|--:|--:|
| ID only | 57 | 18,527 | 38,454 | 499.3 | – | – | 1,441 |
| DIA-NN | 27 | 3,024 | 8,422 | 4.8 | 398.0 | 35.4 | 84 |
| OpenMS | 19 | 1,653 | 4,147 | 63.8 | 37.2 | 11.8 | 12 |
| Total | 103 | 23,204 | 51,023 | 568.0 | 435.3 | 47.2 | 1,538 |

Each data view has one row per entity: one PSM in `psm`; one peptide feature per run in
`feature`, with the intensities of its label channels nested in the row; and, in `pg`, one
protein group per quantification unit (a run or a group of fractionated runs) and label.
Table 2 lists the views and their key columns. The metadata views are small (one row per
sample, run or dataset) and can be read in full; the data views are split into row groups
with per-column statistics, so that readers can skip the parts a query does not touch.
