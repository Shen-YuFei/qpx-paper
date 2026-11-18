"""Quantification metrics per dataset version from the pg view.

For every dataset version folder under --root (<root>/<dataset>/<version>/) with a pg view:

- missingness.csv, after Webel et al. (2024): protein groups binned by the integer part of their
  median log2 intensity over the units that quantify them; per bin, the number of protein groups
  and the fraction of the protein group by unit matrix without a quantity (no row, or a null or
  zero intensity). A unit is a set of grouped runs and a label.
- replicates.csv, after Walzer et al. (2022): for samples quantified in more than one unit, the
  median over samples of the median coefficient of variation of the intensities of the protein
  groups quantified in every unit of the sample, and the median Pearson correlation of log2
  intensities over pairs of units of a sample, on the protein groups both units quantify (at
  least three).

Decoys are dropped and protein groups kept at a dataset-level q-value of 0.01; rows without a
q-value are kept as exported.

Run: python scripts/validation/quant_metrics.py --root <corpus folder> [--out data/validation]
"""

import argparse
from itertools import combinations
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def load(con, folder):
    pg = sorted(str(p) for p in folder.glob("*.pg.parquet"))
    run = sorted(str(p) for p in folder.glob("*.run.parquet"))
    return con.execute(f"""
        WITH channels AS (
            SELECT DISTINCT run_file_name, s.label, s.sample_accession
            FROM (SELECT run_file_name, unnest(samples) AS s FROM read_parquet({run}))
        )
        SELECT array_to_string(list_sort(pg.pg_accessions), ';') AS protein_group,
               array_to_string(pg.grouped_runs, ';') || '|' || pg.label AS unit,
               c.sample_accession, pg.intensity
        FROM read_parquet({pg}) AS pg
        LEFT JOIN channels AS c ON c.run_file_name = pg.grouped_runs[1] AND c.label = pg.label
        WHERE NOT pg.is_decoy AND coalesce(pg.global_qvalue <= 0.01, true)
    """).df()


def missingness(df):
    units = df["unit"].nunique()
    quantified = df[df["intensity"] > 0]
    median = np.log2(quantified.groupby("protein_group")["intensity"].median())
    cells = quantified.groupby("protein_group")["unit"].nunique()
    bins = pd.DataFrame({"bin": np.floor(median).astype(int), "cells": cells})
    out = bins.groupby("bin").agg(protein_groups=("cells", "size"), cells=("cells", "sum"))
    out["missing_fraction"] = 1 - out["cells"] / (out["protein_groups"] * units)
    return out.drop(columns="cells").reset_index().assign(units=units)


def replicates(df):
    quantified = df[(df["intensity"] > 0) & df["sample_accession"].notna()]
    cvs, correlations = [], []
    for _, sample in quantified.groupby("sample_accession"):
        matrix = sample.pivot_table(index="protein_group", columns="unit", values="intensity")
        if matrix.shape[1] < 2:
            continue
        shared = matrix.dropna()
        if len(shared):
            cvs.append((shared.std(axis=1) / shared.mean(axis=1)).median())
        logs = np.log2(matrix)
        correlations += [logs[a].corr(logs[b], min_periods=3)
                         for a, b in combinations(logs.columns, 2)]
    correlations = [r for r in correlations if not np.isnan(r)]
    return {"samples_with_replicates": len(cvs), "median_cv": np.median(cvs) if cvs else None,
            "median_correlation": np.median(correlations) if correlations else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "validation")
    args = parser.parse_args()

    con = duckdb.connect()
    missing, agreement = [], []
    for folder in sorted({p.parent for p in args.root.glob("*/*/*.pg.parquet")}):
        key = {"dataset": folder.parent.name, "version": folder.name}
        df = load(con, folder)
        missing.append(missingness(df).assign(**key))
        agreement.append(key | replicates(df))

    args.out.mkdir(parents=True, exist_ok=True)
    pd.concat(missing).to_csv(args.out / "missingness.csv", index=False)
    pd.DataFrame(agreement).to_csv(args.out / "replicates.csv", index=False)
    print(f"{args.out}: {len(agreement)} datasets")


if __name__ == "__main__":
    main()
