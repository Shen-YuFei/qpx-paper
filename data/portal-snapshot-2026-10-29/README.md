# QPX corpus on browse.quantms.org, snapshot 2026-10-29

Read-only inventory of https://browse.quantms.org/quantms/datasets/ (155 dataset folders,
280 content-hash folders). Row counts come from Parquet footers; only run, sample, dataset
and provenance tables were read in full. Totals in `corpus_summary.md` add up every QPX
hash folder, so datasets with several versions are counted more than once.

- `corpus_datasets.csv` – one row per QPX hash folder (acquisition class and evidence,
  species, instrument, sample/run counts, PSM/feature/PG rows, size, writer metadata).
- `corpus_files.csv` – one row per file.
- `corpus_anomalies.md` – datasets without QPX output, datasets with several QPX versions,
  missing views and fields.

This is the portal as published, not the deposited data record: most folders were written
with QPX 1.0.x and many do not record the acquisition method.

## Acquisition method

`acquisition_latest.csv` classifies the latest QPX version of each dataset, produced by
`classify_acq.py` from SDRF files (in the dataset folders and in
bigbio/sdrf-annotated-datasets), the PRIDE Archive API and the QPX run and dataset views.
The SDRF value wins when present; disagreements with the QPX files or PRIDE are listed in
the `conflict` column. The script reads the raw sources collected in the scratchpad
(`acquisition_sources.json`, `acquisition_cache/`), which are not kept here.
