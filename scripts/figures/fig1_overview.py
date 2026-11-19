"""Figure 1: overview of how the corpus was built and how it is accessed.

The counts per processing route and the corpus totals come from the same snapshot tables as
Fig. 2 and are checked against Table 3; a view or file that no dataset holds is drawn dashed
(Supplementary Fig. 2 shows the views per dataset).

Run: python scripts/figures/fig1_overview.py
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

from fig2_corpus import SNAPSHOT, check, load
from figS2_coverage import presence
from qpxfig import DOUBLE, INK, MM, MONO, MUTED, PANEL_FILL, ROUTE_COLOURS, ROUTES, RULE, save

W, H = 183, 88  # mm
DATA_HEAD = "#3d3d3d"
META_HEAD = "#8a8a8a"
STRIPE = "#e3e3e3"


def box(ax, x, y, w, h, fill="white", edge=RULE, lw=0.5, dashed=False, r=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fill, ec=edge, lw=lw, ls=(0, (2, 1.2)) if dashed else "-"))


def text(ax, x, y, s, size=6, weight="normal", ha="left", va="center", color=INK, family=None):
    ax.text(x, y, s, fontsize=size, fontweight=weight, ha=ha, va=va, color=color,
            linespacing=1.25, family=family)


def line(ax, xs, ys, arrow=False):
    if arrow:
        ax.add_patch(FancyArrowPatch((xs[0], ys[0]), (xs[1], ys[1]), arrowstyle="-|>",
                                     mutation_scale=5, lw=0.6, color=INK, shrinkA=0,
                                     shrinkB=0))
    else:
        ax.plot(xs, ys, color=INK, lw=0.6, solid_capstyle="butt")


def bus(ax, x_from, ys_from, x_bus, x_to, ys_to):
    """Right-angle connector: lines from the sources to a vertical bus, arrows to the targets."""
    for y in ys_from:
        line(ax, [x_from, x_bus], [y, y])
    ys = list(ys_from) + list(ys_to)
    line(ax, [x_bus, x_bus], [min(ys), max(ys)])
    for y in ys_to:
        line(ax, [x_bus, x_to], [y, y], arrow=True)


def table(ax, x, y, w, h, name, head, present=True):
    """A Parquet view: a header with the view name over column stripes."""
    if not present:
        box(ax, x, y, w, h, fill="none", edge=MUTED, dashed=True, r=0.6)
        text(ax, x + w / 2, y + h / 2, name, size=5.5, ha="center", color=MUTED, family=MONO)
        return
    hh = 2.6
    box(ax, x, y, w, h, fill="white", edge=head, r=0.6)
    ax.add_patch(Rectangle((x, y + h - hh), w, hh, fc=head, ec=head, lw=0.5))
    text(ax, x + w / 2, y + h - hh / 2, name, size=5.5, ha="center", color="white",
         weight="bold", family=MONO)
    n = 5
    cw = (w - 1.2) / n
    for i in range(n):
        if i % 2 == 0:
            ax.add_patch(Rectangle((x + 0.6 + i * cw, y + 0.6), cw, h - hh - 1.2, fc=STRIPE,
                                   ec="none"))


def page(ax, x, y, w, h, label, present=True):
    """A file: a page with a folded corner and its name."""
    c = 1.4
    pts = [(x, y), (x + w, y), (x + w, y + h - c), (x + w - c, y + h), (x, y + h)]
    ax.add_patch(Polygon(pts, closed=True, fc="white" if present else "none",
                         ec=INK if present else MUTED, lw=0.5,
                         ls="-" if present else (0, (2, 1.2))))
    if present:
        ax.add_patch(Polygon([(x + w - c, y + h), (x + w - c, y + h - c), (x + w, y + h - c)],
                             closed=True, fc=RULE, ec=INK, lw=0.5))
    text(ax, x + w + 1, y + h / 2, label, size=5.5, color=INK if present else MUTED,
         family=MONO)


def window(ax, x, y, w, h, kind):
    """A browser or desktop window glyph."""
    box(ax, x, y, w, h, fill="white", edge=INK, r=0.5)
    bar = 1.5
    ax.add_patch(Rectangle((x, y + h - bar), w, bar, fc=RULE, ec=INK, lw=0.5))
    for i in range(3):
        ax.add_patch(plt.Circle((x + 0.8 + i * 0.9, y + h - bar / 2), 0.25, fc=INK, ec="none"))
    if kind == "browser":
        heights = [0.35, 0.6, 0.9, 0.5, 0.75]
        bw = (w - 2) / len(heights)
        for i, f in enumerate(heights):
            ax.add_patch(Rectangle((x + 1 + i * bw + 0.15, y + 0.7), bw - 0.3,
                                   f * (h - bar - 1.4), fc=MUTED, ec="none"))
    else:
        ax.add_patch(Rectangle((x, y), w * 0.3, h - bar, fc=STRIPE, ec=INK, lw=0.5))
        for i in range(3):
            yy = y + 0.9 + i * (h - bar - 1.4) / 2.5
            ax.plot([x + w * 0.38, x + w - 0.8], [yy, yy], color=MUTED, lw=0.6)


def code(ax, x, y, w, h, s):
    box(ax, x, y, w, h, fill=INK, edge=INK, r=0.5)
    text(ax, x + w / 2, y + h / 2, s, size=5, ha="center", color="white", family=MONO)


def corpus():
    df = load()
    check(df)
    latest = pd.read_csv(SNAPSHOT / "acquisition_latest.csv", usecols=["dataset", "subdir"])
    rows = pd.read_csv(SNAPSHOT / "corpus_datasets.csv", usecols=["dataset", "subdir",
                                                                  "psm_rows"])
    psms = latest.merge(rows, on=["dataset", "subdir"], validate="one_to_one")["psm_rows"].sum()
    held = presence()[0].any()
    return {"routes": df["route"].value_counts(), "datasets": len(df),
            "samples": int(df["sample_count"].sum()), "runs": int(df["run_count"].sum()),
            "psms": int(psms), "held": held}


def main():
    c = corpus()
    held = c["held"]
    fig = plt.figure(figsize=(DOUBLE, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    cols = [(2, 35), (43, 37), (86, 60), (150, 31)]
    heads = ["Public datasets", "Reprocessing", "QPX dataset", "Access"]
    for (x, w), head in zip(cols, heads):
        text(ax, x, H - 2.5, head, size=7, weight="bold", va="top")
        ax.plot([x, x + w], [H - 7.5, H - 7.5], color=RULE, lw=0.5)
    top, bottom = 80, 10  # extent of the boxes below the column headers

    # Column 1: repositories and sample annotation.
    x, w = cols[0]
    box(ax, x, 49, w, top - 49, fill=PANEL_FILL, edge=PANEL_FILL)
    text(ax, x + 2, top - 2.5, "Repositories", weight="bold", va="top")
    for i, name in enumerate(["PRIDE", "iProX", "MassIVE", "PDC"]):
        cx, cy = x + 2 + (i % 2) * 16, 68 - (i // 2) * 5.8
        box(ax, cx, cy, 15, 4.6, r=0.8)
        text(ax, cx + 7.5, cy + 2.3, name, size=5.5, ha="center")
    text(ax, x + 2, 59.6, "and other public studies", size=5.5, color=MUTED)
    for i in range(3):
        px = x + 2 + i * 1.3
        pts = [(px, 51), (px + 4.5, 51), (px + 4.5, 55.6), (px + 3.3, 56.8), (px, 56.8)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.5))
    text(ax, x + 11, 53.9, "raw MS files", size=5.5)

    box(ax, x, bottom, w, 45 - bottom, fill=PANEL_FILL, edge=PANEL_FILL)
    text(ax, x + 2, 42.5, "Sample annotation", weight="bold", va="top")
    tx, ty, tw, th = x + 2, 24, 20, 14
    ax.add_patch(Rectangle((tx, ty), tw, th, fc="white", ec=INK, lw=0.5))
    ax.add_patch(Rectangle((tx, ty + th - 2.6), tw, 2.6, fc=DATA_HEAD, ec=INK, lw=0.5))
    text(ax, tx + tw / 2, ty + th - 1.3, "SDRF-Proteomics", size=5, ha="center", color="white",
         weight="bold")
    for i in range(1, 4):
        ax.plot([tx + i * tw / 4] * 2, [ty, ty + th - 2.6], color=RULE, lw=0.4)
        ax.plot([tx, tx + tw], [ty + i * (th - 2.6) / 4] * 2, color=RULE, lw=0.4)
    text(ax, x + 2, 21.5, "Runs linked to samples,\nlabels and ontology terms", size=5.5,
         color=MUTED, va="top")

    # Column 2: one box per processing route, in the order of Table 3.
    x, w = cols[1]
    routes = {
        "ID only": ("quantms-msnet recipe", "Identification only"),
        "DIA-NN": ("quantmsdiann (DIA-NN)", "DIA, label-free"),
        "OpenMS": ("quantms (OpenMS)", "DDA, label-free and TMT"),
    }
    rh = 16
    ys = [top - rh, (top + bottom - rh) / 2, bottom]
    for route, y in zip(ROUTES, ys):
        name, sub = routes[route]
        box(ax, x, y, w, rh)
        ax.add_patch(Rectangle((x, y), 1.6, rh, fc=ROUTE_COLOURS[route], ec="none"))
        text(ax, x + 4, y + 10.6, name, weight="bold")
        text(ax, x + 4, y + 5.6, sub, size=5.5, color=MUTED)
        text(ax, x + w - 2.5, y + 10.6, f"{c['routes'][route]}", size=7, weight="bold",
             ha="right")
        text(ax, x + w - 2.5, y + 5.6, "datasets", size=5, color=MUTED, ha="right")
    bus(ax, cols[0][0] + cols[0][1], [64.5, 27.5], x - 3, x, [y + rh / 2 for y in ys])

    # Column 3: the dataset folder, its Parquet views and the columns that join them.
    x, w = cols[2]
    fy, fh = bottom + 6, top - bottom - 9.5
    ax.add_patch(Polygon([(x, fy + fh), (x, fy + fh + 3.2), (x + 18, fy + fh + 3.2),
                          (x + 20, fy + fh)], closed=True, fc=PANEL_FILL, ec=PANEL_FILL))
    text(ax, x + 2, fy + fh + 1.6, "{PREFIX}/", size=5.5, family=MONO)
    text(ax, x + w, fy + fh + 1.6, "one folder per dataset", size=5, color=MUTED, ha="right")
    box(ax, x, fy, w, fh, fill=PANEL_FILL, edge=PANEL_FILL)
    bus(ax, cols[1][0] + cols[1][1], [y + rh / 2 for y in ys], x - 3, x, [fy + fh / 2])

    tw, th, gap = 16, 8, 3
    gx = [x + gap + i * (tw + (w - 2 * gap - 3 * tw) / 2) for i in range(3)]
    row_a = fy + fh - 3 - th
    for name, gxi in zip(["psm", "feature", "pg"], gx):
        table(ax, gxi, row_a, tw, th, name, DATA_HEAD, held[name])
    trunk = row_a - 4
    for gxi in gx:
        line(ax, [gxi + tw / 2] * 2, [row_a, trunk])
    line(ax, [gx[0] + tw / 2, gx[2] + tw / 2], [trunk, trunk])
    for a, b, label in [(0, 1, "run_file_name"), (1, 2, "grouped_runs")]:
        text(ax, (gx[a] + gx[b] + tw) / 2, trunk + 1.8, label, size=5, ha="center",
             family=MONO, color=MUTED)
    row_b = trunk - 4 - th
    line(ax, [gx[1] + tw / 2] * 2, [trunk, row_b + th], arrow=True)
    table(ax, gx[1], row_b, tw, th, "run", META_HEAD)
    table(ax, gx[2], row_b, tw, th, "sample", META_HEAD)
    line(ax, [gx[1] + tw, gx[2]], [row_b + th / 2] * 2, arrow=True)
    text(ax, (gx[1] + tw + gx[2]) / 2, row_b - 1.8, "sample_accession", size=5, ha="center",
         family=MONO, color=MUTED)
    row_c = row_b - 4 - 7
    for name, gxi in zip(["dataset", "ontology", "provenance"], gx):
        table(ax, gxi, row_c, tw, 7, name, META_HEAD)
    row_d = row_c - 3 - 5.4
    for label, gxi in zip(["SDRF", ".h5mu", ".h5ad"], gx):
        page(ax, gxi + 1, row_d, 4.2, 5.4, label, held[label])

    others = ["pepmap", "protein", "site", "proteoform", "fragment", "xic", "mz"]
    ow, oh, og = (w - 2 * gap - 3 * 0.8) / 4, 3.8, 0.8
    for i, name in enumerate(others):
        bx = x + gap + (i % 4) * (ow + og)
        by = row_d - 3 - oh - (i // 4) * (oh + og)
        table(ax, bx, by, ow, oh, name, DATA_HEAD, held[name])

    # Key and corpus totals under the folder.
    ky = bottom + 2.6
    kx = x
    for kind, label in [("data", "data view"), ("meta", "metadata view"),
                        ("absent", "not in this corpus")]:
        if kind == "absent":
            box(ax, kx, ky - 1, 4, 2, fill="none", edge=MUTED, dashed=True, r=0.3)
        else:
            ax.add_patch(Rectangle((kx, ky - 1), 4, 2,
                                   fc=DATA_HEAD if kind == "data" else META_HEAD, ec="none"))
        text(ax, kx + 5, ky, label, size=5, color=MUTED)
        kx += 5 + 1.06 * len(label) + 3
    text(ax, x + w / 2, bottom - 4.5,
         f"{c['datasets']} datasets · {c['samples']:,} samples · {c['runs']:,} runs · "
         f"{c['psms'] / 1e6:,.0f} million PSMs", size=6, ha="center", weight="bold")

    # Column 4: ways to read the data.
    x, w = cols[3]
    access = [("QPX Explorer", "quantms portal", "browser"), ("QPX UI", "desktop viewer", "app"),
              ("SQL", "DuckDB and others", "sql"), ("Python", "qpx package", "python")]
    ah = 13
    step = (top - bottom - ah) / 3
    ay = [top - ah - i * step for i in range(4)]
    for (name, sub, kind), y in zip(access, ay):
        box(ax, x, y, w, ah)
        if kind in ("browser", "app"):
            window(ax, x + 2, y + 3.2, 8.5, 6.6, kind)
        else:
            code(ax, x + 2, y + 4.3, 8.5, 4.4, "SELECT" if kind == "sql" else ">>>")
        text(ax, x + 12.5, y + 8.2, name, weight="bold")
        text(ax, x + 12.5, y + 4.4, sub, size=5.5, color=MUTED)
    bus(ax, cols[2][0] + cols[2][1], [fy + fh / 2], x - 3, x, [y + ah / 2 for y in ay])

    save(fig, "fig1")


if __name__ == "__main__":
    main()
