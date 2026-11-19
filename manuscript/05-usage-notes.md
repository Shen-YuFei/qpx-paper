# Usage Notes

## Accessing the files

QPX files are plain Parquet files and can be read by any Parquet reader, including DuckDB,
pandas and PyArrow, Polars, Apache Spark and the R arrow package. [TBD: reading of nested columns in Polars, Spark and R] Files
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
the container image `ghcr.io/bigbio/qpx:1.4.0` [TBD: container image]) opens a dataset
folder as a single object, runs SQL across its views with DuckDB, converts tool outputs,
validates files and exports quantification results to MuData; its documentation is at
https://qpx.quantms.org. An example Python script in the repository of this paper
(`examples/read_dataset.py`; see Code Availability) attaches the sample of each quantification
unit to the protein-group quantities, joins feature intensities to the sample annotations and
assigns peptides to the folds described below.

## QPX Explorer

The QPX Explorer of the quantms portal (https://portal.quantms.org/apps/qpx-explore) opens one
dataset version at a time and queries it with DuckDB on the server. It shows the files and
their row counts, the samples and runs, protein and peptide search and a gallery of curated
queries (Fig. 4a). [TBD: portal description]

## QPX UI

QPX UI (https://github.com/bigbio/qpxui) is an open-source desktop viewer for macOS, Windows
and Linux that opens a local dataset folder, an S3 bucket or any dataset of the quantms portal.
It queries the data with DuckDB on the user's machine, reading only the parts of remote files a
query needs, and builds a report with identification and quality control charts for each
dataset (Fig. 4b). [TBD: version cited]

## Error rates and decoys

Every `psm`, `feature` and `pg` row has an `is_decoy` flag, and the q-values are stored as the
workflow computed them: `psm.qvalue` for PSMs, `feature.precursor_qvalue` and
`feature.global_qvalue` for precursors within a run and across the dataset, and `pg.pg_qvalue`
and `pg.global_qvalue` for protein groups within a run and across the dataset. A null q-value
means that the source reported none. To use the rows at a given error rate, drop the decoys and
filter on the q-value of the level the analysis needs; the `confident()` methods of the `qpx`
package do this for PSMs and features. [TBD: export threshold and decoys of each subset]

## Quantities and missing values

A feature row holds one primary intensity per label channel (`intensities`), and a `pg` row one
primary `intensity` for its label; further quantities reported by the tool, such as normalised,
label-free quantification (LFQ) or intensity-based absolute quantification (iBAQ) values, are kept under their tool names in `additional_intensities`. Several
quantities can therefore exist for the same row, and analyses should state which one they used.
[TBD: source of the primary quantities of each subset] Missing values take three forms. A null intensity in an existing row means that the
peptide or protein group was identified in that run or channel but not quantified; a missing row
means that it was neither identified nor quantified there, as the converters add no zero or null
placeholders; and a null in any other column means that the source did not report the value.
[TBD: meaning of zero intensities in TMT datasets]

## Numerical precision and identifiers

Files rewritten by `qpxc transform relayout` keep 12 mantissa bits for intensities and mass
errors and 16 for retention times, ion mobilities and collisional cross sections, a relative error
of at most 1.2 × 10^-4^ for intensities, well below the variation between repeated measurements of
a precursor; the file metadata key `qpx.mantissa_bits` lists the rounded columns. Scores, q-values
and m/z values are not rounded, so the rows that pass a threshold do not change, but intensities
should be compared with a tolerance rather than for equality. Row identifiers (`psm_id`,
`feature_id`, `pg_id`) are unique within a dataset version only: relayout renumbers them, and
older specifications derive them differently. To match records across versions or datasets, use
the content columns, such as the peptidoform, charge, run file name and protein accessions.
[TBD: whether the deposited files were rewritten with relayout]

## Reuse

The corpus suits several kinds of reuse without returning to the raw files. Protein-group
quantities from datasets with the same organism and tissue annotation can be combined into
expression atlases; feature-level intensities allow a quantification method to be applied
uniformly across datasets, which supports both meta-analyses and benchmarking of
quantification and normalisation methods; and the PSM records, with their peptidoforms,
charges, retention times and scores, provide training and evaluation data for retention
time and fragment spectrum prediction and for PSM rescoring. [TBD: HLA-binding models]

## Splits for machine learning

Models of peptide properties overestimate their accuracy when the same peptide occurs in the
training and the test data, including in another modified form or another dataset
[@Wen_2024]. We recommend assigning peptides to ten folds by sequence: take the unmodified
`sequence`, replace isoleucine by leucine, compute the MD5 digest of the upper-case string, read
it as a big-endian integer and take the remainder modulo 10. All peptidoforms and PSMs of a
sequence then fall in the same fold, in every dataset and every version of the corpus, without a
separate split file; we suggest folds 8 and 9 for validation and testing. The example scripts
implement this rule.

## Combining datasets

Datasets come from different laboratories, instruments, acquisition methods and labelling
strategies, so quantities are not directly comparable across datasets without normalisation and
correction for batch effects. Intensities are reported as produced by each workflow (for
example, DIA-NN or OpenMS label-free and TMT reporter intensities) and are not normalised across
datasets. Error rates are controlled within each dataset, at the levels and thresholds the
workflow applied, which the provenance view records where the workflow reports them; combining
datasets does not preserve these error rates.

The workflows read the enzyme, modifications and labels of each dataset from its SDRF but apply
one search and quantification strategy per route. Studies whose design calls for a specialised
analysis, such as cross-linking, glycoproteomics, open modification searches or non-specific
digestion, are represented only by what this strategy finds, which can differ from the results of
the original publication; the SDRF allows such datasets to be reprocessed with other settings.
[TBD: datasets to which this applies]

## Known issues

Known issues of individual datasets are listed in the `known_issues` column of
`datasets.csv`. [TBD: known issues and where to report them]

## Versions and citation

Each processed version of a dataset is a folder named by its content hash, added next to the
earlier versions rather than replacing them, and each file records its specification version
(`qpx_version`). Users should report the accession and version folder of every dataset they
use, cite this paper and the deposited record [TBD: DOI and versioning of the deposited record],
and cite the original data of each dataset, given in `datasets.csv`, since the results
derive from the submitters' raw files.
