"""Supplementary Table 2: the columns of every QPX view, generated from the schema YAML files.

The schemas ship with the qpx package (qpx/core/data/schemas). Each view contributes one row per
field, in schema order, followed by the fields of the shared struct types (types.yaml) that
nested columns use. Required follows the specification: yes, the column must be present and
holds no nulls unless Nullable is yes; no, the column must be present and may hold nulls;
optional, the column may be left out of a file. Struct fields have no Required value; one that is
not nullable must not be null inside a non-null struct.

Run: python scripts/tables/data_dictionary.py [--schemas <dir>] [--out supplementary/data_dictionary.csv]
"""

import argparse
import importlib.resources
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]

# Order of Table 1: data views, then metadata views.
VIEWS = [
    "psm",
    "feature",
    "pg",
    "pepmap",
    "protein",
    "site",
    "proteoform",
    "fragment",
    "xic",
    "mz",
    "sample",
    "run",
    "dataset",
    "ontology",
    "provenance",
]


def required(spec):
    if spec.get("required"):
        return "yes"
    return "optional" if spec.get("optional") else "no"


def rows(table, fields, struct=False):
    for name, spec in fields.items():
        need = "" if struct else required(spec)
        yield {
            "table": table,
            "column": name,
            "type": spec["type"],
            "required": need,
            "nullable": ("yes" if spec.get("nullable") else "no")
            if need in ("yes", "")
            else "",
            "minimum": spec.get("minimum", ""),
            "maximum": spec.get("maximum", ""),
            "description": " ".join(str(spec.get("doc", "")).split()),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--schemas",
        type=Path,
        default=Path(
            str(importlib.resources.files("qpx") / "core" / "data" / "schemas")
        ),
    )
    parser.add_argument(
        "--out", type=Path, default=ROOT / "supplementary" / "data_dictionary.csv"
    )
    args = parser.parse_args()

    files = {p.stem: p for p in args.schemas.glob("*.yaml")}
    assert set(files) == set(VIEWS) | {"types"}, sorted(
        set(files) ^ (set(VIEWS) | {"types"})
    )
    out = []
    for view in VIEWS:
        out += rows(view, yaml.safe_load(files[view].read_text())["fields"])
    for name, struct in yaml.safe_load(files["types"].read_text()).items():
        out += rows(f"type {name}", struct["fields"], struct=True)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out).to_csv(args.out, index=False)
    print(f"{args.out}: {len(out)} rows from {args.schemas}")


if __name__ == "__main__":
    main()
