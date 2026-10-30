# Tables

Table 2: QPX views. Data and metadata views are Parquet files named
`{PREFIX}.{view}.parquet`; expression views are AnnData files.

| View | One row per | Primary key | Main content |
|-----------|-----------|------------------|-------------------------|
| `psm` | peptide-spectrum match | `psm_id` | peptidoform, charge, run, scan, retention time, scores and q-values, optional fragment arrays |
| `feature` | peptide feature in a run | `feature_id` | peptidoform, charge, run, retention time, intensities per label channel, protein-group assignment, q-values |
| `pg` | protein group, quantification unit and label | `pg_id` | member accessions and genes, runs in the unit, label, intensity and additional intensities, q-values, peptide counts |
| `pepmap` | peptidoform | `peptidoform` | proteins and genes the peptidoform maps to, uniqueness flags |
| `site` | modification-site claim | `site_id` | protein, position, modification, q-value, probability that the residue is modified, evidence fraction |
| `proteoform` | protein-family member, unit and label | `proteoform_id` | canonical, isoform, variant or chain member, member-level q-value |
| `mz` | spectrum | `id` | MS1 and MS2 peak arrays and scan metadata |
| `sample` | sample | `sample_accession` | organism, tissue or cell type, disease and other SDRF characteristics |
| `run` | MS run | `run_file_name` | samples and label channels in the run, fraction, instrument, enzymes, dissociation and acquisition method |
| `dataset` | dataset (single row) | `project_accession` | title, description, publication, software, search parameters |
| `ontology` | field and view | `field_name`, `view` | ontology terms used by the dataset's fields |
| `provenance` | processing step | `step_order` | tool, version, parameters and FDR thresholds |
| `ae`, `de` (`.h5ad`) | protein × sample, protein × contrast | – | absolute expression (e.g. iBAQ) and differential expression results |

Table 3: Views written by each converter. Yes: always written. SDRF: written when an SDRF
is given. PDC: built from PDC study metadata. –: not written. The dataset column also
stands for the provenance view. [TODO: check against the converter documentation of the cited
release; conditional cases are simplified here.]

| Source | psm | feature | pg | sample, run | dataset |
|---|:-:|:-:|:-:|:-:|:-:|
| MaxQuant | Yes | Yes | Yes | SDRF | Yes |
| FragPipe | Yes | Yes | Yes | SDRF | Yes |
| DIA-NN | – | Yes | With PG matrix | Yes | Yes |
| Spectronaut | – | Yes | Yes | SDRF | Yes |
| OpenMS (native QPX export) | Yes | Yes | Yes | Yes | Yes |
| OpenMS consensusXML | Yes | Yes | Yes | SDRF | Yes |
| CPTAC CDAP | Yes | Yes | Yes | PDC | Yes |
| mzIdentML | Yes | – | If in file | SDRF | Yes |
| quantms MSstats input | – | Yes | – | Yes | Yes |
