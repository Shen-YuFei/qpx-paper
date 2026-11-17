# Methods

## Dataset selection

The corpus comprises 103 datasets: 89 from ProteomeXchange (PXD accessions) [@Deutsch_2025], 8 from
iProX [@Chen_2021], 2 from the CPTAC Proteomic Data Commons [@Thangudu_2024], 1 from MassIVE and 3 from other sources
[TODO: name the sources of the HuiYan and PMI datasets]. [TODO (Yasset, Chengxin): the
criteria used to select datasets for reprocessing, e.g. availability of raw files, an SDRF
annotation, supported instrument and acquisition type.] Eighty-two datasets include human
samples and seven mouse samples; the others cover plants, yeast, *Drosophila*, zebrafish,
other vertebrates, bacteria and viruses. The most common instruments are Orbitrap Fusion,
Q Exactive HF, Q Exactive, Orbitrap Fusion Lumos and Q Exactive HF-X.

According to the acquisition method annotated in their SDRF files, 60 datasets were acquired
in data-dependent mode (52 label-free, 7 TMT-labelled and 1 with both label-free and TMT
runs) and 24 in data-independent mode; 4 datasets contain both DDA and DIA runs, and 15
have no acquisition method annotated. None of the SDRF files describes an MHC enrichment,
so the snapshot contains no dataset that can be identified as immunopeptidomics. [TODO:
provisional counts from the 29 October 2026 snapshot; 8 datasets have conflicting
annotations between SDRF versions or between the SDRF and the repository metadata, listed in
`data/portal-snapshot-2026-10-29/acquisition_latest.csv`.]

## Sample metadata annotation

Each dataset is described by an SDRF-Proteomics file [@Dai_2021], which lists one row per MS
run and label channel and records the organism, tissue or cell type, disease, instrument,
labelling, enzyme, modifications and other experimental factors using ontology terms. SDRF
files are curated in the community repository of annotated datasets
(https://github.com/bigbio/sdrf-annotated-datasets) and validated with sdrf-pipelines
(https://github.com/bigbio/sdrf-pipelines). [TODO: confirm that every deposited dataset
went through this route, and describe the curation and review process.] The SDRF drives
both the processing workflows, which read search parameters and the experimental design
from it, and the QPX sample and run views, which keep the curated values as text; the run view also stores the
ontology terms of run-level values such as the instrument, and the ontology view maps the
columns of each view to controlled vocabulary terms.

## Data processing workflows

Datasets were processed with Nextflow workflows that follow nf-core practices
[@Di_Tommaso_2017; @Ewels_2020] and run every tool from a versioned container, which fixes the
software version of each step and lets the same workflow run on a laptop, a cluster or the cloud.

DDA datasets were processed with quantms [@Dai_2024], which is built on OpenMS
[@Pfeuffer_2024]. [TODO: search engines, rescoring, FDR thresholds and quantification
methods used for label-free and TMT data, and the quantms versions; the provenance view
records them per dataset.] DIA datasets were processed with the DIA-NN-based quantms
workflow (quantmsdiann) [@Demichev_2019]. [TODO: DIA-NN versions and library-free or
library-based search settings.] The identification-only datasets were produced with the
`quantms-msnet` recipe. [TODO (Yasset, Chengxin): describe MSNet and how these datasets were
searched.] [TODO (Jonas Scheid): immunopeptidomics datasets processed with nf-core/mhcquant
[@Bichmann_2019; @Scheid_2025], including non-specific digestion searches and HLA annotation.]

Each dataset records its processing chain in the QPX provenance view: the tools and, where
the source provides them, their versions, parameters and FDR thresholds.

## The QPX format

QPX organises the results of one dataset into views (Table 2). Data views hold
identification and quantification results: `psm` holds peptide-spectrum matches with scores
and, optionally, fragment peak arrays; `feature` holds identified and quantified peptide
features per run, with a quantity for each label channel and the origin of each
identification (direct, transferred between runs, or secondary, from a co-fragmenting
peptide of a chimeric spectrum); `pg` holds protein groups and their
quantities; `pepmap` is a deduplicated peptide-to-protein map and `protein` annotates the
proteins from the sequence database; `site` and `proteoform` hold modification-site and
proteoform claims with their own error control; `fragment` and `xic` hold fragment ion
quantities and extracted ion chromatograms of DIA analyses; and `mz` holds MS1 and MS2
spectra. Metadata views describe the samples (`sample`), the MS runs and their link to
samples and channels (`run`), the project and its publication (`dataset`), the controlled
vocabulary terms of its columns and scores (`ontology`) and the processing chain (`provenance`).
Absolute and differential expression results are stored as AnnData files (`.h5ad`)
[@Virshup_2024], and the quantification results of a dataset can be exported as a single
MuData file (`.h5mu`) [@Bredikhin_2022]. The original SDRF is kept next to the views. Parquet
views are named `{PREFIX}.{view}.parquet`, for example `PXD014414.feature.parquet`.

Each view has a schema, shipped with the QPX package as a YAML definition, that fixes the
column names and types, including nested types: a feature's intensities, for example, are a
list of (label, intensity) pairs that join to the label channels declared in the run view, and
a channel that was identified but not quantified has a null intensity. Peptidoforms are written
in a canonical ProForma 2.0 form [@LeDuc_2022], with fixed modifications and labels written
inline and modifications as Unimod accessions, so the same peptidoform has the same string
whichever tool reported it. Scores and tool-specific parameters are stored as name-value pairs,
and the ontology view maps their names to PSI-MS and other controlled vocabulary terms where a
mapping exists [@Mayer_2013]. The schema distinguishes three kinds of column: required columns
must be present and non-null, nullable columns must be present but may be null, and optional
columns may be left out of a file. Each Parquet file stores the specification version
(`qpx_version`) and the writing software in its file-level metadata, and every column carries
its description in the field metadata, so a file can be interpreted without the specification
at hand.

Converters write Parquet files compressed with Zstandard, in row groups of at most 131,072
rows. Before publication, `qpxc transform relayout` can rewrite a dataset for faster selective
reads: it stores the rows of one peptide or protein together, numbers the feature,
protein-group and PSM identifiers in the new row order, stores score and parameter lists whose
entries have the same names in every row as structures with one field per name, and rounds
measured values, keeping 12 mantissa bits for intensities and mass errors and 16 for retention
times, ion mobilities and collisional cross sections (a relative error of at most 2^-13^ and
2^-17^), while scores, q-values and m/z values are left untouched. Each step is recorded in the
file metadata, and the `qpx` package reads such files back in the logical layout.

The specification uses a `{major}.{minor}` version. During the current stabilisation period on
the 1.x line, a minor version may change the data model; readers check the `qpx_version` of
each file. This paper describes specification 1.3, written by QPX 1.4.0, which added the
`fragment` and `protein` views, typed q-value columns and the origin of feature
identifications, and changed how peptidoforms are written and row identifiers derived, so files
converted again with 1.4.0 have new identifiers. `qpxc migrate` rewrites an older dataset into
a new folder under the current specification, but it cannot add information that the older
files did not store, so converting again from the tool outputs is preferred where they exist.
The specification, schemas, reference implementation and documentation are developed in the
open on GitHub under the Apache 2.0 licence, and changes go through public pull requests and
review. The `qpxc validate` command checks a dataset against the schemas: column presence and
types, nulls in required columns and nested fields, primary-key uniqueness, value ranges, file
metadata and references between views; on request it also checks consistency across views and
derives the row identifiers again.

## Conversion from third-party tools

The `qpxc convert` commands write QPX from the outputs of MaxQuant, FragPipe, DIA-NN,
Spectronaut [@Bruderer_2015], Proteome Discoverer (text exports) [@Orsburn_2021], OpenMS
(consensusXML), CPTAC CDAP [@Rudnick_2016], mzIdentML [@Vizcaino_2017] and the quantms MSstats
input table [@Kohler_2023] (Table 3); OpenMS can also write QPX directly. Converters map each
tool's columns to QPX fields, rewrite modification notation into the canonical ProForma form,
convert units such as retention time in minutes to seconds, and take the sample and run
metadata from an SDRF where one is given. When the source does not report a value, the field is
left null rather than estimated: DIA-NN reports, for example, have no PSM-level table, so
DIA-NN conversions have no `psm` view. Values that a converter derives are labelled as such:
when a consensusXML file reports no protein abundance, the protein-group intensity is the sum
of its unique peptides and is marked with that quantification method. The documentation lists,
per converter, which views are written and where each field comes from.

## Quality control

[TODO: pmultiqc [@Yue_2026] (https://github.com/bigbio/pmultiqc), a MultiQC [@Ewels_2016] plugin,
summarises identification rates, missing values, mass error and retention time per run.
The dataset folders in the snapshot contain no pmultiqc reports; decide whether to generate
them for every deposited dataset and describe the metrics here.]
