# Usage Notes

## Accessing the files

QPX files are plain Parquet files and can be read by any Parquet reader, including DuckDB,
pandas and PyArrow, Polars, Apache Spark and the R arrow package. [TODO: confirm that the
nested columns, such as feature intensities, read correctly in Polars, Spark and R.] For
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

The `qpx` Python package (`pip install qpx`) opens a dataset folder as a single object, runs
SQL across its views with DuckDB, converts tool outputs, validates files and exports
quantification results to MuData. Its documentation (https://qpx.quantms.org) includes a
plain-text version written for large language models (`llms.txt`).

## QPX Explorer

The QPX Explorer of the quantms portal (https://portal.quantms.org/apps/qpx-explore) opens
one dataset version at a time and queries it with DuckDB on the server. It shows the files
and their row counts, the organisms, instruments, runs and samples, lets users search
protein groups and peptides and view per-protein details, and offers a gallery of curated
queries. The same queries are available to AI agents through a Model Context Protocol (MCP)
interface. [TODO (Yasset): screenshots for Fig. 5 and a short description of the portal
around it.]

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
dataset, at the PSM, peptide and protein-group levels recorded in the provenance view;
combining datasets does not preserve these error rates, and users should filter on the
q-value columns at the level their analysis needs. Intensities are reported as produced by
each workflow (for example, DIA-NN or OpenMS label-free and TMT reporter intensities) and are
not normalised across datasets. Several datasets have more than one QPX version: each version
lives in its own content-addressed folder, and the `qpx_version` and `provenance.json` of each
folder tell which specification and workflow produced it.
