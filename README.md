# QPX manuscript (Scientific Data, Data Descriptor)

Working draft of the QPX paper, a Data Descriptor for Scientific Data.

## Layout

- `manuscript/metadata.yaml` – title, authors, abstract, keywords.
- `manuscript/NN-*.md` – one file per section, concatenated in file-name order.
- `references.bib` – BibTeX entries fetched from Crossref by DOI.
- `figures/`, `data/`, `scripts/` – figure files, derived tables and the scripts that make them.
- `templates/` – Springer Nature LaTeX class `sn-jnl.cls` and `sn-nature.bst`
  (journal article template, December 2024), the pandoc LaTeX template, and
  `nature.csl` for the docx build.

## Build

Requires pandoc and tectonic (both in the Bigbio conda environment).

```bash
make docx   # build/qpx-paper.docx, for co-author comments
make pdf    # build/qpx-paper.tex and build/qpx-paper.pdf (sn-jnl, sn-nature)
```

Cite with pandoc syntax, e.g. `[@Dai_2024]`; the LaTeX build turns it into `\citep`.
