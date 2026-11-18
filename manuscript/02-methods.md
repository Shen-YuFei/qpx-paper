# Methods

## Dataset selection

The corpus comprises 103 datasets: 89 from ProteomeXchange (PXD accessions) [@Deutsch_2025], 8 from
iProX [@Chen_2021], 2 from the CPTAC Proteomic Data Commons [@Thangudu_2024], 1 from MassIVE and 3 from other sources
[TODO: name the sources of the HuiYan and PMI datasets]. By hosting repository, 87 datasets
are in PRIDE, 8 in iProX, 3 in MassIVE and 2 in the PDC (Fig. 2a). [TODO (Yasset, Chengxin): the
criteria used to select datasets for reprocessing, e.g. availability of raw files, an SDRF
annotation, supported instrument and acquisition type.] Eighty-two datasets include human
samples and seven mouse samples; the others cover plants, yeast, *Drosophila*, zebrafish,
other vertebrates, bacteria and viruses. The most common instruments are Orbitrap Fusion,
Q Exactive HF, Q Exactive, Orbitrap Fusion Lumos and Q Exactive HF-X (Fig. 2c,d).
Supplementary Table 1 lists every dataset with its accession, hosting repository and original
publication, and the deposited data of each dataset are cited individually [@ds_IPX0000937000; @ds_MSV000085836; @ds_PXD000561; @ds_PXD000612; @ds_PXD000672; @ds_PXD000865; @ds_PXD002137; @ds_PXD002395; @ds_PXD002767; @ds_PXD002854; @ds_PXD002899; @ds_PXD003497; @ds_PXD003539; @ds_PXD003903; @ds_PXD003947; @ds_PXD004242; @ds_PXD004452; @ds_PXD004683; @ds_PXD004684; @ds_PXD004701; @ds_PXD004732; @ds_PXD005526; @ds_PXD006225; @ds_PXD006675; @ds_PXD008333; @ds_PXD008722; @ds_PXD008840; @ds_PXD009348; @ds_PXD009449; @ds_PXD009737; @ds_PXD010154; @ds_PXD010429; @ds_PXD010595; @ds_PXD010899; @ds_PXD010957; @ds_PXD011821; @ds_PXD011896; @ds_PXD012131; @ds_PXD012174; @ds_PXD012574; @ds_PXD012636; @ds_PXD013231; @ds_PXD013658; @ds_PXD013868; @ds_PXD014145; @ds_PXD014404; @ds_PXD014414; @ds_PXD014525; @ds_PXD014877; @ds_PXD016986; @ds_PXD017199; @ds_PXD018450; @ds_PXD018830; @ds_PXD019483; @ds_PXD019643; @ds_PXD020109; @ds_PXD020192; @ds_PXD020248; @ds_PXD020252; @ds_PXD021013; @ds_PXD021394; @ds_PXD022469; @ds_PXD022992; @ds_PXD023508; @ds_PXD023662; @ds_PXD024364; @ds_PXD024742; @ds_PXD025864; @ds_PXD027008; @ds_PXD027817; @ds_PXD028251; @ds_PXD028618; @ds_PXD028735; @ds_PXD030304; @ds_PXD030348; @ds_PXD030671; @ds_PXD030983; @ds_PXD031498; @ds_PXD034656; @ds_PXD036643; @ds_PXD036826; @ds_PXD038732; @ds_PXD040266; @ds_PXD041047; @ds_PXD041268; @ds_PXD041421; @ds_PXD042233; @ds_PXD046290; @ds_PXD046320; @ds_PXD048538; @ds_PXD052856; @ds_PXD054415; @ds_PXD058009; @ds_PXD062529; @ds_PXD070780; @ds_PXD071155]. [TODO: data
citations for the five datasets whose repository records could not be retrieved: HuiYan-E480,
HuiYanAstralMouse and PMID23933261 have no repository accession, and the PDC records of
PDC000127 and PDC000219 name no contacts.]

According to the acquisition method annotated in their SDRF files, 60 datasets were acquired
in data-dependent mode (52 label-free, 7 TMT-labelled and 1 with both label-free and TMT
runs) and 24 in data-independent mode; 4 datasets contain both DDA and DIA runs, and 15
have no acquisition method annotated (Fig. 2e). None of the SDRF files describes an MHC enrichment,
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

QPX organises the results of one dataset into views (Table 1). Data views hold identification
and quantification results: `psm` holds peptide-spectrum matches with scores and, optionally,
fragment peak arrays; `feature` holds identified and quantified peptide features per run, with
a quantity for each label channel and the origin of each identification (direct, transferred
between runs, or secondary, from a co-fragmenting peptide of a chimeric spectrum); `pg` holds
protein groups and their quantities; `pepmap` is a deduplicated peptide-to-protein map and
`protein` annotates the proteins from the sequence database; `site` and `proteoform` hold
modification-site and proteoform claims with their own error control; `fragment` and `xic` hold
fragment ion quantities and extracted ion chromatograms of DIA analyses; and `mz` holds MS1 and
MS2 spectra, for example from mzML files [@Martens_2011]. Metadata views describe the samples
(`sample`), the MS runs and their link to samples and channels (`run`), the project and its
publication (`dataset`), the controlled vocabulary terms of its columns and scores (`ontology`)
and the processing chain (`provenance`). Absolute and differential expression results are
stored as AnnData files (`.h5ad`) [@Virshup_2024], and the quantification results of a dataset
can be exported as a single MuData file (`.h5mu`) [@Bredikhin_2022]. `qpxc convert` copies the
SDRF next to the views as `{PREFIX}.sdrf.tsv`. Parquet views are named `{PREFIX}.{view}.parquet`, for example
`PXD014414.feature.parquet`.

Each view has a schema, shipped with the QPX package as a YAML definition, that fixes the
column names and types, including nested types: a feature's intensities, for example, are a
list of (label, intensity) pairs that join to the label channels declared in the run view, and
a channel that was identified but not quantified has a null intensity. Peptidoforms are written
in a canonical ProForma 2.0 form [@LeDuc_2022], with fixed modifications and labels written
inline and modifications as Unimod accessions, so the same peptidoform has the same string
whichever tool reported it. Scores and tool-specific parameters are stored as name-value pairs,
and the ontology view maps their names to PSI-MS and other controlled vocabulary terms where a
mapping exists [@Mayer_2013]. The schema distinguishes three kinds of column: required columns
must be present and, unless declared nullable, non-null, nullable columns must be present but may be null, and optional
columns may be left out of a file. Each Parquet file stores the specification version
(`qpx_version`) and the writing software in its file-level metadata, and every column carries
its description in the field metadata, so a file can be interpreted without the specification
at hand. Supplementary Table 2, generated from the schemas, lists every column of every view with
its type, requirement and description.

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
each file. This paper describes specification 1.3, written by QPX 1.4.0; all files in the
deposited record follow it. Specification 1.3 introduced the canonical peptidoform described
above and derives row identifiers differently, so the peptidoform strings and row identifiers
of the deposited files can differ from those of older versions of the same dataset on the
quantms portal, and these columns cannot be used to join the two. [TODO: name the deposited
datasets that were rewritten with `qpxc migrate` because their tool outputs are no longer
available, and the information they lack; if every dataset was converted again, drop this and
at most point users holding older files to `qpxc migrate` in Usage Notes.] The `qpxc validate`
command checks a dataset against the schemas: column presence and types, nulls in required
columns and nested fields, primary-key uniqueness, value ranges, file metadata and references
between views; on request it also checks consistency across views and derives the row
identifiers again.

## Conversion from third-party tools

[TODO: name the converter or writer and the QPX release that produced each subset of the
deposited record.] The `qpxc convert` commands of QPX 1.4.0 read the outputs of MaxQuant,
FragPipe, DIA-NN, Spectronaut [@Bruderer_2015], Proteome Discoverer [@Orsburn_2021], OpenMS
(consensusXML), CPTAC CDAP [@Rudnick_2016], mzIdentML [@Vizcaino_2017] and the quantms MSstats
input table [@Kohler_2023]. Converters map each tool's columns to QPX fields, rewrite
modification notation into the canonical ProForma form, convert units such as retention time in
minutes to seconds, and take the sample and run metadata from an SDRF where one is given. When
the source does not report a value, the field is left null rather than estimated: DIA-NN
reports, for example, have no PSM-level table, so DIA-NN conversions have no `psm` view. Values
that a converter derives are labelled as such: when a consensusXML file reports no protein
abundance, the protein-group intensity is the sum of its unique peptides and is marked with
that quantification method. Supplementary Table 3 lists the views that each converter writes,
and the documentation lists where each field comes from.

## Quality control

[TODO: pmultiqc [@Yue_2026] (https://github.com/bigbio/pmultiqc), a MultiQC [@Ewels_2016] plugin,
summarises identification rates, missing values, mass error and retention time per run.
The dataset folders in the snapshot contain no pmultiqc reports; decide whether to generate
them for every deposited dataset and describe the metrics here.]
