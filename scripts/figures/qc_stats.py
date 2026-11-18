"""Per-run quality statistics of the corpus, computed from the QPX views (specification 1.3).

For every dataset folder listed in the selection table and present under --root it writes:

- qc_runs.csv: per run, the distinct target peptidoforms and the median precursor mass error
  (psm view; the feature view when a dataset has no psm view, as for DIA-NN), and
- qc_units.csv: per quantification unit (the grouped runs and the label), the protein groups
  with a quantity (pg view; datasets without a pg view have no rows), and
- qc_datasets.csv: per dataset, the protein groups quantified in any unit, the number of units
  and the completeness of the protein group x unit matrix.

Decoys are excluded. The pipelines export at different thresholds (1% or 5%), so rows are kept
at q <= 0.01 (psm.qvalue, feature.precursor_qvalue, pg.global_qvalue); rows without a q-value,
as in the identification-only route, are kept as exported. The mass error is computed from
observed_mz and calculated_mz, which every psm view has; DIA-NN has no psm view and no mass
error.

Run: python scripts/figures/qc_stats.py --root <corpus folder> [--out data/qc]
"""

import argparse
from pathlib import Path

import duckdb
import pandas as pd

from qpxfig import ROOT

SELECTION = ROOT / "data" / "portal-snapshot-2026-10-29" / "acquisition_latest.csv"


def view(folder, name):
    files = sorted(folder.glob(f"*.{name}.parquet"))
    return files[0] if files else None


def run_stats(con, folder):
    psm = view(folder, "psm")
    if psm is not None:
        return con.sql(f"""
            SELECT run_file_name, count(DISTINCT peptidoform) AS peptidoforms,
                   median(1e6 * (observed_mz - calculated_mz) / calculated_mz)
                       AS median_mass_error_ppm
            FROM read_parquet('{psm}')
            WHERE NOT is_decoy AND (qvalue IS NULL OR qvalue <= 0.01)
            GROUP BY run_file_name
        """).df().assign(source_view="psm")
    return con.sql(f"""
        SELECT run_file_name, count(DISTINCT peptidoform) AS peptidoforms
        FROM read_parquet('{view(folder, "feature")}')
        WHERE NOT is_decoy AND (precursor_qvalue IS NULL OR precursor_qvalue <= 0.01)
        GROUP BY run_file_name
    """).df().assign(source_view="feature")


def unit_stats(con, folder):
    pg = view(folder, "pg")
    if pg is None:
        return None, None
    con.sql(f"""
        CREATE OR REPLACE TEMP TABLE quantified AS
        SELECT DISTINCT list_sort(grouped_runs) AS grouped_runs, label, pg_group_id
        FROM read_parquet('{pg}')
        WHERE NOT is_decoy AND intensity IS NOT NULL
          AND (global_qvalue IS NULL OR global_qvalue <= 0.01)
    """)
    units = con.sql("""
        SELECT array_to_string(grouped_runs, ';') AS grouped_runs, label,
               count(*) AS protein_groups
        FROM quantified GROUP BY ALL
    """).df()
    groups = con.sql("SELECT count(DISTINCT pg_group_id) FROM quantified").fetchall()[0][0]
    cells = len(units) * groups
    summary = {"quantified_groups": groups, "units": len(units),
               "completeness": units["protein_groups"].sum() / cells}
    return units, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, required=True,
                        help="folder holding <dataset>/<ref> QPX folders")
    parser.add_argument("--selection", type=Path, default=SELECTION)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "qc")
    parser.add_argument("--threads", type=int, default=24)
    args = parser.parse_args()

    selection = pd.read_csv(args.selection)
    con = duckdb.connect()
    con.sql(f"SET threads={args.threads}")
    runs, units, datasets = [], [], []
    for row in selection.itertuples():
        folder = args.root / row.dataset / row.subdir
        if not folder.is_dir():
            continue
        keys = {"dataset": row.dataset, "subdir": row.subdir, "pipeline": row.pipeline}
        runs.append(run_stats(con, folder).assign(**keys))
        unit_table, summary = unit_stats(con, folder)
        if unit_table is not None:
            units.append(unit_table.assign(**keys))
            datasets.append({**keys, **summary})
        print(f"{row.dataset}/{row.subdir}: {len(runs[-1])} runs", flush=True)

    args.out.mkdir(parents=True, exist_ok=True)
    pd.concat(runs).to_csv(args.out / "qc_runs.csv", index=False)
    pd.concat(units).to_csv(args.out / "qc_units.csv", index=False)
    pd.DataFrame(datasets).to_csv(args.out / "qc_datasets.csv", index=False)
    print(f"{len(runs)} of {len(selection)} datasets, {sum(len(r) for r in runs)} runs")


if __name__ == "__main__":
    main()
