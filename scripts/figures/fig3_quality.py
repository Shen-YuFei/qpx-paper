"""Figure 3: identification and quantification statistics per dataset.

Plots the tables written by qc_stats.py: for each dataset the median over its runs (or
quantification units) of the identified peptidoforms, the quantified protein groups and the
precursor mass error, and the completeness of its protein group x unit matrix.

Run: python scripts/figures/fig3_quality.py [--qc data/qc]
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from qpxfig import DOUBLE, MM, ROOT, label_panels, log_axis, route_strip, save

ROUTE = {"MSNet": "ID only", "DIA-NN": "DIA-NN", "OpenMS/quantms": "OpenMS"}


def per_route(table, column):
    return {ROUTE[p]: g[column].dropna() for p, g in table.groupby("pipeline")}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--qc", type=Path, default=ROOT / "data" / "qc")
    args = parser.parse_args()

    runs = pd.read_csv(args.qc / "qc_runs.csv")
    units = pd.read_csv(args.qc / "qc_units.csv")
    datasets = pd.read_csv(args.qc / "qc_datasets.csv")
    keys = ["dataset", "subdir", "pipeline"]
    per_run = runs.groupby(keys)[["peptidoforms", "median_mass_error_ppm"]].median().reset_index()
    per_unit = units.groupby(keys)["protein_groups"].median().reset_index()
    datasets["completeness_pct"] = 100 * datasets["completeness"]
    print(f"{len(per_run)} datasets, {len(runs)} runs, {len(per_unit)} with protein quantities")

    fig = plt.figure(figsize=(DOUBLE, 52 * MM))
    gs = fig.add_gridspec(1, 4, left=0.075, right=0.975, bottom=0.22, top=0.84, wspace=0.24)
    axes = [fig.add_subplot(gs[0, i]) for i in range(4)]

    route_strip(axes[0], per_route(per_run, "peptidoforms"))
    route_strip(axes[1], per_route(per_unit, "protein_groups"), note="No quantities")
    route_strip(axes[2], per_route(datasets, "completeness_pct"), note="No quantities")
    route_strip(axes[3], per_route(per_run, "median_mass_error_ppm"), note="No psm view")

    log_axis(axes[0], per_run["peptidoforms"])
    log_axis(axes[1], per_unit["protein_groups"])
    axes[0].set_xlabel("Peptidoforms per run")
    axes[1].set_xlabel("Protein groups per unit")
    axes[2].set_xlim(0, 100)
    axes[2].set_xlabel("Matrix completeness (%)")
    axes[3].axvline(0, color="#bfbfbf", lw=0.5, zorder=1)
    axes[3].set_xlabel("Precursor mass error (ppm)")
    for ax in axes[1:]:
        ax.set_yticklabels([])

    label_panels(fig, axes, ["Identification", "Quantification", "Completeness",
                             "Mass accuracy"])
    save(fig, "fig3")


if __name__ == "__main__":
    main()
