"""Compare two versions of the same dataset, such as an older portal version and the deposited one.

For the psm, feature and pg views present in both version folders, it reports the target
records (for pg, the quantities, one per protein group, run or unit and label, so that the two
layouts are comparable), the distinct peptide sequences with charge (psm, feature) or protein groups (pg), the
Jaccard index of these sets, and, for feature and pg, the agreement of log2 intensities on the
shared keys: their Pearson correlation and the median absolute log2 ratio. Peptidoform strings
and row identifiers changed between specifications, so features are matched on sequence, charge,
run and label, summing the intensities of peptidoforms that share them, and protein groups on
their sorted accessions and label, summing over units. Both the older layout (one pg row per run
with nested intensities) and specification 1.3 (one pg row per unit and label) are read.

Run: python scripts/validation/compare_versions.py <old version folder> <new version folder>
     [--out data/validation/versions.csv]
"""

import argparse
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def files(folder, view):
    return sorted(str(p) for p in folder.glob(f"*.{view}.parquet"))


def columns(con, paths):
    return {r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_parquet({paths})").fetchall()}


def count(con, source):
    return con.execute(f"SELECT count(*) FROM ({source})").fetchall()[0][0]


def psm_keys(con, paths):
    source = f"SELECT sequence, charge FROM read_parquet({paths}) WHERE NOT is_decoy"
    return count(con, source), con.execute(f"SELECT DISTINCT * FROM ({source})").df(), None


def feature_keys(con, paths):
    source = f"""SELECT sequence, charge, run_file_name, intensities
                 FROM read_parquet({paths}) WHERE NOT is_decoy"""
    quant = con.execute(f"""
        SELECT sequence, charge, run_file_name, i.label AS label, sum(i.intensity) AS intensity
        FROM (SELECT sequence, charge, run_file_name, unnest(intensities) AS i FROM ({source}))
        GROUP BY ALL
    """).df()
    return count(con, source), quant[["sequence", "charge"]].drop_duplicates(), quant


def pg_keys(con, paths):
    if "grouped_runs" in columns(con, paths):
        source = f"SELECT pg_accessions, label, intensity FROM read_parquet({paths}) WHERE NOT is_decoy"
    else:
        source = f"""SELECT pg_accessions, i.label AS label, i.intensity AS intensity
                     FROM (SELECT pg_accessions, unnest(intensities) AS i
                           FROM read_parquet({paths}) WHERE NOT is_decoy)"""
    quant = con.execute(f"""
        SELECT array_to_string(list_sort(pg_accessions), ';') AS protein_group, label,
               sum(intensity) AS intensity
        FROM ({source}) GROUP BY ALL
    """).df()
    return count(con, source), quant[["protein_group"]].drop_duplicates(), quant


KEYS = {"psm": psm_keys, "feature": feature_keys, "pg": pg_keys}
COLUMNS = ["view", "old_records", "new_records", "old_keys", "new_keys", "jaccard",
           "matched_quantities", "log2_correlation", "median_abs_log2_ratio"]


def agreement(old, new):
    on = [c for c in old.columns if c != "intensity"]
    both = old.merge(new, on=on, suffixes=("_old", "_new"))
    both = both[(both["intensity_old"] > 0) & (both["intensity_new"] > 0)]
    ratio = np.log2(both["intensity_new"]) - np.log2(both["intensity_old"])
    return {"matched_quantities": len(both),
            "log2_correlation": np.corrcoef(np.log2(both["intensity_old"]),
                                            np.log2(both["intensity_new"]))[0, 1],
            "median_abs_log2_ratio": ratio.abs().median()}


def compare(con, old, new):
    rows = []
    for view, keys in KEYS.items():
        old_files, new_files = files(old, view), files(new, view)
        if not old_files or not new_files:
            continue
        (old_n, old_set, old_q), (new_n, new_set, new_q) = (keys(con, old_files),
                                                             keys(con, new_files))
        shared = len(old_set.merge(new_set))
        row = {"view": view, "old_records": old_n, "new_records": new_n,
               "old_keys": len(old_set), "new_keys": len(new_set),
               "jaccard": shared / (len(old_set) + len(new_set) - shared)}
        if old_q is not None:
            row |= agreement(old_q, new_q)
        rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "validation" / "versions.csv")
    args = parser.parse_args()

    result = compare(duckdb.connect(), args.old, args.new).assign(
        dataset=args.new.parent.name, old_version=args.old.name, new_version=args.new.name)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.out, mode="a", header=not args.out.exists(), index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
