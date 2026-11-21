"""Supplementary Figure 3: remote reads of QPX over a simulated network link.

The benchmark (scripts/benchmark/remote_benchmark.py) serves the feature and pg views of the
DIA-NN analysis of PXD041421, as written and after `qpxc transform relayout`, from a local HTTP
server with a set latency and bandwidth, and queries them with DuckDB. It also queries a file of
the quantms portal over the real network and a local copy of it over a link set to the latency
and bandwidth measured for that network. Its result files are in data/benchmark/PXD041421_DIANN.

Run: python scripts/figures/figS3_remote.py
"""

import json

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

from figS1_benchmark import QPX, RELAYOUT, grouped_rows
from qpxfig import DOUBLE, MM, MUTED, ROOT, label_panels, log_axis, save

RESULTS = ROOT / "data" / "benchmark" / "PXD041421_DIANN"
MB = 1e6

COLOURS = {"qpx": QPX, "qpx-relayout": RELAYOUT}
OFFSETS = {"qpx": -0.14, "qpx-relayout": 0.14, "portal": -0.14, "simulated": 0.14}
GROUPS = {
    "Features": {
        "count_features": "Count features",
        "one_protein": "Features of one protein",
        "one_run": "Intensities of one run",
        "top10_proteins": "Top 10 proteins",
        "download_feature": "Download the file",
    },
    "Protein groups": {
        "pg_one_protein": "Groups of one protein",
        "pg_per_run": "Groups per run",
        "download_pg": "Download the file",
    },
}
CALIBRATION = {"Portal file": {
    "count_features": "Count features",
    "one_protein": "Features of one protein",
    "one_run": "Intensities of one run",
}}


def dots(ax, groups, results, field, scale, xlabel, labels):
    ys = grouped_rows(ax, groups, names=labels)
    if not labels:
        ax.set_yticklabels([])
    for y in ys.values():
        ax.axhline(y, color="#ececec", lw=0.4, zorder=1)
    values = []
    for r in results:
        side = r.get("layout", r.get("side"))
        colour = COLOURS.get(side, MUTED)
        value = r[field] / scale
        values.append(value)
        ax.scatter(value, ys[r["query"]] + OFFSETS[side], s=9,
                   color="white" if side == "simulated" else colour, edgecolors=colour,
                   linewidths=0.6, zorder=3)
    log_axis(ax, values)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _pos: f"{x:,g}"))
    ax.set_xlabel(xlabel)


def main():
    remote = json.loads((RESULTS / "remote.json").read_text())["results"]
    calibration = json.loads((RESULTS / "calibration.json").read_text())["results"]
    fig = plt.figure(figsize=(DOUBLE, 62 * MM))
    a = fig.add_axes([0.16, 0.17, 0.2, 0.6])
    b = fig.add_axes([0.39, 0.17, 0.2, 0.6])
    c = fig.add_axes([0.77, 0.17, 0.2, 0.6])
    dots(a, GROUPS, remote, "median_bytes", MB, "Data transferred (MB)", labels=True)
    dots(b, GROUPS, remote, "median_seconds", 1, "Median query time (s)", labels=False)
    dots(c, CALIBRATION, calibration, "median_seconds", 1, "Median query time (s)", labels=True)

    def marker(colour, fill):
        return Line2D([], [], marker="o", ls="", ms=3.2, markerfacecolor=fill,
                      markeredgecolor=colour, markeredgewidth=0.6)

    handles = [marker(QPX, QPX), marker(RELAYOUT, RELAYOUT), marker(MUTED, MUTED),
               marker(MUTED, "white")]
    names = ["QPX", "QPX after relayout", "Portal, real network", "Same file, simulated link"]
    fig.legend(handles, names, loc="lower left", ncol=4, bbox_to_anchor=(0.16, 0.885),
               handletextpad=0.2, columnspacing=1.2, borderaxespad=0, fontsize=6)
    label_panels(fig, [a, b, c], ["Data transferred", "Query time, simulated link",
                                  "Simulated against real network"])
    save(fig, "figS3")


if __name__ == "__main__":
    main()
