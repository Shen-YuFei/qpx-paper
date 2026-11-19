"""Supplementary Figure 2: views and files held by each dataset in the portal snapshot.

One row per dataset, grouped by processing route; a filled cell marks a view or file present in
the latest QPX version of the dataset (for the SDRF, anywhere in the dataset folder). Views that
no dataset holds are kept as empty columns. The row under each route counts its datasets per
column.

Run: python scripts/figures/figS2_coverage.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch, Rectangle

from qpxfig import DOUBLE, INK, MM, MONO, MUTED, PANEL_FILL, ROOT, ROUTE_COLOURS, ROUTES, save

SNAPSHOT = ROOT / "data" / "portal-snapshot-2026-10-29"
ROUTE = {"MSNet": "ID only", "DIA-NN": "DIA-NN", "OpenMS/quantms": "OpenMS"}

DATA_VIEWS = ["psm", "feature", "pg", "pepmap", "protein", "site", "proteoform", "fragment",
              "xic", "mz"]
META_VIEWS = ["sample", "run", "dataset", "ontology", "provenance"]
FILES = {".h5mu": r"\.h5mu$", ".h5ad": r"\.h5ad$", "SDRF": r"sdrf\.tsv$",
         "provenance.json": r"(?:^|/)provenance\.json$"}
COLUMNS = DATA_VIEWS + META_VIEWS + list(FILES)
W = 183  # mm


def presence():
    acq = pd.read_csv(SNAPSHOT / "acquisition_latest.csv", usecols=["dataset", "subdir",
                                                                    "pipeline"])
    files = pd.read_csv(SNAPSHOT / "corpus_files.csv", usecols=["dataset", "subdir", "filename",
                                                                "view"])
    latest = files.merge(acq[["dataset", "subdir"]], on=["dataset", "subdir"])
    table = pd.DataFrame(False, index=acq["dataset"], columns=COLUMNS)
    for view, group in latest.dropna(subset=["view"]).groupby("view"):
        table.loc[group["dataset"].unique(), view] = True
    for column, pattern in FILES.items():
        source = files if column == "SDRF" else latest
        hits = source.loc[source["filename"].str.contains(pattern), "dataset"].unique()
        table.loc[table.index.intersection(hits), column] = True
    route = acq.set_index("dataset")["pipeline"].map(ROUTE)
    order = sorted(table.index, key=lambda d: (ROUTES.index(route[d]), d))
    return table.loc[order], route.loc[order]


def main():
    table, route = presence()
    groups = [DATA_VIEWS, META_VIEWS, list(FILES)]
    names = ["Data views", "Metadata views", "Files"]
    # Two blocks side by side: ID only on the left, DIA-NN and OpenMS on the right.
    blocks = [["ID only"], ["DIA-NN", "OpenMS"]]
    rh, label_w, group_gap, route_gap = 2.0, 16.5, 1.2, 3.0  # mm
    cw = (W / 2 - label_w - 3 - group_gap * (len(groups) - 1)) / len(COLUMNS)
    col_x = []
    x = label_w
    for group in groups:
        for _ in group:
            col_x.append(x)
            x += cw
        x += group_gap
    rows_needed = [sum(2 + (route == r).sum() for r in b) + route_gap * (len(b) - 1) / rh
                   for b in blocks]
    rows_needed[-1] += 1 + route_gap / rh  # the corpus total under the last block
    head_h = 31  # mm above the first row: legend, group names and column labels
    height = head_h + max(rows_needed) * rh + 2
    fig = plt.figure(figsize=(DOUBLE, height * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(height, 0)
    ax.axis("off")

    handles = [Patch(color=ROUTE_COLOURS[r], label=f"Present ({r})") for r in ROUTES]
    handles.append(Patch(color=PANEL_FILL, label="Absent"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(label_w / W, 1), ncol=4,
              handlelength=1, handleheight=1, columnspacing=1.6, borderaxespad=0.5,
              fontsize=6)

    for b, block in enumerate(blocks):
        x0 = b * W / 2
        top = head_h
        for group, name, start in zip(groups, names,
                                      np.cumsum([0] + [len(g) for g in groups[:-1]])):
            gx0, gx1 = x0 + col_x[start], x0 + col_x[start + len(group) - 1] + cw
            ax.text((gx0 + gx1) / 2, top - 20.5, name, ha="center", va="bottom", fontsize=6)
            ax.plot([gx0 + 0.2, gx1 - 0.2], [top - 19.8] * 2, color=INK, lw=0.5)
        for i, column in enumerate(COLUMNS):
            ax.text(x0 + col_x[i] + cw / 2, top - 1, column, rotation=90, ha="center",
                    va="bottom", fontsize=5.5, family=MONO)
        y = top
        for r in block:
            sub = table[route == r]
            ax.add_patch(Rectangle((x0 + 1, y + 0.45), 1.1, 1.1, fc=ROUTE_COLOURS[r],
                                   ec="none"))
            ax.text(x0 + 2.8, y + rh / 2, f"{r} · {len(sub)} datasets", va="center",
                    fontsize=6, fontweight="bold")
            y += rh
            for dataset, present in sub.iterrows():
                ax.text(x0 + label_w - 1, y + rh / 2, dataset, ha="right", va="center",
                        fontsize=5)
                for i, column in enumerate(COLUMNS):
                    ax.add_patch(Rectangle((x0 + col_x[i] + 0.15, y + 0.15), cw - 0.3,
                                           rh - 0.3, ec="none",
                                           fc=ROUTE_COLOURS[r] if present[column]
                                           else PANEL_FILL))
                y += rh
            ax.text(x0 + label_w - 1, y + rh / 2, "Datasets", ha="right", va="center",
                    fontsize=5, color=MUTED)
            for i, count in enumerate(sub.sum().to_numpy()):
                ax.text(x0 + col_x[i] + cw / 2, y + rh / 2, str(count), ha="center",
                        va="center", fontsize=5, color=MUTED)
            y += rh + route_gap
    ax.text(x0 + label_w - 1, y + rh / 2, f"All {len(table)} datasets", ha="right",
            va="center", fontsize=5, fontweight="bold")
    for i, count in enumerate(table.sum().to_numpy()):
        ax.text(x0 + col_x[i] + cw / 2, y + rh / 2, str(count), ha="center", va="center",
                fontsize=5, fontweight="bold")
    save(fig, "figS2")


if __name__ == "__main__":
    main()
