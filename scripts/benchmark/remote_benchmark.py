"""Remote-read benchmark: QPX queries over HTTP with a set latency and bandwidth.

A local HTTP server answers the range requests of DuckDB's httpfs extension for the files of
one or more QPX dataset folders. It delays every response by a fixed latency, delays every new
connection by a fixed setup time, sends all responses through one shared bandwidth limit, and
counts the requests and bytes it sends. Each query runs in a new Python process after duckdb is
imported and httpfs is loaded, so nothing is cached between runs. Downloading the whole view file
over the same link is the reference.

`calibrate` runs the same queries on a file of the quantms portal, over the real network, and on a
local copy of that file served with the latency, setup time and bandwidth measured for that
network, to show how closely the simulated link reproduces the real one.

    python remote_benchmark.py run --dataset qpx=DIR --dataset qpx-relayout=DIR --prefix bench \
        --protein P04406 --run RUN --latency-ms 50 --connect-ms 100 --bandwidth-mbit 100 \
        --repeats 3 --out results.json
    python remote_benchmark.py calibrate --url URL --file FILE --protein P04406 --run RUN \
        --proxy HOST:PORT --latency-ms L --connect-ms C --bandwidth-mbit B --repeats 3 \
        --out calibration.json
"""

from __future__ import annotations

import argparse
import email.utils
import http.server
import json
import os
import platform
import statistics
import subprocess
import sys
import threading
import time
import urllib.request
from importlib.metadata import version
from pathlib import Path

CHUNK = 64 * 1024

FEATURE_QUERIES = {
    "count_features": "SELECT count(*) FROM '{feature}'",
    "one_protein": "SELECT peptidoform, charge, run_file_name, intensities FROM '{feature}' WHERE anchor_protein = '{protein}'",
    "one_run": (
        "SELECT count(*), median(i) FROM "
        "(SELECT unnest(intensities).intensity AS i FROM '{feature}' WHERE run_file_name = '{run}')"
    ),
    "top10_proteins": (
        "SELECT anchor_protein, sum(i.intensity) AS total FROM '{feature}', unnest(intensities) AS t(i) "
        "WHERE anchor_protein IS NOT NULL GROUP BY anchor_protein ORDER BY total DESC LIMIT 10"
    ),
}
# Filters sit in the same SELECT as the unnest: DuckDB 2.0 does not push a filter below a
# lateral unnest into the Parquet scan, which would then read every row group.
PG_QUERIES = {
    "pg_one_protein": "SELECT unnest(grouped_runs) AS run_file_name, intensity FROM '{pg}' WHERE anchor_protein = '{protein}'",
    "pg_per_run": (
        "SELECT run_file_name, count(*) FROM (SELECT unnest(grouped_runs) AS run_file_name FROM '{pg}' "
        "WHERE is_decoy IS NOT TRUE AND pg_qvalue <= 0.01) GROUP BY run_file_name"
    ),
}
QUERIES = {**FEATURE_QUERIES, **PG_QUERIES}
CALIBRATION_QUERIES = ("count_features", "one_protein", "one_run")

# Runs one query in a fresh process: argv[1] the SQL, argv[2] a JSON list of SET statements,
# argv[3] "profile" to run it with EXPLAIN ANALYZE and report DuckDB's own HTTP statistics.
RUNNER = """
import json, re, sys, time
import duckdb
connection = duckdb.connect()
connection.sql("SET enable_progress_bar = false")
connection.sql("LOAD httpfs")
for statement in json.loads(sys.argv[2]):
    connection.sql(statement)
profile = sys.argv[3] == "profile"
start = time.perf_counter()
rows = connection.sql(("EXPLAIN ANALYZE " if profile else "") + sys.argv[1]).fetchall()
result = {"seconds": time.perf_counter() - start, "rows": len(rows)}
if profile:
    plan = rows[0][1]
    amount, unit = re.search(r"in: ([0-9.]+) (\\w+)", plan).groups()
    scale = {"Bytes": 1, "KiB": 2**10, "MiB": 2**20, "GiB": 2**30}[unit]
    result.update(rows=None, duckdb_bytes=float(amount) * scale, duckdb_get=int(re.search(r"#GET: (\\d+)", plan).group(1)))
print(json.dumps(result))
"""

PROXY_VARIABLES = (
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
)


class Link:
    """A link of *rate* bytes per second; chunks are sent in the order they ask for it."""

    def __init__(self, rate: float):
        self.rate = rate
        self.lock = threading.Lock()
        self.free_at = 0.0

    def reserve(self, size: int) -> float:
        """The time at which *size* more bytes have gone through the link."""
        with self.lock:
            self.free_at = max(time.monotonic(), self.free_at) + size / self.rate
            return self.free_at


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    # DuckDB opens a connection per thread and file part; a short backlog drops some of them.
    request_queue_size = 256

    def __init__(
        self,
        files: dict[str, Path],
        latency: float,
        connect: float,
        rate: float,
        connection_rate: float | None,
    ):
        super().__init__(("127.0.0.1", 0), Handler)
        self.files = files
        self.latency = latency
        self.connect = connect
        self.link = Link(rate)
        self.connection_rate = connection_rate
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.counts = {"connections": 0, "head": 0, "get": 0, "bytes": 0}

    def count(self, key: str, amount: int = 1):
        with self.lock:
            self.counts[key] += amount

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def setup(self):
        super().setup()
        self.server.count("connections")
        self.own = (
            Link(self.server.connection_rate) if self.server.connection_rate else None
        )
        time.sleep(self.server.connect)

    def log_message(self, format, *args):
        pass

    def do_HEAD(self):
        self.serve(body=False)

    def do_GET(self):
        self.serve(body=True)

    def serve(self, body: bool):
        path = self.server.files.get(self.path.split("?")[0])
        if path is None:
            self.send_error(404)
            return
        size = path.stat().st_size
        start, end = 0, size - 1
        requested = self.headers.get("Range")
        if requested:
            first, last = requested.removeprefix("bytes=").split("-")
            if first:
                start, end = int(first), min(int(last), size - 1) if last else size - 1
            else:
                start = size - int(last)
        time.sleep(self.server.latency)
        self.send_response(206 if requested else 200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header(
            "Last-Modified", email.utils.formatdate(path.stat().st_mtime, usegmt=True)
        )
        self.send_header("Content-Length", str(end - start + 1))
        if requested:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        self.server.count("get" if body else "head")
        if not body:
            return
        with path.open("rb") as handle:
            handle.seek(start)
            remaining = end - start + 1
            while remaining:
                chunk = handle.read(min(CHUNK, remaining))
                done = self.server.link.reserve(len(chunk))
                if self.own:
                    done = max(done, self.own.reserve(len(chunk)))
                time.sleep(max(0.0, done - time.monotonic()))
                self.wfile.write(chunk)
                remaining -= len(chunk)
        self.server.count("bytes", end - start + 1)


def run_query(
    sql: str, settings: list[str], proxied: bool, profile: bool = False
) -> dict:
    env = (
        dict(os.environ)
        if proxied
        else {k: v for k, v in os.environ.items() if k not in PROXY_VARIABLES}
    )
    command = [
        sys.executable,
        "-I",
        "-c",
        RUNNER,
        sql,
        json.dumps(settings),
        "profile" if profile else "plain",
    ]
    out = subprocess.run(
        command, check=True, stdout=subprocess.PIPE, text=True, env=env
    )
    return json.loads(out.stdout)


def download(url: str) -> dict:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    start = time.perf_counter()
    with opener.open(url) as response:
        size = 0
        while chunk := response.read(1 << 20):
            size += len(chunk)
    return {"seconds": time.perf_counter() - start, "rows": 0, "bytes": size}


def serve(files: dict[str, Path], args) -> Server:
    per_connection = args.connection_mbit * 1e6 / 8 if args.connection_mbit else None
    server = Server(
        files,
        args.latency_ms / 1000,
        args.connect_ms / 1000,
        args.bandwidth_mbit * 1e6 / 8,
        per_connection,
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def measured(server: Server, call) -> dict:
    server.reset()
    result = call()
    return {**result, **server.counts}


def summarize(runs: list[dict], **fields) -> dict:
    keys = (
        "seconds",
        "connections",
        "head",
        "get",
        "bytes",
        "duckdb_bytes",
        "duckdb_get",
    )
    return {
        **fields,
        **{
            f"median_{k}": statistics.median(r[k] for r in runs)
            for k in keys
            if k in runs[0]
        },
        "result_rows": runs[0]["rows"],
        "repeats": len(runs),
    }


def environment(args) -> dict:
    return {
        "python": platform.python_version(),
        "duckdb": version("duckdb"),
        "os": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "latency_ms": args.latency_ms,
        "connect_ms": args.connect_ms,
        "bandwidth_mbit": args.bandwidth_mbit,
        "connection_mbit": args.connection_mbit,
    }


def cmd_run(args):
    layouts = dict(item.split("=", 1) for item in args.dataset)
    files = {}
    for layout, folder in layouts.items():
        for view in ("feature", "pg"):
            files[f"/{layout}/{view}.parquet"] = (
                Path(folder) / f"{args.prefix}.{view}.parquet"
            )
    server = serve(files, args)
    runs: dict[tuple[str, str], list[dict]] = {}
    for _ in range(args.repeats):
        for layout in layouts:
            urls = {
                view: f"{server.base}/{layout}/{view}.parquet"
                for view in ("feature", "pg")
            }
            for query, sql in QUERIES.items():
                text = sql.format(**urls, protein=args.protein, run=args.run)
                runs.setdefault((query, layout), []).append(
                    measured(server, lambda: run_query(text, [], False))
                )
            for view, url in urls.items():
                runs.setdefault((f"download_{view}", layout), []).append(
                    measured(server, lambda: download(url))
                )
    results = [summarize(r, query=q, layout=layout) for (q, layout), r in runs.items()]
    sizes = {
        key.strip("/").removesuffix(".parquet"): path.stat().st_size
        for key, path in files.items()
    }
    Path(args.out).write_text(
        json.dumps(
            {"environment": environment(args), "sizes": sizes, "results": results},
            indent=2,
        )
        + "\n"
    )


def cmd_calibrate(args):
    server = serve({"/feature.parquet": Path(args.file)}, args)
    sides = {
        "portal": (args.url, [f"SET http_proxy = '{args.proxy}'"], True),
        "simulated": (f"{server.base}/feature.parquet", [], False),
    }
    runs: dict[tuple[str, str], list[dict]] = {}
    for _ in range(args.repeats):
        for side, (url, settings, proxied) in sides.items():
            for query in CALIBRATION_QUERIES:
                text = QUERIES[query].format(
                    feature=url, protein=args.protein, run=args.run
                )
                if side == "portal":
                    runs.setdefault((query, side), []).append(
                        run_query(text, settings, proxied, profile=True)
                    )
                else:
                    call = lambda: run_query(text, settings, proxied, profile=True)  # noqa: E731
                    runs.setdefault((query, side), []).append(measured(server, call))
    results = [summarize(r, query=q, side=side) for (q, side), r in runs.items()]
    Path(args.out).write_text(
        json.dumps(
            {"environment": environment(args), "url": args.url, "results": results},
            indent=2,
        )
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("run", "calibrate"):
        command = sub.add_parser(name)
        command.add_argument("--protein", required=True)
        command.add_argument("--run", required=True)
        command.add_argument("--latency-ms", type=float, required=True)
        command.add_argument("--connect-ms", type=float, required=True)
        command.add_argument(
            "--bandwidth-mbit",
            type=float,
            required=True,
            help="shared by all connections",
        )
        command.add_argument(
            "--connection-mbit",
            type=float,
            help="limit of each connection (default: none)",
        )
        command.add_argument("--repeats", type=int, default=3)
        command.add_argument("--out", required=True)
    run = sub.choices["run"]
    run.add_argument(
        "--dataset", action="append", required=True, help="LAYOUT=FOLDER, repeatable"
    )
    run.add_argument("--prefix", default="bench")
    calibrate = sub.choices["calibrate"]
    calibrate.add_argument("--url", required=True)
    calibrate.add_argument("--file", required=True)
    calibrate.add_argument("--proxy", required=True)
    args = parser.parse_args()
    {"run": cmd_run, "calibrate": cmd_calibrate}[args.command](args)


if __name__ == "__main__":
    main()
