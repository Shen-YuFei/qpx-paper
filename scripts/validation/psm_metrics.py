"""PSM-level validation metrics per dataset version, after Wen and Noble (2024).

For every dataset version folder under --root (<root>/<dataset>/<version>/) with a psm view:

- psm_qvalue_curve.csv: the number of target PSMs at or below each q-value threshold, up to the
  highest q-value in the view, for views whose PSMs carry q-values (the workflows export PSMs
  at their own threshold, so the curve stops there);
- psm_fragment_tic.csv: over a random sample of target PSMs with peak arrays, the fraction of the
  MS2 ion current in peaks annotated as b or y ions (neutral losses included), summarised by its
  quartiles.

The acceptance rate of Wen and Noble (accepted PSMs over all MS2 spectra) needs the number of MS2
spectra per run, which the views do not record, and is not computed.

Run: python scripts/validation/psm_metrics.py --root <corpus folder> [--out data/validation]
"""

import argparse
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
THRESHOLDS = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
SAMPLE_PSMS = 20000


def qvalue_curve(con, files):
    top = con.execute(f"SELECT max(qvalue) FROM read_parquet({files}) WHERE NOT is_decoy"
                      ).fetchall()[0][0]
    if top is None:
        return []
    cuts = [t for t in THRESHOLDS if t <= top] + [top]
    counts = con.execute(f"""
        SELECT {", ".join(f"count(*) FILTER (WHERE qvalue <= {t})" for t in cuts)}
        FROM read_parquet({files}) WHERE NOT is_decoy
    """).fetchall()[0]
    return [{"qvalue": t, "target_psms": n} for t, n in zip(cuts, counts)]


def fragment_tic(con, files):
    return con.execute(f"""
        WITH sampled AS (
            SELECT row_number() OVER () AS k, intensity_array, ion_type_array
            FROM (SELECT intensity_array, ion_type_array FROM read_parquet({files})
                  WHERE NOT is_decoy AND intensity_array IS NOT NULL
                    AND ion_type_array IS NOT NULL)
            USING SAMPLE reservoir({SAMPLE_PSMS} ROWS) REPEATABLE (1)
        ),
        peaks AS (
            SELECT k, unnest(intensity_array) AS intensity, unnest(ion_type_array) AS ion
            FROM sampled
        ),
        psms AS (
            SELECT k, sum(intensity) FILTER (WHERE regexp_matches(ion, '^[by][0-9]'))
                      / sum(intensity) AS by_fraction
            FROM peaks GROUP BY k
        )
        SELECT count(*), quantile_cont(coalesce(by_fraction, 0), [0.25, 0.5, 0.75])
        FROM psms
    """).fetchall()[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "validation")
    args = parser.parse_args()

    con = duckdb.connect()
    curves, tics = [], []
    for folder in sorted(p.parent for p in args.root.glob("*/*/*.psm.parquet")):
        files = sorted({str(p) for p in folder.glob("*.psm.parquet")})
        key = {"dataset": folder.parent.name, "version": folder.name}
        curves += [key | row for row in qvalue_curve(con, files)]
        n, quartiles = fragment_tic(con, files)
        if n:
            q1, median, q3 = quartiles
            tics.append(key | {"psms_sampled": n, "by_fraction_q1": q1,
                               "by_fraction_median": median, "by_fraction_q3": q3})

    args.out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(curves).to_csv(args.out / "psm_qvalue_curve.csv", index=False)
    pd.DataFrame(tics).to_csv(args.out / "psm_fragment_tic.csv", index=False)
    print(f"{args.out}: {len(curves)} curve points, {len(tics)} datasets with peak arrays")


if __name__ == "__main__":
    main()
