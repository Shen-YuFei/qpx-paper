# Technical Validation

## Schema validation

[TODO: run `qpxc validate` on every deposited dataset with the cited QPX release and report
the result. In the 29 October 2026 snapshot, all 1,198 Parquet files could be opened and
their footers read, but 78 of the 103 latest versions were written with specification 1.0.1
or 1.0.2 and are not expected to pass the current schemas; the 25 written with 1.1 have not
been checked.]

## Storage and query performance

We compared QPX with the mzTab and CSV outputs of the same quantms analyses (Fig. 3)
[TODO: rerun with the cited QPX release, a current DuckDB and the Zstandard default, add
memory use and tool-native outputs, and report the hardware]. For a label-free DDA dataset
(PXD007683, 11 runs, 538,000 PSMs and 500,000 features), counting PSMs took 2 ms on the QPX
files and 1,031 ms on the mzTab file, a 424-fold difference; counting features was 304-fold
faster, filtering PSMs by charge 241-fold, counting distinct proteins 28-fold and selecting
two columns 8-fold, and retrieving the ten most abundant proteins 1.4-fold. The QPX files,
compressed with Snappy in this comparison, were 1.3 times smaller than the gzip-compressed
mzTab and CSV files for this dataset (36.3 versus 48.2 MB) and 2.0 times
smaller for a 120-run TMT 10-plex dataset (30.1 versus 60.8 MB). The gains come from the
columnar layout: a query reads only the columns it uses, skips row groups whose statistics
exclude the filter value, and does not parse text, whereas every query on mzTab has to
decompress and parse the whole file.

## Consistency with the source tool outputs

[TODO: for a set of datasets per converter (MaxQuant, FragPipe, DIA-NN, OpenMS), compare the
number of PSMs, precursors, peptides and protein groups and the intensities in the QPX views
with the original tool outputs, and report the agreement.]

## Comparison with the originally reported results

[TODO: for selected datasets, compare identification numbers and quantities from the
reprocessing with those reported in the original publications.]

## Quality metrics across the corpus

[TODO: distribution of pmultiqc metrics across datasets (Fig. 4), once reports exist for the
deposited datasets.]
