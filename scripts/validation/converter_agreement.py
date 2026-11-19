"""Compare public proteomics reports with QPX conversions of the same inputs.

Run with Bigbio on PATH. The manifest lists the local paths and provenance of
the inputs. By default the script writes fresh conversions beside the inputs.
Use --reuse-qpx to check existing conversions, including the OpenMS benchmark.
Source parsing uses pandas, DuckDB and ElementTree without importing QPX.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict
from functools import cache
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/validation/sources.csv"
RESULT = ROOT / "data/validation/converter_agreement.csv"
FIELDS = (
    "converter",
    "accession",
    "view",
    "quantity",
    "source_value",
    "qpx_value",
    "matched",
    "only_source",
    "only_qpx",
    "max_rel_diff",
    "note",
)
RTOL = 1e-6
PEPTIDE = ["peptidoform", "charge"]
FEATURE = [*PEPTIDE, "run"]
PROTEIN = ["accessions", "runs"]
UNIMOD = {"Acetyl": 1, "Carbamidomethyl": 4, "Oxidation": 35, "TMT6plex": 737}
NAMED_MOD = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
DIANN_QVALUE = 0.01


def read_tsv(path, columns=None):
    return pd.read_csv(path, sep="\t", usecols=columns, low_memory=False)


def run_stem(raw):
    return re.sub(
        r"\.(?:mzML|raw|d)(?:\.gz)?$",
        "",
        str(raw).replace("\\", "/").rsplit("/", 1)[-1],
        flags=re.I,
    )


def accessions(values):
    members = set()
    for value in values:
        if not value:
            continue
        match = re.fullmatch(r"(?:sp|tr)\|([^|]+)\|[^|]+", value)
        members.add(match[1] if match else value)
    return ";".join(sorted(members))


def protein_sets(cells):
    return cells.fillna("").map(lambda value: accessions(re.split(r"[;,]\s*", value)))


@cache
def openms_peptide(value):
    """Translate the named OpenMS modifications occurring in the two quantms exports."""

    def modification(match):
        name = match[1]
        unimod = (
            name.split(":")[1] if name.upper().startswith("UNIMOD:") else UNIMOD[name]
        )
        return f"[UNIMOD:{unimod}]"

    value = NAMED_MOD.sub(modification, value)
    value = re.sub(r"^\.?(\[[^]]+\])", r"\1-", value)
    return re.sub(r"\.(\[[^]]+\])$", r"-\1", value)


def parquet(directory, view, columns):
    return pd.read_parquet(directory / f"bench.{view}.parquet", columns=columns)


def qpx_features(directory, extra=()):
    return parquet(
        directory,
        "feature",
        ["peptidoform", "charge", "run_file_name", "intensities", *extra],
    ).rename(columns={"run_file_name": "run"})


def qpx_psms(directory, extra=()):
    table = parquet(
        directory, "psm", ["peptidoform", "charge", "run_file_name", "scan", *extra]
    )
    table["scan"] = table["scan"].map(lambda v: tuple(v))
    return table.rename(columns={"run_file_name": "run"})


def qpx_proteins(directory, extra=()):
    table = parquet(
        directory, "pg", ["pg_accessions", "grouped_runs", "label", "intensity", *extra]
    )
    table["accessions"] = table.pop("pg_accessions").map(accessions)
    table["runs"] = table.pop("grouped_runs").map(lambda runs: ";".join(sorted(runs)))
    return table


def channel_rows(table):
    flat = table.explode("intensities", ignore_index=True)
    values = pd.DataFrame(flat.pop("intensities").tolist(), index=flat.index)
    return flat.join(values)


def examples(frame, columns, limit=2):
    return (
        str(frame.sort_values(columns).loc[:, columns].head(limit).to_dict("records"))
        if len(frame)
        else ""
    )


class Agreement:
    def __init__(self, converter, accession):
        self.converter = converter
        self.accession = accession
        self.rows = []

    def add(self, view, quantity, source=None, qpx=None, *, note="", **counts):
        self.rows.append(
            {
                "converter": self.converter,
                "accession": self.accession,
                "view": view,
                "quantity": quantity,
                "source_value": source,
                "qpx_value": qpx,
                "note": note,
                **counts,
            }
        )

    def keys(self, view, quantity, source, qpx, key, note=""):
        """Count overlapping row occurrences, including repeated natural keys."""
        left = source.value_counts(key, dropna=False, sort=False).rename("source")
        right = qpx.value_counts(key, dropna=False, sort=False).rename("qpx")
        counts = pd.concat([left, right], axis=1).fillna(0).reset_index()
        source_only = counts["source"].gt(counts["qpx"])
        qpx_only = counts["qpx"].gt(counts["source"])
        self.add(
            view,
            quantity,
            len(source),
            len(qpx),
            matched=int(counts[["source", "qpx"]].min(axis=1).sum()),
            only_source=int((counts["source"] - counts["qpx"]).clip(lower=0).sum()),
            only_qpx=int((counts["qpx"] - counts["source"]).clip(lower=0).sum()),
            note=" ".join(
                filter(
                    None,
                    [
                        note,
                        f"Source examples {examples(counts[source_only], key)}."
                        if source_only.any()
                        else "",
                        f"QPX examples {examples(counts[qpx_only], key)}."
                        if qpx_only.any()
                        else "",
                    ],
                )
            ),
        )

    def identities(self, view, source, qpx):
        for quantity, key in (
            ("peptidoforms", ["peptidoform"]),
            ("precursors", PEPTIDE),
        ):
            self.keys(
                view,
                quantity,
                source[key].drop_duplicates(),
                qpx[key].drop_duplicates(),
                key,
            )

    def intensities(self, view, source, qpx, key, note=""):
        """Pair quantities at unique natural keys and report any ambiguous keys."""
        cols = [*key, "intensity"]
        left = source[cols].dropna(subset=["intensity"])
        right = qpx[cols].dropna(subset=["intensity"])
        self.keys(view, "quantified_keys", left, right, key, note)
        left_dupes = left.duplicated(key, keep=False)
        right_dupes = right.duplicated(key, keep=False)
        ambiguous = pd.concat(
            [left.loc[left_dupes, key], right.loc[right_dupes, key]]
        ).drop_duplicates()
        if len(ambiguous):
            self.add(
                view,
                "ambiguous_intensity_keys",
                int(left_dupes.sum()),
                int(right_dupes.sum()),
                note="Counts rows with repeated complete keys. Those keys prevent unique per-row pairing. "
                f"Examples {examples(ambiguous, key)}.",
            )
            left = left.merge(ambiguous.assign(ambiguous=True), on=key, how="left").loc[
                lambda f: f["ambiguous"].isna()
            ]
            right = right.merge(
                ambiguous.assign(ambiguous=True), on=key, how="left"
            ).loc[lambda f: f["ambiguous"].isna()]
        pairs = left.merge(
            right, on=key, suffixes=("_source", "_qpx"), validate="one_to_one"
        )
        delta = (pairs["intensity_qpx"] - pairs["intensity_source"]).abs()
        magnitude = pairs["intensity_source"].abs()
        relative = delta.div(magnitude.where(magnitude.ne(0), 1)).mask(
            magnitude.eq(0) & delta.ne(0), np.inf
        )
        different = relative.gt(RTOL)
        self.add(
            view,
            "intensity_mismatches",
            qpx=int(different.sum()) if len(pairs) else None,
            matched=len(pairs),
            max_rel_diff=relative.max() if len(relative) else None,
            note=f"Threshold {RTOL:g} relative to source. {note}".rstrip()
            + (
                f" Examples {examples(pairs[different], [*key, 'intensity_source', 'intensity_qpx'])}."
                if different.any()
                else ""
            ),
        )


def msstats_source(path, sdrf_path):
    msstats = pd.read_csv(path)
    sdrf = read_tsv(sdrf_path, ["comment[data file]", "comment[label]"])
    msstats["run"] = msstats["Reference"].str.split(".mzML", regex=False).str[0]
    msstats["peptidoform"] = msstats["PeptideSequence"].map(openms_peptide)
    msstats["intensity"] = msstats["Intensity"]
    if "Channel" in msstats:
        sdrf["run"] = sdrf["comment[data file]"].map(run_stem)
        # PXD014145's SDRF orders each plex by increasing reporter mass (N before C).
        channels = sdrf[["run", "comment[label]"]].drop_duplicates()
        channels["Channel"] = channels.groupby("run").cumcount() + 1
        msstats = msstats.merge(channels, on=["run", "Channel"], validate="many_to_one")
        msstats["label"] = msstats["comment[label]"]
        msstats["rt"] = msstats["RetentionTime"].astype("float32")
        msstats["scan"] = (
            msstats["Reference"]
            .str.extract(r"scan=(\d+)")[0]
            .astype(int)
            .map(lambda n: (n,))
        )
    else:
        msstats = msstats.rename(columns={"PrecursorCharge": "Charge"})
        msstats["label"] = "LFQ"
    return msstats.rename(columns={"Charge": "charge"})


def check_msstats(audit, inputs, output):
    source = msstats_source(inputs["msstats"], inputs["sdrf"])
    extra = ["rt", "scan"] if "Channel" in source else []
    qpx = qpx_features(output, extra)
    if extra:
        qpx["scan"] = qpx["scan"].map(tuple)
    key = [*FEATURE, *extra]
    features = source.drop_duplicates(key)
    note = "As exported by quantms. One feature per run, peptidoform, charge, and available peak coordinates."
    input_note = (
        "One MSstats row per TMT reporter channel."
        if extra
        else "One MSstats row per LFQ precursor and run."
    )
    audit.add("feature", "input_rows", len(source), len(qpx), note=input_note)
    audit.keys("feature", "feature_rows", features, qpx, key, note)
    audit.identities("feature", features, qpx)
    converted = channel_rows(qpx)
    zero = source["intensity"].eq(0)
    audit.add(
        "feature",
        "zero_intensities",
        int(zero.sum()),
        int(converted["intensity"].eq(0).sum()),
        note=f"MSstats zeros remain numeric. Source examples {examples(source[zero], [*key, 'label', 'intensity'])}.",
    )
    audit.intensities(
        "feature",
        source,
        converted,
        [*key, "label"],
        "Zero intensities are retained for MSstats.",
    )


def user_params(node):
    return {p.attrib["name"]: p.attrib["value"] for p in node.findall("UserParam")}


def xml_entities(path):
    """Keep one logical XML record in memory at a time."""
    stack = []
    names = {
        "IdentificationRun",
        "map",
        "UnassignedPeptideIdentification",
        "consensusElement",
    }
    for event, elem in ET.iterparse(path, events=("start", "end")):
        if event == "start":
            stack.append(elem)
            continue
        stack.pop()
        if elem.tag in names:
            yield elem
            stack[-1].remove(elem)


def xml_groups(protein_id):
    hits = {
        p.attrib["id"]: p.attrib["accession"] for p in protein_id.findall("ProteinHit")
    }
    groups = [
        [hits[ref] for ref in value.split(",")[1:]]
        for key, value in user_params(protein_id).items()
        if re.fullmatch(r"indistinguishable_proteins_\d+", key)
    ]
    covered = {protein for group in groups for protein in group}
    groups.extend([protein] for protein in hits.values() if protein not in covered)
    return {accessions(group) for group in groups}


def xml_psms(pid, run):
    scan = re.search(r"\bscan=(\d+)", pid.attrib.get("spectrum_reference", ""))
    if not scan:
        return []
    return [
        (
            openms_peptide(hit.attrib["sequence"]),
            int(hit.attrib["charge"]),
            run,
            (int(scan[1]),),
        )
        for hit in pid.findall("PeptideHit")
    ]


def openms_source(path):
    maps, origin = {}, {}
    groups, psms, features = set(), [], []
    for elem in xml_entities(path):
        if elem.tag == "IdentificationRun":
            protein = elem.find("ProteinIdentification")
            origin[elem.attrib["id"]] = [
                run_stem(name)
                for name in user_params(protein)["spectra_data"].strip("[]").split(",")
            ]
            groups.update(xml_groups(protein))
        elif elem.tag == "map":
            maps[int(elem.attrib["id"])] = run_stem(elem.attrib["name"])
        elif elem.tag == "UnassignedPeptideIdentification":
            idx = int(user_params(elem)["id_merge_index"])
            psms.extend(
                xml_psms(elem, origin[elem.attrib["identification_run_ref"]][idx])
            )
        else:
            pids = elem.findall("PeptideIdentification")
            for pid in pids:
                idx = int(user_params(pid)["map_index"])
                psms.extend(xml_psms(pid, maps[idx]))
            hit = pids[0].find("PeptideHit") if pids else None
            if hit is None:
                continue
            peptide = openms_peptide(hit.attrib["sequence"])
            charge = int(elem.attrib["charge"]) or int(hit.attrib["charge"])
            centroid = elem.find("centroid").attrib
            for sub in elem.findall("./groupedElementList/element"):
                a = sub.attrib
                features.append(
                    (
                        peptide,
                        charge,
                        maps[int(a["map"])],
                        np.float32(a["rt"]),
                        np.float32(centroid["mz"]),
                        np.float32(centroid["rt"]),
                        "LFQ",
                        float(a["it"]),
                        elem.attrib["id"],
                    )
                )
    return (
        pd.DataFrame(psms, columns=[*FEATURE, "scan"]),
        pd.DataFrame(
            features,
            columns=[
                *FEATURE,
                "rt",
                "observed_mz",
                "consensus_rt",
                "label",
                "intensity",
                "xml_feature",
            ],
        ),
        pd.DataFrame({"accessions": sorted(groups)}),
    )


def check_openms(audit, inputs, output):
    psms, features, groups = openms_source(inputs["consensusxml"])
    converted = qpx_psms(output)
    key = [*FEATURE, "scan"]
    unique = psms.drop_duplicates(key)
    audit.add(
        "psm",
        "input_hits_with_scan",
        len(psms),
        len(converted),
        note="Includes assigned and unassigned PeptideHits.",
    )
    audit.keys(
        "psm",
        "psm_rows",
        unique,
        converted,
        key,
        "Distinct spectrum, peptidoform and charge per run.",
    )
    audit.identities("psm", unique, converted)

    coordinates = ["rt", "observed_mz", "consensus_rt"]
    key = [*FEATURE, *coordinates]
    positive = features[features["intensity"].gt(0)]
    peaks = positive.drop_duplicates([*FEATURE, "rt", "intensity"])
    converted = qpx_features(output, coordinates)
    audit.add("feature", "input_identified_elements", len(features), len(converted))
    audit.keys(
        "feature",
        "feature_rows",
        peaks,
        converted,
        key,
        "Positive sub-feature intensities in identified consensus elements. Identical measured peaks counted once.",
    )
    audit.identities("feature", peaks, converted)
    audit.intensities("feature", peaks, channel_rows(converted), [*key, "label"])

    converted = qpx_proteins(output)
    audit.keys(
        "pg",
        "protein_groups",
        groups,
        converted[["accessions"]].drop_duplicates(),
        ["accessions"],
        "XML indistinguishable protein groups plus ungrouped hits. QPX exports groups with attributable run evidence.",
    )
    audit.add(
        "pg",
        "intensity_comparison",
        qpx=len(converted),
        note="This consensusXML has no fraction-group protein abundances. QPX computes its protein intensities from unique-peptide feature sums.",
    )


FRAGPIPE_MASSES = {"57.0215": 4, "15.9949": 35, "42.0106": 1}


@cache
def fragpipe_peptide(sequence, mods):
    nterm = ""
    residues = list(sequence)
    for token in mods.split(",") if mods else []:
        token = token.strip()
        position, mass = token.split("(")
        tag = f"[UNIMOD:{FRAGPIPE_MASSES[mass[:-1]]}]"
        if position == "N-term":
            nterm += f"{tag}-"
        else:
            residues[int(position[:-1]) - 1] += tag
    return nterm + "".join(residues)


def assigned_peptides(table, sequence):
    return [
        fragpipe_peptide(peptide, mods)
        for peptide, mods in zip(
            table[sequence], table["Assigned Modifications"].fillna(""), strict=True
        )
    ]


def fragpipe_experiments(path):
    annotation = read_tsv(path)
    annotation["run"] = annotation["file"].map(run_stem)
    return (
        annotation.groupby("sample")["run"]
        .agg(lambda runs: ";".join(sorted(set(runs))))
        .to_dict()
    )


def fragpipe_ions(path, experiments):
    ions = read_tsv(path).rename(columns={"Charge": "charge"})
    ions["peptidoform"] = (
        ions["Modified Sequence"]
        .str.replace(
            r"\[(\d+\.\d+)\]",
            lambda match: f"[UNIMOD:{FRAGPIPE_MASSES[match[1]]}]",
            regex=True,
        )
        .str.replace(r"^n(\[[^]]+\])", r"\1-", regex=True)
    )
    ions["assigned_peptidoform"] = assigned_peptides(ions, "Peptide Sequence")
    observed = []
    for experiment, runs in experiments.items():
        intensity = ions[f"{experiment} Intensity"]
        positive = intensity.gt(0)
        observed.append(
            ions.loc[positive, [*PEPTIDE, "assigned_peptidoform", "M/Z"]].assign(
                run=runs, label="LFQ", intensity=intensity[positive]
            )
        )
    return ions, pd.concat(observed, ignore_index=True)


def fragpipe_groups(path, experiments):
    groups = read_tsv(path)
    # FragPipe identifies contaminants in the database prefix and lists their accession separately.
    groups["accessions"] = protein_sets(
        groups["Protein"].str.replace("contam_", "", regex=False)
        + ","
        + groups["Indistinguishable Proteins"]
        .fillna("")
        .str.replace("contam_", "", regex=False)
    )
    rows = []
    for experiment, runs in experiments.items():
        raw = groups[f"{experiment} Intensity"]
        maxlfq = groups[f"{experiment} MaxLFQ Intensity"]
        intensity = raw.where(raw.gt(0)).fillna(maxlfq.where(maxlfq.gt(0)))
        evidence = groups[
            [
                f"{experiment} {count}"
                for count in (
                    "Spectral Count",
                    "Unique Spectral Count",
                    "Total Spectral Count",
                )
            ]
        ]
        observed = intensity.notna() | evidence.fillna(0).ne(0).any(axis=1)
        rows.append(
            groups.loc[observed, ["accessions"]].assign(
                runs=runs, label="LFQ", intensity=intensity[observed]
            )
        )
    return groups, pd.concat(rows, ignore_index=True)


def check_fragpipe(audit, inputs, output):
    source = read_tsv(
        inputs["psm"],
        ["Spectrum", "Peptide", "Charge", "Assigned Modifications", "Intensity"],
    )
    source["peptidoform"] = assigned_peptides(source, "Peptide")
    scan_parts = source["Spectrum"].str.rsplit(".", n=3, expand=True)
    source["run"] = scan_parts[0]
    source["scan"] = scan_parts[1].astype(int).map(lambda n: (n,))
    source = source.rename(columns={"Charge": "charge"})
    qpx = qpx_psms(output)
    audit.keys(
        "psm",
        "psm_rows",
        source,
        qpx,
        [*FEATURE, "scan"],
        "One complete deposited A549 run, 3152. Use the deposited Philosopher results, including reported contaminants. "
        "PRIDE records 1% FDR at PSM and protein levels.",
    )
    audit.identities("psm", source, qpx)
    audit.add(
        "psm",
        "intensity_comparison",
        note="The source PSM Intensity has no scalar counterpart in the QPX PSM view.",
    )

    experiments = fragpipe_experiments(inputs["annotation"])
    ions, source = fragpipe_ions(inputs["ion"], experiments)
    qpx = qpx_features(output)
    audit.add(
        "feature",
        "input_ion_rows",
        len(ions),
        len(qpx),
        note="Combined table, before expansion across experiments.",
    )
    omitted = source[source["peptidoform"].ne(source["assigned_peptidoform"])]
    audit.add(
        "feature",
        "modification_column_disagreements",
        int(ions["peptidoform"].ne(ions["assigned_peptidoform"]).sum()),
        note=f"Counts native ion rows covering {len(omitted)} positive run-intensity observations. "
        "Some deposited rows have site modifications in Modified Sequence absent from Assigned Modifications. "
        "QPX adds the Modified Sequence delta masses that Assigned Modifications leave out. "
        f"Examples {examples(omitted, [*FEATURE, 'assigned_peptidoform', 'M/Z', 'intensity'])}.",
    )
    feature_note = "One observation per positive experiment intensity in combined_ion.tsv, keyed by Modified Sequence."
    audit.keys("feature", "feature_rows", source, qpx, FEATURE, feature_note)
    audit.identities("feature", source, qpx)
    converted = channel_rows(qpx)
    audit.intensities("feature", source, converted, [*FEATURE, "label"], feature_note)

    groups, source = fragpipe_groups(inputs["pg"], experiments)
    qpx = qpx_proteins(output)
    audit.keys(
        "pg",
        "protein_groups",
        groups[["accessions"]].drop_duplicates(),
        qpx[["accessions"]].drop_duplicates(),
        ["accessions"],
    )
    key = [*PROTEIN, "label"]
    audit.keys(
        "pg",
        "protein_group_rows",
        source,
        qpx,
        key,
        "Keep groups with a quantity or spectral count in the experiment.",
    )
    audit.intensities(
        "pg",
        source,
        qpx,
        key,
        "Compare reported raw intensity with MaxLFQ used when raw intensity is unavailable.",
    )


def diann_source(path, connection):
    table = connection.execute(
        """
        SELECT
            "Run" AS run, "Modified.Sequence" AS modified_sequence, "Precursor.Charge" AS charge,
            "Protein.Group" AS accessions, "Precursor.Quantity" AS intensity,
            "PG.Quantity" AS raw_pg, "PG.MaxLFQ" AS maxlfq, "Q.Value" AS q
        FROM read_csv(?, delim = '\t', header = true, sample_size = 50000)
        """,
        [str(path)],
    ).df()
    return table


def check_diann(audit, inputs, output):
    with duckdb.connect(config={"threads": 4, "memory_limit": "8GB"}) as connection:
        raw = diann_source(inputs["report"], connection)
        qpx = connection.execute(
            """
            SELECT peptidoform, charge, run_file_name AS run,
                   is_decoy, is_library_decoy, channel.label, channel.intensity
            FROM read_parquet(?), UNNEST(intensities) AS i(channel)
            """,
            [str(output / "bench.feature.parquet")],
        ).df()

    passes = raw["q"].lt(DIANN_QVALUE) & raw["accessions"].notna()
    source = raw.loc[passes, :].copy()
    excluded = raw.loc[~passes, ["run", "modified_sequence", "charge", "q"]]
    audit.add(
        "feature",
        "input_report_rows",
        len(raw),
        len(qpx),
        note=f"Native DIA-NN report. In both counts below, Q.Value < {DIANN_QVALUE} and Protein.Group present. "
        f"Rejected source rows {len(excluded)}. Examples {examples(excluded, list(excluded))}.",
    )
    source["run"] = source["run"].map(run_stem)
    source["is_decoy"] = source["accessions"].str.startswith(
        ("DECOY_", "decoy_", "rev_", "REV_")
    )
    source["is_library_decoy"] = source["modified_sequence"].str.startswith("^")
    source["peptidoform"] = (
        source["modified_sequence"].str.removeprefix("^").map(openms_peptide)
    )
    source["label"] = "LFQ"
    key = [*FEATURE, "is_decoy", "is_library_decoy"]
    audit.keys("feature", "feature_rows", source, qpx, key)
    audit.identities("feature", source, qpx)
    missing_quantity = source["intensity"].le(0) | source["intensity"].isna()
    audit.add(
        "feature",
        "unquantified_rows",
        int(missing_quantity.sum()),
        int(qpx["intensity"].isna().sum()),
        note="DIA-NN zero or missing precursor quantities are null in QPX. "
        f"Source examples {examples(source[missing_quantity], [*FEATURE, 'intensity'])}.",
    )
    source["intensity"] = source["intensity"].where(~missing_quantity)
    audit.intensities(
        "feature",
        source,
        qpx,
        [*key, "label"],
        "Primary intensity is Precursor.Quantity.",
    )
    audit.add(
        "psm",
        "intensity_comparison",
        note="DIA-NN has no PSM table in this report. MS2.Scan is precursor metadata.",
    )

    source["accessions"] = protein_sets(source["accessions"])
    source = source[source["accessions"].ne("")]
    source["runs"] = source["run"]
    source["raw_pg"] = source["raw_pg"].where(source["raw_pg"].gt(0))
    source["maxlfq"] = source["maxlfq"].where(source["maxlfq"].gt(0))
    groups = source.groupby(PROTEIN, as_index=False)[["raw_pg", "maxlfq"]].max()
    groups["intensity"] = groups["raw_pg"].fillna(groups["maxlfq"])
    groups["label"] = "LFQ"
    qpx = qpx_proteins(output)
    audit.keys(
        "pg",
        "protein_groups",
        groups[["accessions"]].drop_duplicates(),
        qpx[["accessions"]].drop_duplicates(),
        ["accessions"],
    )
    key = [*PROTEIN, "label"]
    audit.keys(
        "pg",
        "protein_group_rows",
        groups,
        qpx,
        key,
        "One row per membership set and run, after the same precursor q-value filter.",
    )
    audit.intensities(
        "pg",
        groups,
        qpx,
        key,
        "Each repeated run/group uses its largest positive PG.Quantity, falling back to positive PG.MaxLFQ.",
    )


MQ_COORDINATES = ["rt_start", "rt_stop", "scan"]
MQ_FLAGS = ["Reverse", "Potential contaminant"]
MQ_REPORTER = "Reporter intensity"


@cache
def maxquant_peptide(sequence):
    value = sequence.strip("_").replace("(ox)", "[UNIMOD:35]").removeprefix("(ac)")
    # parameters.txt declares fixed carbamidomethylation. mqpar.xml specifies TMT
    # at lysines and the peptide N-terminus. Acetylation occupies the latter site.
    value = value.replace("C", "C[UNIMOD:4]").replace("K", "K[UNIMOD:737]")
    nterm = 1 if sequence.startswith("_(ac)") else 737
    return f"[UNIMOD:{nterm}]-{value}"


def maxquant_ids(frame):
    return frame.rename(columns={"Charge": "charge", "Raw file": "run"}).assign(
        peptidoform=frame["Modified sequence"].map(maxquant_peptide),
    )


def maxquant_targets(frame, qpx, key):
    contaminants = frame.loc[
        frame["Potential contaminant"].eq("+"), key
    ].drop_duplicates()
    qpx = qpx.merge(
        contaminants.assign(contaminant=True),
        on=key,
        how="left",
        validate="many_to_one",
    )
    return frame.loc[frame[MQ_FLAGS].ne("+").all(axis=1)], qpx.loc[
        ~qpx["is_decoy"] & qpx["contaminant"].isna()
    ]


def maxquant_psms(audit, path, evidence, output):
    columns = [
        "Modified sequence",
        "Charge",
        "Raw file",
        "Scan number",
        "Reverse",
        "Evidence ID",
    ]
    raw = read_tsv(path, columns)
    raw["Potential contaminant"] = raw["Evidence ID"].map(
        evidence.set_index("id")["Potential contaminant"]
    )
    source = maxquant_ids(raw)
    source["scan"] = source["Scan number"].map(lambda n: (n,))
    qpx = qpx_psms(output, ["is_decoy"])
    key = [*FEATURE, "scan"]
    audit.keys("psm", "input_psm_rows", source, qpx, key)
    targets, target_qpx = maxquant_targets(source, qpx, key)
    audit.keys(
        "psm",
        "psm_rows",
        targets,
        target_qpx,
        key,
        "MaxQuant PSM FDR 1%. Remove Reverse and Potential contaminant. "
        "The latter is looked up by Evidence ID, and the source mask is applied to both sides.",
    )
    audit.identities("psm", targets, target_qpx)
    audit.add(
        "psm",
        "intensity_comparison",
        note="QPX PSM has no scalar counterpart to MaxQuant Precursor Intensity.",
    )


def maxquant_features(audit, evidence, reporters, output):
    key = [*FEATURE, *MQ_COORDINATES]
    evidence = maxquant_ids(evidence)
    evidence["scan"] = evidence["MS/MS scan number"].map(
        lambda n: (int(n),) if pd.notna(n) else ()
    )
    evidence["rt_start"] = (60 * evidence["Calibrated retention time start"]).astype(
        "float32"
    )
    evidence["rt_stop"] = (60 * evidence["Calibrated retention time finish"]).astype(
        "float32"
    )
    partition = [
        "Modified sequence",
        "charge",
        "run",
        "Calibrated retention time start",
        "Calibrated retention time finish",
        "scan",
    ]
    retained = evidence.assign(transfer=evidence["Type"].eq("MULTI-MATCH")).sort_values(
        ["transfer", "PEP", "id"]
    )
    duplicates = retained.duplicated(partition)
    source = retained.loc[~duplicates]
    qpx = qpx_features(output, [*MQ_COORDINATES, "is_decoy"])
    qpx["scan"] = qpx["scan"].map(tuple)

    audit.add(
        "feature",
        "input_evidence_rows",
        len(evidence),
        len(qpx),
        note=f"Collapse {int(duplicates.sum())} repeated peak identities. Choose direct MS/MS first, then lower PEP and lower id. "
        f"Dropped examples {examples(retained[duplicates], [*key, 'Type', 'PEP', 'id'])}.",
    )
    audit.keys("feature", "all_feature_rows", source, qpx, key)
    targets, target_qpx = maxquant_targets(source, qpx, key)
    audit.keys(
        "feature",
        "feature_rows",
        targets,
        target_qpx,
        key,
        "Exclude Reverse and Potential contaminant on both sides.",
    )
    audit.identities("feature", targets, target_qpx)

    values = targets.melt(
        id_vars=key,
        value_vars=list(reporters),
        var_name="label",
        value_name="intensity",
    )
    values["label"] = values["label"].map(reporters)
    values["intensity"] = values["intensity"].where(values["intensity"].gt(0))
    observed = channel_rows(target_qpx)
    channel_key = [*key, "label"]
    reporter_note = (
        "Compare positive, uncorrected Reporter intensity. mqpar.xml gives eight channels in the order "
        "TMT128N, TMT128C, TMT129N, TMT129C, TMT130N, TMT130C, TMT131N, TMT131C."
    )
    audit.keys("feature", "reporter_keys", values, observed, channel_key, reporter_note)
    audit.intensities("feature", values, observed, channel_key, reporter_note)


def maxquant_groups(audit, path, reporters, evidence, output):
    raw = read_tsv(path)
    flags = [*MQ_FLAGS, "Only identified by site"]
    groups = raw.loc[raw[flags].ne("+").all(axis=1)].copy()
    groups["accessions"] = protein_sets(groups["Protein IDs"])
    groups["runs"] = ";".join(sorted(evidence["Raw file"].unique()))
    values = groups.melt(
        id_vars=PROTEIN,
        value_vars=list(reporters),
        var_name="label",
        value_name="intensity",
    )
    values["label"] = values["label"].map(reporters)
    values["intensity"] = values["intensity"].where(values["intensity"].gt(0))
    note = (
        f"Exclude Reverse, Potential contaminant, and Only identified by site from {len(raw)} input groups on both sides. "
        "The one unnamed experiment aggregates the twelve fractions of evidence.txt."
    )
    qpx = qpx_proteins(output, ["is_decoy", "contaminant", "cv_params"])
    site_only = qpx.pop("cv_params").map(
        lambda params: (
            params is not None
            and any(param["cv_name"] == "only_identified_by_site" for param in params)
        )
    )
    qpx = qpx.loc[~(qpx.pop("is_decoy") | qpx.pop("contaminant") | site_only)]
    audit.keys(
        "pg",
        "protein_groups",
        groups[["accessions"]].drop_duplicates(),
        qpx[["accessions"]].drop_duplicates(),
        ["accessions"],
        note,
    )
    audit.keys("pg", "protein_group_rows", values, qpx, [*PROTEIN, "label"], note)
    audit.intensities("pg", values, qpx, [*PROTEIN, "label"], note)


def check_maxquant(audit, inputs, output):
    parameters = ET.parse(inputs["mqpar"])
    channels = [
        f"TMT{node.text.rsplit('Nter', 1)[1]}"
        for node in parameters.findall(".//isobaricLabels/string")
        if "-Nter" in node.text
    ]
    reporters = {
        f"{MQ_REPORTER} {index}": channel for index, channel in enumerate(channels)
    }
    columns = [
        "id",
        "Modified sequence",
        "Raw file",
        "Charge",
        "MS/MS scan number",
        "Type",
        "PEP",
        "Calibrated retention time start",
        "Calibrated retention time finish",
        *MQ_FLAGS,
        *reporters,
    ]
    evidence = read_tsv(inputs["evidence"], columns)
    maxquant_psms(audit, inputs["msms"], evidence, output)
    maxquant_features(audit, evidence, reporters, output)
    maxquant_groups(audit, inputs["pg"], reporters, evidence, output)


INPUT_OPTIONS = {
    "diann": {"report": "--report-path", "sdrf": "--sdrf-file"},
    "openms-consensus": {"consensusxml": "--consensusxml", "sdrf": "--sdrf-file"},
    "quantms-msstats": {"msstats": "--msstats-file", "sdrf": "--sdrf-file"},
    "maxquant": {
        "msms": "--msms-file",
        "evidence": "--evidence-file",
        "pg": "--protein-groups-file",
        "sdrf": "--sdrf-file",
    },
    "fragpipe": {
        "psm": "--psm-file",
        "ion": "--ion-file",
        "pg": "--pg-file",
        "annotation": "--experiment-annotation-file",
    },
}
CHECKS = {
    "diann": check_diann,
    "openms-consensus": check_openms,
    "quantms-msstats": check_msstats,
    "maxquant": check_maxquant,
    "fragpipe": check_fragpipe,
}
EXACT_NAMES = {
    "report.tsv": "report",
    "msms.txt": "msms",
    "evidence.txt": "evidence",
    "proteinGroups.txt": "pg",
    "mqpar.xml": "mqpar",
    "parameters.txt": "parameters",
    "summary.txt": "summary",
    "psm.tsv": "psm",
    "combined_ion.tsv": "ion",
    "combined_protein.tsv": "pg",
    "experiment_annotation.tsv": "annotation",
}
SUFFIXES = {
    ".sdrf.tsv": "sdrf",
    ".consensusXML": "consensusxml",
    "_msstats_in.csv": "msstats",
    "_msstats_in.csv.gz": "msstats",
}


def source_kind(path):
    for suffix, role in SUFFIXES.items():
        if path.name.endswith(suffix):
            return role
    return EXACT_NAMES[path.name]


def convert(converter, accession, inputs, output):
    command = [
        "qpxc",
        "convert",
        converter,
        "--output-folder",
        str(output),
        "--output-prefix",
        "bench",
        "--project-accession",
        accession,
    ]
    for role, option in INPUT_OPTIONS[converter].items():
        command.extend([option, str(inputs[role])])
    if converter != "openms-consensus":
        command.extend(["--max-cpus", "4"])
    if converter in {"diann", "openms-consensus"}:
        command.append("--no-mudata")
    if converter == "openms-consensus":
        command.extend(["--structures", "psm,feature,pg"])
    if converter == "diann":
        command.extend(["--qvalue-threshold", str(DIANN_QVALUE)])
    print(" ".join(command), flush=True)
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reuse-qpx",
        action="store_true",
        help="Use previously converted views beside the source files.",
    )
    args = parser.parse_args()
    units = defaultdict(dict)
    with MANIFEST.open(newline="") as source:
        for row in csv.DictReader(source):
            path = Path(row["file"])
            units[row["converter"], row["accession"]][source_kind(path)] = path

    rows = []
    for (converter, accession), inputs in sorted(units.items()):
        directory = next(
            parent
            for parent in next(iter(inputs.values())).parents
            if parent.name == accession
        )
        output = directory / "qpx"
        print(f"Checking {converter} {accession}", flush=True)
        if not args.reuse_qpx:
            convert(converter, accession, inputs, output)
        audit = Agreement(converter, accession)
        CHECKS[converter](audit, inputs, output)
        rows.extend(audit.rows)

    with RESULT.open("w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
