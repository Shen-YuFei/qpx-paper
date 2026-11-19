# Supplementary Information

Supplementary Table 1 (`supplementary/datasets.csv`): The datasets of the corpus, one row per
dataset: accession, hosting repository and data citation; processing route; acquisition and
labelling as annotated in the SDRF; organisms and instruments; numbers of samples, runs, PSM,
feature and protein-group records and size; specification version and version folder of the
QPX files; whether the portal holds an SDRF; first public release; original publication; and
known issues. Built by `scripts/tables/dataset_table.py`. [TBD: data]

Supplementary Table 2 (`supplementary/data_dictionary.csv`): Columns of the QPX views of
specification 1.3, generated from the schema files of QPX 1.4.0 by
`scripts/tables/data_dictionary.py`: view, column, type, whether the column is required (yes:
present and non-null unless nullable; no: present and may be null; optional: may be left out of
a file), value range and description, followed by the fields of the struct types that nested
columns use. [TBD: data]

Supplementary Table 3: Views written by the `qpxc convert` commands of QPX 1.4.0. Yes: written. In:
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
view; producers write it through the `qpx` Python API. OpenMS can also write QPX directly.

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

Supplementary Figure 1: Query time and storage of QPX compared with mzTab and CSV outputs.
[TBD: figure]

Supplementary Figure 2: Views and files held by each dataset. Each row is a dataset, grouped by
processing route; a filled cell marks a view or file present in the latest QPX version of the
dataset, except for the SDRF column, which marks an SDRF anywhere in the dataset folder. The
row under each route gives the number of its datasets holding each view or file, and the last
row the number over all datasets. [TBD: figure]
