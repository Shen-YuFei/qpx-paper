"""Storage and query benchmark of QPX against the text outputs of the same analysis.

The text side is the gzip-compressed mzTab (PSM queries) and MSstats input table (feature
queries) of one quantms/OpenMS analysis; the QPX side is the same analysis converted with
`qpxc convert openms-consensus`, both as written (`qpx`) and after `qpxc transform relayout`
(`qpx-relayout`). Every measurement runs in a fresh Python process, so peak memory is per
query; times are medians over repeated runs on a warm page cache.

    python benchmark.py prepare --workdir DIR --consensusxml X --msstats CSV --mztab MZTAB --sdrf SDRF
    python benchmark.py run --workdir DIR --repeats 5
    python benchmark.py storage --workdir DIR --msstats CSV --sdrf SDRF
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import os
import platform
import resource
import shutil
import statistics
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

PREFIX = "bench"

QPX_LAYOUTS = ("qpx", "qpx-relayout")

# (query, text format, text engine) — every query also runs on both QPX layouts with DuckDB.
QUERIES = [
    ("count_psms", "mztab", "pandas"),
    ("distinct_proteins", "mztab", "pandas"),
    ("filter_charge", "mztab", "pandas"),
    ("select_two_columns", "mztab", "pandas"),
    ("count_features", "csv", "pandas"),
    ("top10_proteins", "csv", "pandas"),
    ("one_protein", "csv", "pandas"),
    ("count_features", "csv", "duckdb"),
    ("top10_proteins", "csv", "duckdb"),
    ("one_protein", "csv", "duckdb"),
]

# A protein quantified in every run of PXD007683, as QPX and the MSstats table name it.
PROTEIN = ("P55011", "sp|P55011|S12A2_HUMAN")

QPX_SQL = {
    "count_psms": "SELECT count(*) FROM '{psm}'",
    "distinct_proteins": "SELECT count(DISTINCT p) FROM (SELECT unnest(protein_accessions) AS p FROM '{psm}')",
    "filter_charge": "SELECT count(*) FROM '{psm}' WHERE charge = 2",
    "select_two_columns": "SELECT peptidoform, charge FROM '{psm}'",
    "count_features": "SELECT count(*) FROM '{feature}'",
    "top10_proteins": (
        "SELECT anchor_protein, sum(i.intensity) AS total FROM '{feature}', unnest(intensities) AS t(i) "
        "WHERE anchor_protein IS NOT NULL GROUP BY anchor_protein ORDER BY total DESC LIMIT 10"
    ),
    "one_protein": (
        f"SELECT peptidoform, charge, run_file_name, intensities FROM '{{feature}}' WHERE anchor_protein = '{PROTEIN[0]}'"
    ),
}

CSV_SQL = {
    "count_features": "SELECT count(*) FROM read_csv('{csv}')",
    "top10_proteins": (
        "SELECT ProteinName, sum(Intensity) AS total FROM read_csv('{csv}') "
        "GROUP BY ProteinName ORDER BY total DESC LIMIT 10"
    ),
    "one_protein": f"SELECT PeptideSequence, PrecursorCharge, Run, Intensity FROM read_csv('{{csv}}') WHERE ProteinName = '{PROTEIN[1]}'",
}


def read_mztab_psms(path: Path):
    """Read the PSM section of a gzip mzTab file into pandas, as a user of the file would."""
    import pandas as pd

    with gzip.open(path, "rt") as handle:
        lines = [line for line in handle if line.startswith(("PSH", "PSM"))]
    return pd.read_csv(io.StringIO("".join(lines)), sep="\t", low_memory=False)


def run_text_pandas(query: str, workdir: Path):
    import pandas as pd

    if query in ("count_features", "top10_proteins", "one_protein"):
        table = pd.read_csv(workdir / f"{PREFIX}.msstats.csv.gz")
        if query == "count_features":
            return len(table)
        if query == "one_protein":
            return table.loc[table["ProteinName"] == PROTEIN[1], ["PeptideSequence", "PrecursorCharge", "Run", "Intensity"]]
        return table.groupby("ProteinName")["Intensity"].sum().nlargest(10)
    psms = read_mztab_psms(workdir / f"{PREFIX}.mzTab.gz")
    if query == "count_psms":
        return len(psms)
    if query == "distinct_proteins":
        # mzTab joins the proteins of a PSM with commas, each as db|accession|entry name.
        return psms["accession"].str.split(",").explode().str.split("|").str[1].nunique()
    if query == "filter_charge":
        return int((psms["charge"] == 2).sum())
    return psms[["sequence", "charge"]]


def run_duckdb(sql: str):
    import duckdb

    return duckdb.sql(sql).df()


def measure_one(fmt: str, engine: str, query: str, workdir: Path) -> dict:
    """Run one query once in this process and report its wall time and peak memory increase."""
    import duckdb  # noqa: F401  (import cost is outside the measurement)
    import pandas  # noqa: F401

    folder = workdir / fmt
    sql = QPX_SQL[query].format(psm=folder / f"{PREFIX}.psm.parquet", feature=folder / f"{PREFIX}.feature.parquet")
    baseline = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start = time.perf_counter()
    if fmt in QPX_LAYOUTS:
        result = run_duckdb(sql)
    elif engine == "duckdb":
        result = run_duckdb(CSV_SQL[query].format(csv=workdir / f"{PREFIX}.msstats.csv.gz"))
    else:
        result = run_text_pandas(query, workdir)
    seconds = time.perf_counter() - start
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if hasattr(result, "shape") and result.shape == (1, 1):
        result = result.iat[0, 0]
    rows = len(result) if hasattr(result, "__len__") else 1
    answer = int(result) if rows == 1 else None
    return {"seconds": seconds, "peak_mib": (peak - baseline) / 1024, "result_rows": rows, "answer": answer}


def parquet_layout(path: Path) -> dict:
    """Size, rows, row groups, codecs and recorded sort order of one Parquet file."""
    import pyarrow.parquet as pq

    meta = pq.ParquetFile(path).metadata
    groups = [meta.row_group(i) for i in range(meta.num_row_groups)]
    return {
        "bytes": path.stat().st_size,
        "rows": meta.num_rows,
        "row_groups": meta.num_row_groups,
        "max_rows_per_group": max(g.num_rows for g in groups),
        "codecs": sorted({g.column(j).compression for g in groups for j in range(g.num_columns)}),
        "sorting_columns": [meta.schema.column(c.column_index).path for c in groups[0].sorting_columns],
    }


def file_sizes(workdir: Path, consensusxml: Path) -> dict:
    return {
        "consensusxml_bytes": consensusxml.stat().st_size,
        "mztab_bytes": (workdir / f"{PREFIX}.mzTab").stat().st_size,
        "mztab_gz_bytes": (workdir / f"{PREFIX}.mzTab.gz").stat().st_size,
        "msstats_bytes": (workdir / f"{PREFIX}.msstats.csv").stat().st_size,
        "msstats_gz_bytes": (workdir / f"{PREFIX}.msstats.csv.gz").stat().st_size,
        **{
            layout: {p.name.split(".")[1]: parquet_layout(p) for p in sorted((workdir / layout).glob(f"{PREFIX}.*.parquet"))}
            for layout in QPX_LAYOUTS
        },
    }


def gzip_copy(source: Path, plain: Path, packed: Path) -> None:
    shutil.copyfile(source, plain)
    with open(plain, "rb") as src, gzip.open(packed, "wb", compresslevel=6) as dst:
        shutil.copyfileobj(src, dst)


def prepare(args) -> None:
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    gzip_copy(Path(args.mztab), workdir / f"{PREFIX}.mzTab", workdir / f"{PREFIX}.mzTab.gz")
    gzip_copy(Path(args.msstats), workdir / f"{PREFIX}.msstats.csv", workdir / f"{PREFIX}.msstats.csv.gz")
    out = workdir / "qpx"
    shutil.rmtree(out, ignore_errors=True)
    start = time.perf_counter()
    subprocess.run(
        [
            "qpxc", "convert", "openms-consensus",
            "--consensusxml", args.consensusxml,
            "--sdrf-file", args.sdrf,
            "--output-folder", str(out),
            "--output-prefix", PREFIX,
            "--structures", "psm,feature,pg",
            "--no-mudata",
        ],
        check=True,
    )
    convert_seconds = time.perf_counter() - start
    relayout = workdir / "qpx-relayout"
    shutil.rmtree(relayout, ignore_errors=True)
    start = time.perf_counter()
    subprocess.run(["qpxc", "transform", "relayout", "--dataset", str(out), "--output-folder", str(relayout)], check=True)
    relayout_seconds = time.perf_counter() - start
    sizes = file_sizes(workdir, Path(args.consensusxml))
    timing = {"convert_seconds": convert_seconds, "relayout_seconds": relayout_seconds, "hardware": hardware()}
    (workdir / "sizes.json").write_text(json.dumps({**sizes, **timing}, indent=2))


def storage(args) -> None:
    """Storage only: a gzip MSstats input table against its QPX feature view (e.g. for TMT data)."""
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    plain, packed = workdir / f"{PREFIX}.msstats.csv", workdir / f"{PREFIX}.msstats.csv.gz"
    gzip_copy(Path(args.msstats), plain, packed)
    out = workdir / "qpx"
    shutil.rmtree(out, ignore_errors=True)
    subprocess.run(
        [
            "qpxc", "convert", "quantms-msstats",
            "--msstats-file", args.msstats,
            "--sdrf-file", args.sdrf,
            "--output-folder", str(out),
            "--output-prefix", PREFIX,
        ],
        check=True,
    )
    sizes = {
        "msstats_bytes": plain.stat().st_size,
        "msstats_gz_bytes": packed.stat().st_size,
        "msstats_rows": sum(1 for _ in open(plain)) - 1,
        "qpx_feature_bytes": (out / f"{PREFIX}.feature.parquet").stat().st_size,
    }
    (workdir / "sizes.json").write_text(json.dumps(sizes, indent=2))


def hardware() -> dict:
    import qpx

    cpu = next(
        (line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")),
        platform.processor(),
    )
    mem_kib = int(next(line.split()[1] for line in Path("/proc/meminfo").read_text().splitlines() if line.startswith("MemTotal")))
    return {
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "memory_gib": round(mem_kib / 1024**2, 1),
        "os": platform.platform(),
        "python": platform.python_version(),
        "qpx": version("qpx"),
        # An editable install reports the version of its last install; the commit pins the code.
        "qpx_commit": subprocess.run(
            ["git", "-C", str(Path(qpx.__file__).parents[1]), "describe", "--always", "--dirty"],
            capture_output=True, text=True,
        ).stdout.strip(),
        "duckdb": version("duckdb"),
        "pandas": version("pandas"),
        "pyarrow": version("pyarrow"),
        "load_average": os.getloadavg(),
    }


def run(args) -> None:
    workdir = Path(args.workdir)
    cases = list(QUERIES) + [(q, layout, "duckdb") for layout in QPX_LAYOUTS for q in QPX_SQL]
    results = []
    for query, fmt, engine in cases:
        runs = []
        for _ in range(args.repeats):
            out = subprocess.run(
                [sys.executable, __file__, "one", "--workdir", str(workdir), fmt, engine, query],
                check=True, capture_output=True, text=True,
            )
            runs.append(json.loads(out.stdout))
        results.append(
            {
                "query": query,
                "format": fmt,
                "engine": engine,
                "median_seconds": statistics.median(r["seconds"] for r in runs),
                "median_peak_mib": statistics.median(r["peak_mib"] for r in runs),
                "result_rows": runs[0]["result_rows"],
                "answer": runs[0]["answer"],
                "repeats": args.repeats,
            }
        )
        print(json.dumps(results[-1]), flush=True)
    (workdir / "results.json").write_text(json.dumps({"hardware": hardware(), "results": results}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    for name in ("workdir", "consensusxml", "msstats", "mztab", "sdrf"):
        p.add_argument(f"--{name}", required=True)
    s = sub.add_parser("storage")
    for name in ("workdir", "msstats", "sdrf"):
        s.add_argument(f"--{name}", required=True)
    r = sub.add_parser("run")
    r.add_argument("--workdir", required=True)
    r.add_argument("--repeats", type=int, default=5)
    o = sub.add_parser("one")
    o.add_argument("--workdir", required=True)
    o.add_argument("fmt")
    o.add_argument("engine")
    o.add_argument("query")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args)
    elif args.command == "storage":
        storage(args)
    elif args.command == "run":
        run(args)
    else:
        print(json.dumps(measure_one(args.fmt, args.engine, args.query, Path(args.workdir))))


if __name__ == "__main__":
    main()
