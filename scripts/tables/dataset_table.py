"""Supplementary Table 1: the datasets of the corpus, one row per dataset.

Combines the portal snapshot of 29 October 2026 (latest QPX version of each dataset), the
public release dates collected on 17 November 2026 and the dataset citations collected from the
repositories (data/dataset_citations.csv, written by fetch_dataset_citations.py). The totals are
checked against Table 3 before writing. Known issues are those found in the snapshot: conflicting
acquisition annotations and several QPX versions on the portal.

Run: python scripts/tables/dataset_table.py [--out supplementary/datasets.csv]
"""

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "data" / "portal-snapshot-2026-10-29"

# Table 3 totals: datasets, samples, runs, records in millions and size in GB, as printed.
EXPECTED = {"datasets": 103, "samples": 23204, "runs": 51023, "psm": 568.0, "feature": 435.3,
            "pg": 47.2, "gb": 1538}

ROUTE = {"MSNet": "ID only", "DIA-NN": "DIA-NN", "OpenMS/quantms": "OpenMS"}
ACQUISITION = {"DDA label-free": "DDA, label-free", "DDA TMT": "DDA, TMT",
               "DDA TMT/label-free": "DDA, TMT and label-free", "DIA": "DIA",
               "mixed DDA/DIA": "DDA and DIA", "unknown": "not annotated"}


def joined(values):
    return "; ".join(json.loads(values))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "supplementary" / "datasets.csv")
    args = parser.parse_args()

    acq = pd.read_csv(SNAPSHOT / "acquisition_latest.csv")
    inv = pd.read_csv(SNAPSHOT / "corpus_datasets.csv")
    files = pd.read_csv(SNAPSHOT / "corpus_files.csv", usecols=["dataset", "subdir", "filename"])
    dates = pd.read_csv(ROOT / "data" / "dataset_public_dates.csv", dtype=str)
    cites = pd.read_csv(ROOT / "data" / "dataset_citations.csv", dtype=str)

    df = acq.merge(inv, on=["dataset", "subdir"], how="left", validate="one_to_one",
                   suffixes=("", "_inv"))
    df = df.merge(dates, on="dataset", how="left", validate="one_to_one")
    cites = cites.rename(columns={"url": "data_citation"})
    df = df.merge(cites[["dataset", "data_citation", "publication_pmid", "publication_doi"]],
                  on="dataset", how="left", validate="one_to_one")
    versions = inv.groupby("dataset")["subdir"].nunique()
    sdrf = set(files.loc[files["filename"].str.endswith("sdrf.tsv"), "dataset"])

    issues = []
    for row in df.itertuples():
        found = []
        if isinstance(row.conflict, str):
            found.append(f"acquisition annotation: {row.conflict}")
        if versions[row.dataset] > 1:
            found.append(f"{versions[row.dataset]} QPX versions on the portal")
        issues.append("; ".join(found))

    out = pd.DataFrame({
        "dataset": df["dataset"],
        "accession": df["accession_used"],
        "repository": df["repository"],
        "data_citation": df["data_citation"],
        "route": df["pipeline"].map(ROUTE),
        "acquisition": df["acquisition_class"].map(ACQUISITION),
        "labelling": df["labeling"],
        "organism": df["species"].map(joined),
        "instrument": df["instrument"].map(joined),
        "samples": df["sample_count"],
        "runs": df["run_count"],
        "psm_records": df["psm_rows"].astype("Int64"),
        "feature_records": df["feature_rows"].astype("Int64"),
        "pg_records": df["pg_rows"].astype("Int64"),
        "size_gb": (df["total_size_bytes"] / 1e9).round(2),
        "qpx_version": df["qpx_version"].map(joined),
        "version_folder": df["subdir"],
        "sdrf_on_portal": df["dataset"].isin(sdrf).map({True: "yes", False: "no"}),
        "first_public_date": df["public_date"].where(
            df["date_kind"].isin(["announced", "publication"])),
        "publication_pmid": df["publication_pmid"],
        "publication_doi": df["publication_doi"],
        "known_issues": issues,
    }).sort_values(["route", "dataset"], key=lambda s: s.map(
        {"ID only": 0, "DIA-NN": 1, "OpenMS": 2}) if s.name == "route" else s)

    got = {"datasets": len(out), "samples": int(out["samples"].sum()),
           "runs": int(out["runs"].sum()),
           "psm": round(out["psm_records"].sum() / 1e6, 1),
           "feature": round(out["feature_records"].sum() / 1e6, 1),
           "pg": round(out["pg_records"].sum() / 1e6, 1),
           "gb": round(df["total_size_bytes"].sum() / 1e9)}
    if got != EXPECTED:
        raise SystemExit(f"totals differ from Table 3: {got}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(f"{args.out}: {len(out)} datasets")


if __name__ == "__main__":
    main()
