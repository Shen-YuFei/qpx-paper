"""Read one dataset version of the QPX corpus with DuckDB.

Shows three common steps and prints the first rows and the row count of each result:

1. protein-group quantities with the sample of each quantification unit and label
   (pg, run and sample views);
2. feature intensities joined to the sample annotations (feature, run and sample views);
3. the peptide folds recommended for machine learning in the Usage Notes (psm or feature view).

Identification-only datasets have no pg or feature view and give only the folds. Decoys are
dropped; protein groups are kept at a dataset-level q-value of 0.01 and features at a run-level
precursor q-value (else the peptide q-value) of 0.01. Rows without a q-value are kept as the
workflow exported them, as in Fig. 3.

Run: python examples/read_dataset.py <dataset version folder> [--max-qvalue 0.01]
"""

import argparse
import hashlib
from pathlib import Path

import duckdb


def fold(sequence):
    """Fold (0-9) of a peptide: MD5 of the upper-case sequence with I written as L, modulo 10."""
    digest = hashlib.md5(sequence.upper().replace("I", "L").encode("ascii")).hexdigest()
    return int(digest, 16) % 10


def register_views(con, folder):
    """Create one DuckDB view per QPX view; a view may be split into several files."""
    names = []
    for name in ("psm", "feature", "pg", "run", "sample"):
        files = [str(p) for p in sorted(folder.glob(f"*.{name}.parquet"))]
        if files:
            con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_parquet({files})")
            names.append(name)
    return names


# The sample of every run and label channel, from the run view.
CHANNELS = """
    channels AS (
        SELECT DISTINCT run_file_name, s.label, s.sample_accession
        FROM (SELECT run_file_name, unnest(samples) AS s FROM run)
    )
"""


def protein_groups(con, max_qvalue):
    """One row per protein group, quantification unit and label, with its sample."""
    return con.sql(f"""
        WITH {CHANNELS}
        SELECT c.sample_accession, pg.label, pg.grouped_runs,
               array_to_string(list_sort(pg.pg_accessions), ';') AS protein_group,
               pg.intensity
        FROM pg
        JOIN channels AS c ON c.run_file_name = pg.grouped_runs[1] AND c.label = pg.label
        WHERE NOT pg.is_decoy AND coalesce(pg.global_qvalue <= {max_qvalue}, true)
    """)


def feature_samples(con, max_qvalue):
    """One row per feature and label channel, with the sample and its annotations."""
    return con.sql(f"""
        WITH {CHANNELS},
        intensities AS (
            SELECT peptidoform, charge, run_file_name, unnest(intensities) AS i
            FROM feature
            WHERE NOT is_decoy
                AND coalesce(coalesce(precursor_qvalue, peptide_qvalue) <= {max_qvalue}, true)
        )
        SELECT f.peptidoform, f.charge, f.run_file_name, f.i.label AS label,
               f.i.intensity AS intensity, c.sample_accession,
               s.organism, s.organism_part, s.disease, s.cell_line
        FROM intensities AS f
        JOIN channels AS c ON c.run_file_name = f.run_file_name AND c.label = f.i.label
        JOIN sample AS s ON s.sample_accession = c.sample_accession
    """)


def peptide_folds(con, source):
    """The fold of every target peptide sequence of the psm or feature view."""
    con.create_function("peptide_fold", fold, ["VARCHAR"], "INTEGER")
    return con.sql(f"""
        SELECT sequence, peptide_fold(sequence) AS fold
        FROM (SELECT DISTINCT sequence FROM {source} WHERE NOT is_decoy)
    """)


def show(title, rel):
    print(f"## {title}: {rel.aggregate('count(*)').fetchall()[0][0]:,} rows")
    print(rel.limit(5).df().to_string(index=False), end="\n\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("folder", type=Path, help="dataset version folder")
    parser.add_argument("--max-qvalue", type=float, default=0.01)
    args = parser.parse_args()

    con = duckdb.connect()
    views = register_views(con, args.folder)
    if "pg" in views:
        show("protein groups by sample", protein_groups(con, args.max_qvalue))
    if "feature" in views:
        show("feature intensities by sample", feature_samples(con, args.max_qvalue))
    folds = peptide_folds(con, "psm" if "psm" in views else "feature")
    show("peptide folds", folds)
    print(folds.aggregate("fold, count(*) AS sequences", "fold").order("fold").df()
          .to_string(index=False))


if __name__ == "__main__":
    main()
