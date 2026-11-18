"""Supplementary Figure 2: views and files held by each dataset in the portal snapshot.

One row per dataset, grouped by processing route; a filled cell marks a view or file present in
the latest QPX version of the dataset (for the SDRF, anywhere in the dataset folder). Views that
no dataset holds are kept as empty columns. The bottom row counts the datasets per column.

Run: python scripts/figures/figS2_coverage.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch

from qpxfig import DOUBLE, MM, MUTED, PANEL_FILL, ROOT, ROUTE_COLOURS, ROUTES, save

SNAPSHOT = ROOT / "data" / "portal-snapshot-2026-10-29"
ROUTE = {"MSNet": "ID only", "DIA-NN": "DIA-NN", "OpenMS/quantms": "OpenMS"}

DATA_VIEWS = ["psm", "feature", "pg", "pepmap", "protein", "site", "proteoform", "fragment",
              "xic", "mz"]
META_VIEWS = ["sample", "run", "dataset", "ontology", "provenance"]
FILES = {".h5mu": r"\.h5mu$", ".h5ad": r"\.h5ad$", "SDRF": r"sdrf\.tsv$",
         "provenance.json": r"(?:^|/)provenance\.json$"}
COLUMNS = DATA_VIEWS + META_VIEWS + list(FILES)


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
    n_rows, n_cols = table.shape
    rgb = np.ones((n_rows, n_cols, 3)) * to_rgb(PANEL_FILL)
    for i, dataset in enumerate(table.index):
        rgb[i, table.loc[dataset].to_numpy()] = to_rgb(ROUTE_COLOURS[route[dataset]])

    fig = plt.figure(figsize=(DOUBLE * 0.75, 232 * MM))
    ax = fig.add_axes([0.24, 0.035, 0.72, 0.87])
    ax.imshow(rgb, aspect="auto", interpolation="none",
              extent=(-0.5, n_cols - 0.5, n_rows - 0.5, -0.5))
    for x in np.arange(-0.5, n_cols):
        ax.axvline(x, color="white", linewidth=0.6)
    for y in np.arange(-0.5, n_rows):
        ax.axhline(y, color="white", linewidth=0.3)
    for x in (len(DATA_VIEWS) - 0.5, len(DATA_VIEWS) + len(META_VIEWS) - 0.5):
        ax.axvline(x, color="white", linewidth=2.5)

    ax.set_yticks(range(n_rows), table.index, fontsize=3.6)
    ax.set_xticks(range(n_cols), COLUMNS, rotation=90, fontsize=5.5)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=1.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for x, count in enumerate(table.sum().to_numpy()):
        ax.text(x, n_rows + 0.6, str(count), ha="center", va="top", fontsize=5, color=MUTED)
    ax.text(-0.7, n_rows + 0.6, "Datasets", ha="right", va="top", fontsize=5, color=MUTED)
    ax.set_ylim(n_rows + 2.2, -0.5)

    handles = [Patch(color=ROUTE_COLOURS[r], label=r) for r in ROUTES]
    handles.append(Patch(color=PANEL_FILL, label="Absent"))
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.01, 0.995), ncol=4,
               handlelength=1, handleheight=1, columnspacing=1.2, fontsize=6)
    save(fig, "figS2")


if __name__ == "__main__":
    main()
