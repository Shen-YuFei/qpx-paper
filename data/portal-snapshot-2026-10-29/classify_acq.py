# Classify the acquisition method of the latest QPX version of each dataset
# from SDRF files, repository metadata and the QPX files themselves.
import collections
import csv
import io
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
CACHE = HERE / "acquisition_cache"


def latest_versions():
    rows = list(csv.DictReader(open(HERE / "corpus_datasets.csv")))
    by = collections.defaultdict(list)
    for r in rows:
        by[r["dataset"]].append(r)
    return {ds: max(v, key=lambda r: max(json.loads(r["creation_dates"]))) for ds, v in by.items()}


def cached_bodies():
    bodies = {}
    for meta in CACHE.glob("*.json"):
        info = json.loads(meta.read_text())
        bin_path = meta.with_suffix(".bin")
        if info.get("status") == 200 and bin_path.exists():
            bodies[info["url"]] = bin_path.read_bytes()
    return bodies


def sdrf_evidence(text):
    df = pd.read_csv(io.StringIO(text), sep="\t", dtype=str).fillna("")
    cols = {c.strip().lower(): c for c in df.columns}

    def values(name):
        col = cols.get(name)
        return sorted(set(df[col])) if col else []

    immuno = []
    for low, col in cols.items():
        vals = " ".join(set(df[col])).lower()
        if any(t in low for t in ("mhc", "hla", "immunopeptid")) or (
            "enrichment" in low and any(t in vals for t in ("mhc", "hla"))
        ):
            immuno.append(f"{col}={sorted(set(df[col]))[:3]}")
    return {
        "acq": values("comment[proteomics data acquisition method]"),
        "label": values("comment[label]"),
        "immuno": immuno,
    }


def acq_from_text(values):
    text = " ".join(values).lower()
    found = set()
    if "independent" in text or "dia" in text.split() or "swath" in text:
        found.add("DIA")
    if "data-dependent" in text or "data dependent" in text or "dda" in text.split():
        found.add("DDA")
    return found


def labeling_from(values):
    text = " ".join(values).lower()
    found = set()
    if "tmt" in text:
        found.add("TMT")
    if "itraq" in text:
        found.add("iTRAQ")
    if "label free" in text or "label-free" in text:
        found.add("label-free")
    return found


def main():
    latest = latest_versions()
    bodies = cached_bodies()
    sources = json.load(open(HERE / "acquisition_sources.json"))
    by_ds = collections.defaultdict(list)
    for s in sources:
        by_ds[s["dataset"]].append(s)

    out = []
    for ds, row in sorted(latest.items()):
        sdrf_acq, sdrf_label, immuno, notes = set(), set(), [], []
        for s in by_ds[ds]:
            if s["kind"] == "local_sdrf":
                text = Path(s["path"]).read_text(errors="replace")
            elif s["kind"] == "remote_sdrf" and s["url"] in bodies:
                text = bodies[s["url"]].decode(errors="replace")
            else:
                continue
            ev = sdrf_evidence(text)
            sdrf_acq |= acq_from_text(ev["acq"])
            sdrf_label |= labeling_from(ev["label"])
            immuno += ev["immuno"]
            if ev["acq"]:
                notes.append(f"{s['kind']}: acq={ev['acq'][:2]}")
        pride_acq, pride_quant = set(), set()
        for s in by_ds[ds]:
            if s["kind"] == "pride_api" and s.get("http", {}).get("status") == 200:
                exp = [e["name"] for e in s["data"].get("experimentTypes") or []]
                quant = [q["name"] for q in s["data"].get("quantificationMethods") or []]
                pride_acq |= acq_from_text(exp)
                pride_quant |= labeling_from(quant)
                notes.append(f"pride: exp={exp} quant={quant}")
        qpx_class = row["acquisition_class"]
        qpx_acq = {"DIA"} if qpx_class == "DIA" else {"DDA"} if qpx_class.startswith("DDA") else set()
        qpx_label = set(json.loads(row["labeling_types"] or "[]"))

        acq = sdrf_acq or qpx_acq or pride_acq
        acq_source = "sdrf" if sdrf_acq else "qpx" if qpx_acq else "pride" if pride_acq else ""
        conflict = []
        for name, other in (("qpx", qpx_acq), ("pride", pride_acq)):
            if other and acq and other != acq:
                conflict.append(f"acq {acq_source}={sorted(acq)} vs {name}={sorted(other)}")
        label = sdrf_label or qpx_label
        if len(acq) == 1:
            (a,) = acq
            if a == "DIA":
                cls = "DIA"
            else:
                cls = "DDA " + ("/".join(sorted(label)) if label else "unknown labelling")
        else:
            cls = "unknown" if not acq else "mixed " + "/".join(sorted(acq))
        out.append(
            {
                "dataset": ds,
                "subdir": row["subdir"],
                "acquisition_class": cls,
                "acq_source": acq_source,
                "labeling": "/".join(sorted(label)),
                "immunopeptidomics_evidence": "; ".join(sorted(set(immuno)))[:300],
                "conflict": "; ".join(conflict),
                "creator": row["creator"],
                "pipeline": "MSNet" if "MSNet" in row["pipeline_versions"] else "DIA-NN" if "DIA-NN" in row["pipeline_versions"] else "OpenMS/quantms",
                "sample_count": row["sample_count"],
                "run_count": row["run_count"],
                "notes": " | ".join(notes)[:500],
            }
        )

    with open(HERE / "acquisition_latest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    return out


if __name__ == "__main__":
    rows = main()
    print(collections.Counter(r["acquisition_class"] for r in rows).most_common())
    print(collections.Counter((r["pipeline"], r["acquisition_class"]) for r in rows).most_common())
    print(collections.Counter(r["acq_source"] for r in rows))
    print("conflicts", sum(1 for r in rows if r["conflict"]))
    print("immuno evidence", [(r["dataset"], r["immunopeptidomics_evidence"][:120]) for r in rows if r["immunopeptidomics_evidence"]])
