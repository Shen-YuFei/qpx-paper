# Supplementary Information

Supplementary Figure 1: Query time and storage of QPX compared with mzTab and CSV outputs.
[TODO: figure from the rerun benchmark. Rerun `scripts/benchmark/benchmark.py` with QPX 1.4.0
and a current DuckDB, on both the default converter output (Zstandard, per-column encodings)
and the output of `qpxc transform relayout` (sorted, renumbered, rounded, structure lists),
state for each the codec, row-group sizes and layout, add memory use and tool-native outputs,
and report the hardware. The earlier numbers, from Snappy-compressed files written by an
earlier QPX release, are in commit a82ea5f.]
