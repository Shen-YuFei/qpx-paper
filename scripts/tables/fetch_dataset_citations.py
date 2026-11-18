"""Fetch data citations and check the QPX corpus release dates."""

from concurrent.futures import ThreadPoolExecutor
import csv
from dataclasses import dataclass, field
from pathlib import Path
import re

import requests


DATA = Path(__file__).resolve().parents[2] / "data"
PRIDE = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/"
PX = "https://proteomecentral.proteomexchange.org"
MASSIVE = "https://massive.ucsd.edu/ProteoSAFe/"
PDC = "https://pdc.cancer.gov/graphql"
HTTP = {
    "headers": {"User-Agent": "QPX-dataset-citations/1.0", "Cache-Control": "no-cache"},
    "timeout": (20, 35),
}
AUTHOR_OVERRIDES = {
    # PRIDE registers two lab PIs as one name.
    "PXD002899": ("Karaca, Samir", "Urlaub, Henning", "Görlich, Dirk"),
    # PRIDE registers the submitter's name in Chinese, which the LaTeX build cannot render.
    "PXD027817": ("Zhang, Yue", "Che, Yi-Qun"),
    # PRIDE registers the HipSci consortium as a person; braces keep it one name in BibTeX.
    "PXD003903": ("{HipSci Project}", "Lamond, Angus"),
}
FIELDS = (
    "dataset",
    "accession_used",
    "repository",
    "cite_key",
    "authors",
    "title",
    "year",
    "doi",
    "url",
    "metadata_source",
    "publication_pmid",
    "publication_doi",
    "public_date_check",
    "note",
)
DOI = re.compile(r'10\.\d{4,9}/[^\s,"<>]+', re.I)
LATEX = str.maketrans({char: "\\" + char for char in "&%_#$"})
HONORIFIC = re.compile(r"^(?:(?:Dr|Prof)\b\.?\s*)+", re.I)
PDC_QUERY = """
query($id: String!) {
  uiStudySummary(pdc_study_id:$id) { pdc_study_id study_name contacts { name } }
  uiPublication(pdc_study_id:$id) { pubmed_id doi title }
}
"""


@dataclass
class Metadata:
    title: str = ""
    authors: tuple[str, ...] = ()
    year: str = ""
    doi: str = ""
    url: str = ""
    source: str = ""
    public_date: str = ""
    date_source: str = ""
    pmids: tuple[str, ...] = ()
    paper_dois: tuple[str, ...] = ()
    notes: list[str] = field(default_factory=list)

    def add_publications(self, pairs):
        pairs = list(pairs)
        self.pmids = unique((*self.pmids, *(pmid for pmid, _ in pairs)))
        self.paper_dois = unique(
            doi.lower() for doi in (*self.paper_dois, *(doi for _, doi in pairs))
        )


def clean(value) -> str:
    return " ".join(str(value or "").split())


def unique(values) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def name(family="", given="", display="") -> str:
    family, given, display = map(clean, (family, given, display))
    if family == "MD":
        display, family, given = given.rstrip(","), "", ""
    family, given, display = (
        HONORIFIC.sub("", part) for part in (family, given, display)
    )
    if family and given.endswith(" Van"):
        given, family = given[:-4], "Van " + family
    if family:
        return ", ".join(filter(None, (family, given)))
    if "," in display:
        return display
    given, _, family = display.rpartition(" ")
    return f"{family}, {given}" if given else display


def doi_in(value) -> str:
    match = DOI.search(clean(value))
    return match[0].rstrip(".)];") if match else ""


def pmid_in(value) -> str:
    match = re.search(r"(?:^|/)(\d+)/?$", clean(value))
    return match[1] if match else ""


def term_value(terms, accession: str) -> str:
    return next(
        (clean(t.get("value")) for t in terms if t["accession"] == accession), ""
    )


def px_references(record):
    for item in record.get("publications", []):
        terms = item.get("terms", []) if isinstance(item, dict) else item
        yield (
            pmid_in(term_value(terms, "MS:1000879")),
            doi_in(term_value(terms, "MS:1001922") or term_value(terms, "MS:1002866")),
        )


def repository_references(items):
    for item in items:
        yield (
            pmid_in(item.get("pubmedID") or item.get("pubmed_id")),
            doi_in(item.get("doi") or item.get("referenceLine") or item.get("title")),
        )


def px_lookup(accession: str) -> tuple[dict, str, str]:
    direct = f"{PX}/api/proxi/v0.1/datasets/{accession}?resultType=full"
    redirect = f"{PX}/cgi/GetDataset?ID={accession}&outputMode=JSON"
    for url in (direct, redirect):
        response = requests.get(url, **HTTP)
        if response.status_code == 404:
            return {}, "", direct
        response.raise_for_status()
        record = response.json()
        # ProteomeCentral can send another dataset's history with a correct identifier.
        if term_value(record["identifiers"], "MS:1001919") != accession:
            continue
        history = record["datasetHistory"]
        if any(item["datasetIdentifier"] != accession for item in history):
            continue
        first = min(
            (item for item in history if item["status"] == "announced"),
            key=lambda item: item["revisionNumber"],
        )
        return record, first["submissionDate"][:10], response.url
    raise ValueError(
        f"ProteomeCentral returned another dataset's record for {accession}"
    )


def pride_metadata(accession, record, announcement, px_source) -> Metadata:
    response = requests.get(PRIDE + accession, **HTTP)
    response.raise_for_status()
    pride = response.json()
    authors = unique(
        name(person["lastName"], person["firstName"])
        for group in ("submitters", "labPIs")
        for person in pride[group]
    )
    published = pride["publicationDate"]
    meta = Metadata(
        title=clean(pride["title"]),
        authors=AUTHOR_OVERRIDES.get(accession, authors),
        year=published[:4],
        url=f"https://www.ebi.ac.uk/pride/archive/projects/{accession}",
        source=response.url,
        public_date=published,
        date_source=response.url,
    )
    if announcement and announcement != published:
        meta.notes.append(
            f"ProteomeCentral first announced on {announcement} UTC ({px_source})."
        )
    meta.add_publications(repository_references(pride["references"]))
    meta.add_publications(px_references(record))
    if doi := doi_in(pride["doi"]):
        registry = requests.get("https://api.crossref.org/works/" + doi, **HTTP)
        registry.raise_for_status()
        meta.doi, meta.url = doi, "https://doi.org/" + doi
        meta.notes.append(
            f"DOI confirmed in Crossref ({registry.url}). Citation metadata come from PRIDE."
        )
    return meta


def massive_metadata(accession: str, record: dict) -> Metadata:
    msv = term_value(record["identifiers"], "MS:1002487") if record else accession
    response = requests.get(f"{MASSIVE}proxi/v0.1/datasets/{msv}", **HTTP)
    response.raise_for_status()
    native = response.json()

    history_url = f"{MASSIVE}MassiveServlet?function=massivehistory&massiveid={msv}"
    history = requests.get(history_url, **HTTP)
    history.raise_for_status()
    public_date = min(
        item["date"][:10]
        for item in history.json()
        if item["workflow"] == "MAKE-DATASET-PUBLIC"
    )

    landing = requests.get(f"{MASSIVE}dataset.jsp?accession={msv}", **HTTP)
    landing.raise_for_status()
    doi = re.search(r"doi:(10\.25345/[A-Za-z0-9]+)", landing.text, re.I)[1]
    registry = requests.get("https://api.datacite.org/dois/" + doi, **HTTP)
    registry.raise_for_status()
    data = registry.json()["data"]["attributes"]
    meta = Metadata(
        title=clean(
            next(
                title["title"] for title in data["titles"] if not title.get("titleType")
            )
        ),
        authors=tuple(
            name(a.get("familyName"), a.get("givenName"), a["name"])
            for a in data["creators"]
        ),
        year=str(data["publicationYear"]),
        doi=doi,
        url="https://doi.org/" + doi,
        source=registry.url,
        public_date=public_date,
        date_source=history_url,
        notes=[f"DataCite publisher={clean(data['publisher'])}."],
    )
    meta.add_publications(px_references(native))
    meta.add_publications(px_references(record))
    return meta


def iprox_metadata(record, announcement, px_source) -> Metadata:
    if not record:
        return Metadata(
            notes=[f"ProteomeCentral returned no matching record ({px_source})."]
        )
    native_id = term_value(record["identifiers"], "MS:1002836")
    authors = unique(
        name(display=term_value(terms, "MS:1000586"))
        for terms in (contact["terms"] for contact in record["contacts"])
        if any(t["accession"] in {"MS:1002037", "MS:1002332"} for t in terms)
    )
    meta = Metadata(
        title=clean(record["title"]),
        authors=authors,
        year=announcement[:4],
        url=f"https://www.iprox.cn/page/project.html?id={native_id}",
        source=px_source,
        public_date=announcement,
        date_source=px_source,
    )
    meta.add_publications(px_references(record))
    return meta


def pdc_metadata(accession: str, year: str) -> Metadata:
    response = requests.post(
        PDC, json={"query": PDC_QUERY, "variables": {"id": accession}}, **HTTP
    )
    response.raise_for_status()
    data = response.json()["data"]
    study = next(x for x in data["uiStudySummary"] if x["pdc_study_id"] == accession)
    meta = Metadata(
        title=clean(study["study_name"]),
        authors=unique(name(display=contact["name"]) for contact in study["contacts"]),
        year=year,
        url="https://pdc.cancer.gov/pdc/study/" + accession,
        source=response.url,
    )
    meta.add_publications(repository_references(data["uiPublication"]))
    if not meta.authors:
        meta.notes.append("PDC uiStudySummary provides no registered study contacts.")
    if len(meta.pmids) > 1:
        meta.notes.append(
            "PDC uiPublication lists multiple associated papers without identifying the original."
        )
    if year:
        meta.notes.append("Year retained from dataset_public_dates.csv.")
    return meta


def lookup(accession: str, repository: str, input_date: str) -> Metadata:
    if not accession:
        return Metadata(notes=["No public dataset accession in the input table."])
    if not repository:
        return Metadata(
            notes=[
                "The accession used is a PMID. The public dataset has no verified repository accession."
            ]
        )
    if repository == "PDC":
        return pdc_metadata(accession, input_date[:4])
    record, announcement, source = (
        px_lookup(accession) if accession.startswith(("PXD", "IPX")) else ({}, "", "")
    )
    if repository == "PRIDE":
        return pride_metadata(accession, record, announcement, source)
    if repository == "MassIVE":
        return massive_metadata(accession, record)
    if repository == "iProX":
        return iprox_metadata(record, announcement, source)
    raise ValueError(f"Unknown repository {repository!r} for {accession}")


def output_row(row: dict, meta: Metadata) -> dict:
    checked = ""
    notes = meta.notes.copy()
    if row["repository"] == "PDC":
        checked = "unverified"
    if meta.public_date:
        checked = (
            "same"
            if meta.public_date == row["public_date"]
            else f"differs: {meta.public_date} from {meta.date_source}"
        )
    elif row["date_kind"] == "paper":
        notes.append(
            "The input year is the paper publication year. The public dataset date remains unknown."
        )
    else:
        notes.append("Public date could not be verified.")

    missing = [
        label
        for label in ("title", "authors", "year", "url")
        if not getattr(meta, label)
    ]
    cite_key = ""
    if not missing:
        cite_key = "ds_" + re.sub(r"[^A-Za-z0-9]", "_", row["accession_used"])
    elif meta.title:
        notes.append(f"Citation incomplete (missing {', '.join(missing)}).")
    return {
        **{k: row[k] for k in ("dataset", "accession_used", "repository")},
        "cite_key": cite_key,
        "authors": "; ".join(meta.authors),
        "title": meta.title,
        "year": meta.year,
        "doi": meta.doi,
        "url": meta.url,
        "metadata_source": meta.source,
        "publication_pmid": "; ".join(meta.pmids),
        "publication_doi": "; ".join(meta.paper_dois),
        "public_date_check": checked,
        "note": " ".join(notes),
    }


def bibtex(row: dict) -> str:
    authors = " and ".join(row["authors"].split("; ")).translate(LATEX)
    title = row["title"].translate(LATEX)
    fields = [
        f"  author = {{{authors}}},",
        f"  title = {{{{{title}}}}},",
        f"  howpublished = {{{row['repository']}}},",
        f"  year = {{{row['year']}}},",
    ]
    if row["doi"]:
        fields.append(f"  doi = {{{row['doi']}}},")
    fields.append(f"  url = {{{row['url']}}},")
    return "\n".join((f"@dataset{{{row['cite_key']},", *fields, "}"))


def main() -> None:
    with (DATA / "dataset_public_dates.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        dates = list(csv.DictReader(stream))
    keys = [
        (row["accession_used"], row["repository"], row["public_date"]) for row in dates
    ]
    unique_keys = list(dict.fromkeys(keys))
    with ThreadPoolExecutor(max_workers=4) as pool:
        metadata = dict(
            zip(
                unique_keys,
                pool.map(lambda key: lookup(*key), unique_keys),
                strict=True,
            )
        )
    rows = [
        output_row(row, metadata[key]) for row, key in zip(dates, keys, strict=True)
    ]
    entries = {row["cite_key"]: bibtex(row) for row in rows if row["cite_key"]}
    with (DATA / "dataset_citations.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (DATA / "dataset_citations.bib").write_text(
        "\n\n".join(entries.values()) + "\n", encoding="utf-8"
    )
    print(f"{len(rows)} rows, {len(entries)} BibTeX entries.")


if __name__ == "__main__":
    main()
