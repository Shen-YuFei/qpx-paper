"""Supplementary Figure 1: storage, query time and memory of QPX against the text outputs.

The benchmark (scripts/benchmark/benchmark.py) reads the mzTab and MSstats outputs of one
quantms/OpenMS analysis of PXD007683 with pandas or DuckDB, and the same analysis converted to
QPX, as written and after `qpxc transform relayout`, with DuckDB. Its result files are copied to
data/benchmark/PXD007683_LFQ.

Run: python scripts/figures/figS1_benchmark.py
"""

import json

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

from qpxfig import DOUBLE, INK, MM, MUTED, ROOT, label_panels, log_axis, save

RESULTS = ROOT / "data" / "benchmark" / "PXD007683_LFQ"
MB = 1e6

# Colour marks what is read, the same in every panel (checked for colour-vision deficiency
# with the dataviz palette validator); the marker fill marks the engine.
TEXT, QPX, RELAYOUT = "#8f540a", "#cc6fa3", "#8a3468"
COLOURS = {"mztab": TEXT, "csv": TEXT, "qpx": QPX, "qpx-relayout": RELAYOUT}
OFFSETS = {("mztab", "pandas"): -0.27, ("csv", "pandas"): -0.27, ("csv", "duckdb"): -0.09,
           ("qpx", "duckdb"): 0.09, ("qpx-relayout", "duckdb"): 0.27}
GROUPS = {
    "PSMs": {
        "count_psms": "Count PSMs",
        "distinct_proteins": "Count proteins",
        "filter_charge": "PSMs of charge 2",
        "select_two_columns": "Read two PSM columns",
    },
    "Features": {
        "count_features": "Count features",
        "top10_proteins": "Top 10 proteins",
        "one_protein": "Features of one protein",
    },
}
GAP = 0.7  # extra space above each group, for its name


def storage_rows(sizes):
    """(group, label, bytes, colour) per bar, top to bottom."""
    qpx, relayout = sizes["qpx"], sizes["qpx-relayout"]
    return [
        ("PSMs", "mzTab", sizes["mztab_bytes"], TEXT),
        ("PSMs", "mzTab, gzip", sizes["mztab_gz_bytes"], TEXT),
        ("PSMs", "QPX psm", qpx["psm"]["bytes"], QPX),
        ("PSMs", "QPX psm, relayout", relayout["psm"]["bytes"], RELAYOUT),
        ("Features", "MSstats table", sizes["msstats_bytes"], TEXT),
        ("Features", "MSstats table, gzip", sizes["msstats_gz_bytes"], TEXT),
        ("Features", "QPX feature", qpx["feature"]["bytes"], QPX),
        ("Features", "QPX feature, relayout", relayout["feature"]["bytes"], RELAYOUT),
        ("All results", "OpenMS consensusXML", sizes["consensusxml_bytes"], TEXT),
        ("All results", "QPX, all views", sum(v["bytes"] for v in qpx.values()), QPX),
        ("All results", "QPX, all views, relayout", sum(v["bytes"] for v in relayout.values()),
         RELAYOUT),
    ]


def grouped_rows(ax, groups, names=True):
    """Place the rows of each group under its name; groups maps a name to row labels.
    Returns the y of each row label."""
    y, ys, ticks = 0.0, {}, []
    for name, labels in groups.items():
        y += GAP if ys else 0
        if names:
                ax.text(-0.02, y - 0.75, name, transform=ax.get_yaxis_transform(), ha="right",
                    va="center", fontsize=5.5, color=MUTED, fontweight="bold")
        for label in labels:
            ys[label] = y
            ticks.append((y, labels[label] if isinstance(labels, dict) else label))
            y += 1
    ax.set_yticks([t for t, _ in ticks], [lab for _, lab in ticks])
    ax.set_ylim(y - 0.4, -1.1)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    return ys


def storage(ax, sizes):
    rows = storage_rows(sizes)
    groups = {}
    for group, label, _, _ in rows:
        groups.setdefault(group, []).append(label)
    ys = grouped_rows(ax, groups)
    for _, label, size, colour in rows:
        ax.barh(ys[label], size / MB, height=0.72, color=colour, linewidth=0)
        ax.text(size / MB * 1.12, ys[label], f"{size / MB:,.1f}", va="center", fontsize=5.5,
                color=INK)
    log_axis(ax, [r[2] / MB for r in rows] + [3000])
    ax.set_xlabel("File size (MB)")


def dots(ax, results, field, xlabel, labels):
    ys = grouped_rows(ax, GROUPS, names=labels)
    if not labels:
        ax.set_yticklabels([])
    for y in ys.values():
        ax.axhline(y, color="#ececec", lw=0.4, zorder=1)
    for r in results:
        colour = COLOURS[r["format"]]
        ax.scatter(r[field], ys[r["query"]] + OFFSETS[(r["format"], r["engine"])], s=9,
                   color=colour if r["engine"] == "duckdb" else "white", edgecolors=colour,
                   linewidths=0.6, zorder=3)
    log_axis(ax, [r[field] for r in results])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _pos: f"{x:,g}"))
    ax.set_xlabel(xlabel)


def main():
    sizes = json.loads((RESULTS / "sizes.json").read_text())
    results = json.loads((RESULTS / "results.json").read_text())["results"]
    fig = plt.figure(figsize=(DOUBLE, 72 * MM))
    a = fig.add_axes([0.155, 0.15, 0.2, 0.64])
    b = fig.add_axes([0.53, 0.15, 0.2, 0.64])
    c = fig.add_axes([0.77, 0.15, 0.2, 0.64])
    storage(a, sizes)
    dots(b, results, "median_seconds", "Median query time (s)", labels=True)
    dots(c, results, "median_peak_mib", "Median peak memory (MiB)", labels=False)

    def marker(colour, fill):
        return Line2D([], [], marker="o", ls="", ms=3.2, markerfacecolor=fill,
                      markeredgecolor=colour, markeredgewidth=0.6)

    # Filled column by column: the formats in the first row, the engines in the second.
    handles = [marker(TEXT, TEXT), marker(INK, "white"), marker(QPX, QPX), marker(INK, INK),
               marker(RELAYOUT, RELAYOUT)]
    names = ["mzTab, MSstats table or consensusXML", "Read with pandas", "QPX",
             "Read with DuckDB", "QPX after relayout"]
    fig.legend(handles, names, loc="lower left", ncol=3, bbox_to_anchor=(0.155, 0.885),
               handletextpad=0.2, columnspacing=1.2, borderaxespad=0, fontsize=6)
    label_panels(fig, [a, b, c], ["Storage", "Query time", "Peak memory"])
    save(fig, "figS1")


if __name__ == "__main__":
    main()
