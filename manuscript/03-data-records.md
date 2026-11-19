# Data Records

[TBD: repository, DOI and folder layout of the deposited record] The corpus is
currently served at https://browse.quantms.org/quantms/datasets/, with one folder per dataset.
Each dataset folder holds one or more subfolders named by a hash of their content, so a
reprocessed version of a dataset appears as a new subfolder next to the earlier ones. A QPX
subfolder contains the views of that version, a `provenance.json` file describing how and when
the version was produced and, for 23 datasets, a MuData export (`.h5mu`) of the quantification
results. The SDRF and the earlier quantms outputs (mzTab [@Griss_2014] and MSstats input tables
[@Kohler_2023]) are kept in the same subfolder or in another subfolder of the dataset. The folder
of PXD048538, for example, holds two versions of the dataset:

```text
PXD048538/
|-- 41b03dd48c8b/
`-- e60b9e9aa4c8/
    |-- PXD048538.dataset.parquet
    |-- PXD048538.feature.parquet
    |-- PXD048538.ontology.parquet
    |-- PXD048538.pg.parquet
    |-- PXD048538.provenance.parquet
    |-- PXD048538.run.parquet
    |-- PXD048538.sample.parquet
    |-- PXD048538.h5mu
    |-- PXD048538.sdrf.tsv
    |-- PXD048538_msstats_in.csv.gz
    `-- provenance.json
```

Table 2 explains the folder and file names. [TBD: version of each dataset deposited]

Table 2: Folder and file names in the corpus.

| Element | Example | Meaning |
|-----------------|---------------|------------------|
| Dataset folder | `PXD048538/` | Repository accession of the dataset, or a project name for datasets without one |
| Version folder | `e60b9e9aa4c8/` | Hash of the content of one processed version of the dataset |
| `{PREFIX}` | `PXD048538` | Usually the accession; a suffix marks a view of a subset processed separately (`PXD004452-GluC`) or a part of a view split into several files (`IPX0002031000-P2`) |
| `{PREFIX}.{view}.parquet` | `PXD048538.pg.parquet` | One view (Table 1) |
| `{PREFIX}.h5mu` | `PXD048538.h5mu` | MuData export of the quantification results |
| `{PREFIX}.sdrf.tsv` | `PXD048538.sdrf.tsv` | SDRF-Proteomics annotation of the samples and runs |
| `provenance.json` | | How and when the version was produced |

Table 3 summarises the corpus [TBD: numbers]. In total it holds 23,204
samples, 51,023 MS runs, 568 million PSM records, 435 million peptide feature records and 47
million protein-group quantity records, in 1.54 TB of files. Within each dataset, the
protein-group records correspond to 398,420 distinct protein groups. The 57
identification-only datasets account for most of the PSM records (499 million) and of the
volume (1.44 TB). The 46 quantitative datasets account for nearly all feature and
protein-group records, and their files total 96 GB.

Table 3: Summary of the QPX corpus by processing workflow. ID only: identification-only
datasets from the `quantms-msnet` recipe; DIA-NN: DIA datasets processed with DIA-NN;
OpenMS: label-free and TMT DDA datasets processed with the OpenMS-based quantms workflows.
PSMs, Features and PGs (protein-group records) in millions; GB, total file size.
[TBD: numbers]

| Subset | Datasets | Samples | Runs | PSMs | Features | PGs | GB |
|---|--:|--:|--:|--:|--:|--:|--:|
| ID only | 57 | 18,527 | 38,454 | 499.3 | – | – | 1,441 |
| DIA-NN | 27 | 3,024 | 8,422 | 4.8 | 398.0 | 35.4 | 84 |
| OpenMS | 19 | 1,653 | 4,147 | 63.8 | 37.2 | 11.8 | 12 |
| Total | 103 | 23,204 | 51,023 | 568.0 | 435.3 | 47.2 | 1,538 |

Each data view has one row per entity: one PSM in `psm`; one peptide feature per run in
`feature`, with the intensities of its label channels nested in the row; and, in `pg`, one
protein group per quantification unit (a run or a group of fractionated runs) and label. Table
1 lists the views and their key columns. The views join through shared columns: `run_file_name`
links `psm`, `feature` and `mz` to the run view, whose sample entries resolve a run and label
channel to a `sample_accession`; `pg.grouped_runs` lists the runs of a quantification unit;
`psm.feature_id`, where present, points to the feature of a PSM; `psm` and `feature` share the
`peptidoform` with `pepmap`; and a feature links to the pg row with the same set of
`pg_accessions` whose `grouped_runs` contain the feature's run and whose label matches. Every
`psm`, `feature` and `pg` row carries an `is_decoy` flag, and the q-value columns, null where
the source does not report them, let users apply their own FDR threshold [TBD: decoy records, q-value levels and primary quantities of each subset]. The metadata views are small (one row per sample, run
or dataset) and can be read in full; the data views are split into row groups with per-column
statistics, so that readers can skip the parts a query does not touch (Supplementary Fig. 1).

[TBD: views in each subset and whether the files were rewritten with relayout]
Supplementary Fig. 2 shows which views each dataset holds.
