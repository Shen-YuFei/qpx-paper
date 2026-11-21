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

# Figure S1: Storage, query time and memory of QPX compared with the mzTab and MSstats tables

![](figures/figS1){width=100%}

One label-free analysis outside the corpus, of the 11 runs of PRIDE PXD007683
[@OConnell_2018; @ds_PXD007683] processed with quantms [@Dai_2024], read from its text outputs
(mzTab [@Griss_2014] and the MSstats input table) and from the same analysis converted from its
OpenMS consensusXML with `qpxc convert openms-consensus`, both as written and after
`qpxc transform relayout`. Colour marks what is read; open circles mark pandas and filled
circles DuckDB [@Raasveldt_2019]. **a**, File sizes, with the text files as written and
gzip-compressed (level 6). QPX files are Parquet with Zstandard compression. As written, the
views keep the order of the source in row groups of 100,000 rows; relayout sorts the psm view by
peptidoform, charge, run and scan and the feature view by protein, peptidoform, charge and run,
writes row groups of about 120,000 rows and rounds intensities and mass
errors to 12 mantissa bits and retention times to 16, leaving scores, q-values and m/z
unchanged. All results compares the consensusXML with every view written from it (psm, feature,
pg, dataset, ontology and provenance). **b**, **c**, Median wall time and increase in peak
resident memory over five runs of each query, each in a new Python process after the libraries
are loaded, on a warm page cache. PSM queries read the PSM section of the mzTab into pandas or
the psm view; feature queries read the MSstats table or the feature view. The queries count the
PSMs, the proteins they name and the PSMs of charge 2, read the sequence and charge of every PSM,
count the features, rank the ten proteins with the largest summed intensity and read the
features of one protein (UniProt P55011). Both sides return 542,403 PSMs, 9,716 proteins,
382,341 PSMs of charge 2 and the same ten proteins. Feature counts differ by design: the MSstats
table has one row per peptidoform, charge and run among the features assigned to a protein
(518,248 rows, 104 of them for P55011), whereas the feature view keeps all 573,203 consensus
features (111 for P55011), including 37,746 without an assigned protein. Conversion took 70 s
and relayout 3 s on one machine (Intel Core Ultra 7 270K Plus, 24 logical CPUs, 123 GiB memory,
Linux) with Python 3.13.9, DuckDB 2.0.0, pandas 2.3.3 and PyArrow 24.0.0; the benchmark script
is `scripts/benchmark/benchmark.py` in the paper repository. [TBD: rerun with the QPX 1.4.0
release; this run used QPX development commit 2dadc0e1.] MB, 10^6^ bytes; MiB, 2^20^ bytes;
PSM, peptide-spectrum match.

# Figure S2: Views and files held by each dataset

![](figures/figS2){width=100%}

Each row is a dataset, grouped by
processing route; a filled cell marks a view or file present in the latest QPX version of the
dataset, except for the SDRF column, which marks an SDRF anywhere in the dataset folder. The
row under each route gives the number of its datasets holding each view or file, and the last
row the number over all datasets. ID only, identification only; SDRF, Sample and Data
Relationship Format. [TBD: figure]
