---
title: "Supplementary Information"
subtitle: "A columnar file format and a corpus of reprocessed public mass spectrometry proteomics data"
reference-section-title: References
toc-title: Contents
geometry: margin=2cm
---

# Table S1: Views written by the QPX converters

Views written by the `qpxc convert` commands of QPX 1.4.0. Yes: written. In:
written when the corresponding tool output is given (for MaxQuant `msms.txt`, `evidence.txt`
and `proteinGroups.txt`; for FragPipe `psm.tsv`, `combined_ion.tsv` or `ion.tsv` and
`protein.tsv`; for Proteome Discoverer the protein export). Opt: written on request
(`--fragments` for the fragment quantities of DIA-NN and Spectronaut reports, `--xic-folder`
for DIA-NN chromatogram exports, and MS2 spectrum tables matched to the converted features for
`mz`). Ab: written when the PSM export has abundance columns. SDRF: written from an SDRF.
PDC: written from PDC study metadata by `qpxc pdc2qpx`. File: written when the mzIdentML file
holds the information. –: not written. The run column stands for the sample and run views,
and every converter also writes the dataset and provenance views. Outside this table, `qpxc convert mz` writes the `mz` view of full runs from
mzML [@Martens_2011], `qpxc convert sdrf` writes the sample and run views, MaxQuant writes the `site` view
from a sites table (`--sites-file`), and the `protein` view is written by MaxQuant from
`proteinGroups.txt` and from a FASTA database by the DIA-NN and OpenMS consensusXML converters
(`--fasta`) or by `qpxc transform protein-properties`. No converter writes the `proteoform`
view; producers write it through the `qpx` Python API. OpenMS can also write QPX directly. Abbreviations: CPTAC CDAP, Common Data Analysis Pipeline of the Clinical
Proteomic Tumor Analysis Consortium; PDC, Proteomic Data Commons; MS2, tandem mass spectra; PSM, peptide-spectrum match; SDRF,
Sample and Data Relationship Format.

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

# Figure S1: Query time and storage of QPX compared with mzTab and CSV outputs

[TBD: figure]

# Figure S2: Views and files held by each dataset

![](figures/figS2){width=100%}

Each row is a dataset, grouped by
processing route; a filled cell marks a view or file present in the latest QPX version of the
dataset, except for the SDRF column, which marks an SDRF anywhere in the dataset folder. The
row under each route gives the number of its datasets holding each view or file, and the last
row the number over all datasets. ID only, identification only; SDRF, Sample and Data
Relationship Format. [TBD: figure]
