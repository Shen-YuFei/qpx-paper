# Supplementary Information

Supplementary Table 1: Views written by the `qpxc convert` commands of QPX 1.4.0. Yes: written. In:
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
[TODO: figure from the rerun benchmark. Rerun `scripts/benchmark/benchmark.py` with QPX 1.4.0
and a current DuckDB, on both the default converter output (Zstandard, per-column encodings)
and the output of `qpxc transform relayout` (sorted, renumbered, rounded, structure lists),
state for each the codec, row-group sizes and layout, add memory use and tool-native outputs,
and report the hardware. The earlier numbers, from Snappy-compressed files written by an
earlier QPX release, are in commit a82ea5f.]
