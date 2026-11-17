# Usage Notes

## Accessing the files

QPX files are plain Parquet files and can be read by any Parquet reader, including DuckDB,
pandas and PyArrow, Polars, Apache Spark and the R arrow package. [TODO: confirm that the
nested columns, such as feature intensities, read correctly in Polars, Spark and R.] Files
rewritten by `qpxc transform relayout` may store a score or parameter list as a structure
with one field per name, which a generic reader sees as a structure (in DuckDB, for example,
`additional_scores.diann_cscore`); the `qpx` package reads them back as lists, and the file
metadata lists the columns stored this way. For
anything beyond the small metadata views, we recommend downloading a dataset folder first:
queries over HTTP work, but each read pays the network latency. The query below counts the
confidently identified protein groups per run in one DIA dataset:

```sql
SELECT r.run_file_name, count(*) AS protein_groups
FROM 'PXD004701.pg.parquet' AS pg,
     unnest(pg.grouped_runs) AS r(run_file_name)
WHERE pg.is_decoy IS NOT TRUE AND pg.pg_qvalue <= 0.01
GROUP BY r.run_file_name
ORDER BY protein_groups DESC;
```

The `qpx` Python package (`pip install qpx`; this paper cites version 1.4.0, also available as
the container image `ghcr.io/bigbio/qpx:1.4.0` [TODO: check after the release]) opens a dataset
folder as a single object, runs SQL across its views with DuckDB, converts tool outputs,
validates files and exports quantification results to MuData; its documentation is at
https://qpx.quantms.org.

## QPX Explorer

The QPX Explorer of the quantms portal (https://portal.quantms.org/apps/qpx-explore) opens one
dataset version at a time and queries it with DuckDB on the server. It shows the files and
their row counts, the samples and runs, protein and peptide search and a gallery of curated
queries. [TODO (Yasset): screenshots for Fig. 5 and a short description of the portal around
it.]

## QPX UI

QPX UI (https://github.com/bigbio/qpxui) is an open-source desktop viewer for QPX data, with
installers for macOS, Windows and Linux. It opens a local file or dataset folder, an S3 bucket
or any dataset of the quantms portal and runs queries on the user's machine with DuckDB; from
remote files it fetches only the Parquet metadata and the column chunks a query needs. It
builds a report for each dataset with identification and quality control charts and offers
protein and peptide search, a protein × sample abundance matrix, a spectrum viewer for PSMs
that store their peaks and an SQL console; it does not yet display the AnnData and MuData
files. [TODO: version cited; screenshots for Fig. 5.]

## Reuse

The corpus suits several kinds of reuse without returning to the raw files. Protein-group
quantities from datasets with the same organism and tissue annotation can be combined into
expression atlases; feature-level intensities allow a quantification method to be applied
uniformly across datasets, which supports both meta-analyses and benchmarking of
quantification and normalisation methods; and the PSM records, with their peptidoforms,
charges, retention times and scores, provide training and evaluation data for retention
time and fragment spectrum prediction and for PSM rescoring. [TODO: HLA-binding models,
once immunopeptidomics datasets are included.]

## Caveats

Datasets come from different laboratories, instruments, acquisition methods and labelling
strategies, so quantities are not directly comparable across datasets without
normalisation and correction for batch effects. Error rates are controlled within each
dataset, at the levels and thresholds the workflow applied, which the provenance view records
where the workflow reports them;
combining datasets does not preserve these error rates, and users should filter on the
q-value columns at the level their analysis needs. Intensities are reported as produced by
each workflow (for example, DIA-NN or OpenMS label-free and TMT reporter intensities) and are
not normalised across datasets. Several datasets have more than one QPX version: each version
lives in its own content-addressed folder, and the `qpx_version` and `provenance.json` of each
folder tell which specification and workflow produced it.
