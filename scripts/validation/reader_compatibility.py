"""Read every QPX view with Polars, Spark and R and compare the values with PyArrow's.

R reads each view into data frames and writes it back (r_roundtrip.R), so that its values can be
compared here. Used for the reader sentence of the Usage Notes, on the benchmark dataset of
Supplementary Fig. S1 (scripts/benchmark/benchmark.py prepare writes the two layouts).

    Rscript scripts/validation/r_roundtrip.R WORKDIR/qpx R_OUT/qpx
    Rscript scripts/validation/r_roundtrip.R WORKDIR/qpx-relayout R_OUT/qpx-relayout
    python scripts/validation/reader_compatibility.py WORKDIR R_OUT
"""

import math
import sys
from pathlib import Path

import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq


def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return a == b or (math.isnan(a) and math.isnan(b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def pairs(value):
    """A map value as R writes it back (key-value structs) or as PyArrow reads it (tuples)."""
    if value is None:
        return None
    return sorted((x["key"], x["value"]) if isinstance(x, dict) else tuple(x) for x in value)


def compare(ref: pa.Table, other: pa.Table) -> list[str]:
    problems = []
    if other.num_rows != ref.num_rows:
        return [f"rows {other.num_rows} != {ref.num_rows}"]
    if set(other.column_names) != set(ref.column_names):
        return [f"columns differ: {set(ref.column_names) ^ set(other.column_names)}"]
    for name in ref.column_names:
        want = ref.column(name)
        if pa.types.is_map(want.type):
            got_pairs = [pairs(v) for v in other.column(name).to_pylist()]
            if got_pairs != [pairs(v) for v in want.to_pylist()]:
                problems.append(f"{name}: map values differ")
            continue
        try:
            got = other.column(name).cast(want.type)
        except (pa.ArrowInvalid, pa.ArrowNotImplementedError) as error:
            problems.append(f"{name}: cannot cast {other.column(name).type} to {want.type}: {error}")
            continue
        if got.equals(want):
            continue
        bad = sum(not same(x, y) for x, y in zip(got.to_pylist(), want.to_pylist()))
        if bad:
            problems.append(f"{name}: {bad} rows differ")
    return problems


def main():
    root, rout = Path(sys.argv[1]), Path(sys.argv[2])
    from pyspark.sql import SparkSession

    spark = (SparkSession.builder.master("local[24]").config("spark.driver.memory", "24g")
             .config("spark.sql.session.timeZone", "UTC")
             # The vectorized reader of Spark 4.2 cannot decode BYTE_STREAM_SPLIT float columns.
             .config("spark.sql.parquet.enableVectorizedReader", "false").getOrCreate())
    spark.sparkContext.setLogLevel("OFF")
    print("polars", pl.__version__, "pyspark", spark.version, "pyarrow", pa.__version__)
    for layout in ("qpx", "qpx-relayout"):
        for path in sorted((root / layout).glob("*.parquet")):
            ref = pq.read_table(path)
            spark_df = spark.read.parquet(str(path))
            results = {
                "polars": compare(ref, pl.read_parquet(path).to_arrow()),
                "spark": compare(ref, spark_df.toArrow()),
                "R": compare(ref, pq.read_table(rout / layout / path.name)),
            }
            for engine, problems in results.items():
                print(layout, path.name, engine, "OK" if not problems else problems, flush=True)
    spark.stop()


if __name__ == "__main__":
    main()
