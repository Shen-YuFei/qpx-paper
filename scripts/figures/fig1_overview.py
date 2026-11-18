"""Figure 1: overview of how the corpus was built and how it is accessed.

Run: python scripts/figures/fig1_overview.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from qpxfig import DOUBLE, INK, MM, MUTED, PANEL_FILL, ROUTE_COLOURS, RULE, save

W, H = 183, 78  # mm


def box(ax, x, y, w, h, fill="white", edge=INK, lw=0.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=fill, ec=edge, lw=lw))


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=6,
                                 lw=0.6, color=INK, shrinkA=0, shrinkB=0))


def text(ax, x, y, s, size=6, weight="normal", ha="left", va="center", color=INK):
    ax.text(x, y, s, fontsize=size, fontweight=weight, ha=ha, va=va, color=color,
            linespacing=1.25)


def main():
    fig = plt.figure(figsize=(DOUBLE, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    cols = [(2, 36), (46, 40), (96, 46), (152, 29)]
    heads = ["Public datasets", "Reprocessing", "QPX dataset", "Access"]
    for (x, w), head in zip(cols, heads):
        text(ax, x, H - 3, head, size=7, weight="bold", va="top")
        ax.plot([x, x + w], [H - 8, H - 8], color=RULE, lw=0.5)

    # Column 1: sources and sample annotation.
    x, w = cols[0]
    box(ax, x, 40, w, 26, fill=PANEL_FILL, edge=PANEL_FILL)
    text(ax, x + 2, 62.5, "Repositories", weight="bold", va="top")
    text(ax, x + 2, 57.5, "ProteomeXchange members\n(PRIDE, iProX, MassIVE)\nProteomic Data Commons\nOther public studies",
         va="top")
    box(ax, x, 12, w, 22, fill=PANEL_FILL, edge=PANEL_FILL)
    text(ax, x + 2, 30.5, "Sample annotation", weight="bold", va="top")
    text(ax, x + 2, 25.5, "SDRF-Proteomics files\nlinking runs to samples,\nlabels and ontology terms",
         va="top")

    # Column 2: one box per processing route, in the order of Table 3.
    x, w = cols[1]
    routes = [
        ("ID only", "quantms-msnet recipe", "Identification only"),
        ("DIA-NN", "quantmsdiann (DIA-NN)", "DIA, label-free"),
        ("OpenMS", "quantms (OpenMS)", "DDA, label-free and TMT"),
    ]
    ys = [52, 32, 12]
    for (route, name, sub), y in zip(routes, ys):
        box(ax, x, y, w, 14, fill="white", edge=RULE)
        ax.add_patch(Rectangle((x, y), 1.6, 14, fc=ROUTE_COLOURS[route], ec="none"))
        text(ax, x + 4, y + 9.2, name, weight="bold")
        text(ax, x + 4, y + 4.4, sub, color=MUTED)
    for y in ys:
        arrow(ax, cols[0][0] + cols[0][1] + 1, 39, x - 1, y + 7)

    # Column 3: the QPX views, grouped by what they hold.
    x, w = cols[2]
    groups = [
        ("Identification", "psm"),
        ("Quantification", "feature, pg"),
        ("Mapping and annotation", "pepmap, protein, site"),
        ("Metadata", "sample, run, dataset, ontology, provenance"),
        ("Expression", "AnnData and MuData files"),
    ]
    box(ax, x, 8, w, 60, fill=PANEL_FILL, edge=PANEL_FILL)
    text(ax, x + 2, 65.5, "Parquet views and SDRF, one folder per dataset", color=MUTED,
         va="top", size=5.5)
    gy = [52, 41.5, 31, 20.5, 10]
    for (name, views), y in zip(groups, gy):
        box(ax, x + 2, y, w - 4, 9, fill="white", edge=RULE)
        text(ax, x + 4, y + 6, name, weight="bold")
        text(ax, x + 4, y + 2.6, views, color=MUTED, size=5.5)
    for y in ys:
        arrow(ax, cols[1][0] + cols[1][1] + 1, y + 7, x - 1, 37)

    # Column 4: ways to read the data.
    x, w = cols[3]
    access = [
        ("QPX Explorer", "quantms portal"),
        ("QPX UI", "desktop viewer"),
        ("SQL", "DuckDB and other engines"),
        ("Python", "qpx package"),
    ]
    ay = [54, 40, 26, 12]
    for (name, sub), y in zip(access, ay):
        box(ax, x, y, w, 11, fill="white", edge=RULE)
        text(ax, x + 2.5, y + 7.2, name, weight="bold")
        text(ax, x + 2.5, y + 3.2, sub, color=MUTED, size=5.5)
        arrow(ax, cols[2][0] + cols[2][1] + 1, 37, x - 1, y + 5.5)

    save(fig, "fig1")


if __name__ == "__main__":
    main()
