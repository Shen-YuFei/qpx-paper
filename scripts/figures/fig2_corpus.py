"""Figure 2: composition of the corpus.

Reads the corpus inventory and the public release dates of the datasets and plots the
datasets by repository, release year, organism, instrument, acquisition and size, coloured by
processing route. The totals are checked against Table 3 before plotting.

data/dataset_public_dates.csv (collected 17 November 2026) gives, per dataset, the hosting
repository and the date of the first public announcement in ProteomeCentral, or the release
recorded by MassIVE or the PDC (date_kind announced or publication), with its source. Rows
without such a date, including one dated only by its paper, count as having no date.

Run: python scripts/figures/fig2_corpus.py
"""

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

from qpxfig import (DOUBLE, MM, MUTED, ROOT, ROUTE_COLOURS, ROUTES, label_panels, log_axis,
                    route_strip, save)

SNAPSHOT = ROOT / "data" / "portal-snapshot-2026-10-29"
DATES = ROOT / "data" / "dataset_public_dates.csv"

# Table 3 totals and the acquisition counts given in the text; update together with them.
EXPECTED = {"datasets": 103, "samples": 23204, "runs": 51023,
            "routes": {"ID only": 57, "DIA-NN": 27, "OpenMS": 19},
            "acquisition": {"DDA": 60, "DIA": 24, "DDA and DIA": 4, "Not annotated": 15}}

PIPELINE_ROUTE = {"MSNet": "ID only", "DIA-NN": "DIA-NN", "OpenMS/quantms": "OpenMS"}

INSTRUMENT_FAMILY = {
    "Orbitrap Fusion": "Orbitrap Tribrid", "Orbitrap Fusion Lumos": "Orbitrap Tribrid",
    "Orbitrap Eclipse": "Orbitrap Tribrid",
    "Q Exactive": "Q Exactive", "Q Exactive Plus": "Q Exactive", "Q Exactive HF": "Q Exactive",
    "Q Exactive HF-X": "Q Exactive",
    "Orbitrap Exploris 480": "Orbitrap Exploris", "Orbitrap Astral": "Orbitrap Astral",
    "LTQ Orbitrap": "LTQ Orbitrap", "LTQ Orbitrap Velos": "LTQ Orbitrap",
    "LTQ Orbitrap Elite": "LTQ Orbitrap", "LTQ Orbitrap XL ETD": "LTQ Orbitrap",
    "Orbitrap": "Orbitrap, model not given",
    "timsTOF Pro": "timsTOF", "timsTOF HT": "timsTOF",
    "TripleTOF 5600": "TripleTOF", "TripleTOF 6600": "TripleTOF",
}

ACQUISITION = {"DDA label-free": "DDA, label-free", "DDA TMT": "DDA, TMT",
               "DDA TMT/label-free": "DDA, TMT and label-free", "DIA": "DIA",
               "mixed DDA/DIA": "DDA and DIA", "unknown": "Not annotated"}

SPECIES_SHOWN = ["Homo sapiens", "Mus musculus", "Escherichia coli"]


def load():
    acq = pd.read_csv(SNAPSHOT / "acquisition_latest.csv")
    inv = pd.read_csv(SNAPSHOT / "corpus_datasets.csv", usecols=["dataset", "subdir", "species",
                                                                 "instrument"])
    df = acq.merge(inv, on=["dataset", "subdir"], how="left", validate="one_to_one")
    dates = pd.read_csv(DATES, dtype=str)
    if set(dates["dataset"]) != set(df["dataset"]):
        raise SystemExit(f"{DATES.name} does not list the same datasets as the corpus")
    df = df.merge(dates[["dataset", "repository", "public_date", "date_kind"]], on="dataset",
                  how="left",
                  validate="one_to_one")
    df["route"] = df["pipeline"].map(PIPELINE_ROUTE)
    df["species"] = df["species"].map(json.loads)
    df["instrument"] = df["instrument"].map(json.loads)
    return df


def check(df):
    acq = df["acquisition_class"].map(lambda a: "DDA" if a.startswith("DDA") else
                                      ACQUISITION[a])
    got = {"datasets": len(df), "samples": int(df["sample_count"].sum()),
           "runs": int(df["run_count"].sum()),
           "routes": df["route"].value_counts().to_dict(),
           "acquisition": acq.value_counts().to_dict()}
    if got != EXPECTED:
        raise SystemExit(f"corpus totals differ from Table 3: {got}")


def organism(species):
    names = {s.split(" K-12")[0].strip().capitalize() for s in species}
    if names == {"Unknown"}:
        return "Not annotated"
    if len(names) > 1 or any(";" in s for s in species):
        return "Several species"
    name = names.pop()
    return name if name in SPECIES_SHOWN else "Other species"


def instrument(models):
    families = {INSTRUMENT_FAMILY[m] for m in models}
    return families.pop() if len(families) == 1 else "Several"


def stacked_barh(ax, df, column, order, italic=()):
    counts = df.groupby([column, "route"]).size().unstack(fill_value=0)
    counts = counts.reindex(index=order, columns=ROUTES, fill_value=0)
    y = np.arange(len(order))[::-1]
    left = np.zeros(len(order))
    for route in ROUTES:
        ax.barh(y, counts[route], left=left, height=0.72, color=ROUTE_COLOURS[route],
                edgecolor="white", linewidth=0.4)
        left += counts[route].to_numpy()
    for yi, total in zip(y, left):
        ax.text(total + left.max() * 0.015, yi, f"{int(total)}", va="center", fontsize=5.5,
                color=MUTED)
    ax.set_yticks(y, order)
    for label in ax.get_yticklabels():
        if label.get_text() in italic:
            label.set_fontstyle("italic")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, left.max() * 1.12)
    ax.set_xlabel("Datasets")


def by_count(series, last=()):
    order = [k for k in series.value_counts().index if k not in last]
    return order + [k for k in last if k in set(series)]


def main():
    df = load()
    check(df)
    df["organism"] = df["species"].map(organism)
    df["family"] = df["instrument"].map(instrument)
    df["acquisition"] = df["acquisition_class"].map(ACQUISITION)
    df["repo"] = df["repository"].fillna("Not identified")
    released = df["date_kind"].isin(["announced", "publication"])
    df["year"] = pd.to_numeric(df["public_date"].str[:4]).where(released)

    fig = plt.figure(figsize=(DOUBLE, 112 * MM))
    gs = fig.add_gridspec(2, 3, left=0.135, right=0.975, bottom=0.08, top=0.88, wspace=0.75,
                          hspace=0.55)
    axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(3)]

    stacked_barh(axes[0], df, "repo", by_count(df["repo"], last=["Not identified"]))

    ax = axes[1]
    years = np.arange(int(df["year"].min()), int(df["year"].max()) + 1)
    counts = df.groupby(["year", "route"]).size().unstack(fill_value=0)
    counts = counts.reindex(index=years, columns=ROUTES, fill_value=0)
    bottom = np.zeros(len(years))
    for route in ROUTES:
        ax.bar(years, counts[route], bottom=bottom, width=0.75, color=ROUTE_COLOURS[route],
               edgecolor="white", linewidth=0.4)
        bottom += counts[route].to_numpy()
    ax.set_xticks(years[::2])
    ax.set_xlabel("Year of public release")
    ax.set_ylabel("Datasets")
    undated = int(df["year"].isna().sum())
    if undated:
        ax.text(0.02, 0.98, f"No date: {undated}", transform=ax.transAxes, va="top",
                fontsize=5.5, color=MUTED)

    stacked_barh(axes[2], df, "organism",
                 by_count(df["organism"], last=["Other species", "Several species",
                                                  "Not annotated"]),
                 italic=SPECIES_SHOWN)

    stacked_barh(axes[3], df, "family",
                 by_count(df["family"], last=["Orbitrap, model not given", "Several"]))

    stacked_barh(axes[4], df, "acquisition",
                 ["DDA, label-free", "DDA, TMT", "DDA, TMT and label-free", "DIA",
                  "DDA and DIA", "Not annotated"])

    ax = axes[5]
    route_strip(ax, {r: g["run_count"] for r, g in df.groupby("route")})
    log_axis(ax, df["run_count"])
    ax.set_xlabel("Runs per dataset")

    handles = [Patch(color=ROUTE_COLOURS[r], label=r) for r in ROUTES]
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.0),
               title="Processing route", title_fontsize=6, handlelength=1.2,
               columnspacing=1.6, borderaxespad=0.4)
    label_panels(fig, axes, ["Repository", "Release year", "Organism", "Instrument",
                             "Acquisition and labelling (SDRF)", "Dataset size"])
    save(fig, "fig2")


if __name__ == "__main__":
    main()
