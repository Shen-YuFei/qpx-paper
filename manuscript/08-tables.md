# Tables

Table 2: QPX views in specification 1.3, written by QPX 1.4.0. Parquet views are named
`{PREFIX}.{view}.parquet`; absolute and differential expression results are AnnData files
(`.h5ad`), and a dataset's quantification results can be exported as one MuData file
(`{PREFIX}.h5mu`).

| View | One row per | Primary key | Main content |
|-----------|-----------|------------------|-------------------------|
| `psm` | peptide-spectrum match | `psm_id` | peptidoform, charge, run, scan, scores and q-values, protein mappings, optional peak arrays and competing modification interpretations |
| `feature` | peptide feature in a run (one multiplet for MS1 labels) | `feature_id` | peptidoform, charge, run, retention time, quantities per label channel, q-values, protein-group assignment, identification origin (direct, transferred or secondary) |
| `pg` | protein group, quantification unit and label | `pg_id` | member accessions and genes, runs in the unit, primary and additional quantities, q-values, peptide counts |
| `pepmap` | peptidoform | `peptidoform` | proteins the peptidoform maps to, with peptide positions, a uniqueness flag and optional sequence edits relative to the reference protein |
| `protein` | protein accession | `accession` | entry name, description, gene, organism, length and sequence from the sequence database |
| `site` | modification-site claim, quantification unit and label | `site_id` | protein, position, modification, q-value, localisation evidence, intensity and stoichiometry |
| `proteoform` | protein-family member, quantification unit and label | `proteoform_id` | canonical, isoform, variant or processed-chain member, evidence, q-value and quantities |
| `fragment` | fragment ion of a feature, label and run | `fragment_id` | ion annotation, m/z, area or height, scores, optional chromatographic arrays |
| `xic` | extracted precursor or fragment ion trace per run and label | `xic_id` | transition, extraction coordinates, linked features, retention time and intensity arrays |
| `mz` | spectrum | `id` | MS level, scan, precursor, timing and ion mobility metadata, peak arrays |
| `sample` | sample | `sample_accession` | organism, tissue or cell type, disease and other SDRF annotations |
| `run` | MS run | `run_file_name` | samples and label channels in the run, fraction, instrument, acquisition method, gradient, acquisition start |
| `dataset` | dataset (single row) | `project_accession` | title, description, publication, software |
| `ontology` | field and view | `field_name`, `view` | controlled vocabulary terms of the columns, scores, parameters and intensity names the views write |
| `provenance` | processing step | `step_order` | tool, version, parameters, configuration and FDR thresholds where available |
| `ae` (`.h5ad`) | sample × protein or protein group | – | absolute expression (e.g. iBAQ) with sample annotations |
| `de` (`.h5ad`) | protein and contrast | – | fold changes, test statistics and p-values per contrast |

Table 3: Views written by the `qpxc convert` commands of QPX 1.4.0. Yes: written. In: written
when the tool output for that level is given. Opt: written on request (fragment quantities from
DIA-NN and Spectronaut reports, DIA-NN chromatogram exports, and MS2 spectra matched to the
converted features). Ab: written when the PSM export has abundance columns. SDRF: written from
an SDRF. PDC: written from PDC study metadata by `qpxc pdc2qpx`. File: written when the
mzIdentML file holds the information. –: not written. The run column stands for the sample and
run views, and every converter also writes the dataset and provenance views. Outside this
table, `qpxc convert mz` writes the `mz` view of full runs from mzML [@Martens_2011], the
`site` view is written from MaxQuant sites tables and the `protein` view from MaxQuant protein
groups or a FASTA database; no converter writes the `proteoform` view.

```{=latex}
\begingroup\setlength{\tabcolsep}{3.5pt}
```

| Source | psm | feature | pg | pepmap | fragment | xic | mz | run |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| MaxQuant | In | In | In | In | – | – | – | SDRF |
| FragPipe | In | In | In | In | – | – | – | SDRF |
| DIA-NN | – | Yes | Yes | Yes | Opt | Opt | Opt | SDRF |
| Spectronaut | – | Yes | Yes | – | Opt | – | – | SDRF |
| Proteome Discoverer | Yes | Ab | In | Ab | – | – | – | SDRF |
| OpenMS consensusXML | Yes | Yes | Yes | – | – | – | – | SDRF |
| CPTAC CDAP | Yes | Yes | Yes | – | – | – | – | PDC |
| mzIdentML | Yes | – | File | File | – | – | – | – |
| quantms MSstats | – | Yes | – | – | – | – | – | SDRF |

```{=latex}
\endgroup
```
