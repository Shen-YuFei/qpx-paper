# Background & Summary

Mass spectrometry (MS)-based proteomics data are now routinely deposited in public
repositories. The ProteomeXchange consortium coordinates submission and dissemination across
its member resources, and PRIDE, its largest member, holds tens of thousands of datasets
[@Deutsch_2022; @Perez_Riverol_2024]. Raw files are the most complete record of an
experiment, but they are rarely what a reuser needs. Most reuse, from building expression
atlases to training machine learning models, starts from identified and quantified
peptides and proteins, and these results are scattered across the native outputs of the
search and quantification tools used in each study, such as MaxQuant, FragPipe, DIA-NN and
OpenMS [@Cox_2008; @Kong_2017; @Demichev_2019; @Pfeuffer_2024]. Each tool writes its own
tables with its own column names, identifier conventions and levels of error control, so
results from different studies cannot be combined without per-tool parsing and, in practice,
without reprocessing the raw data.

Reprocessing public data with a uniform workflow removes much of this heterogeneity. Earlier
efforts reanalysed public datasets to build baseline protein expression resources and
integrate them into Expression Atlas [@Jarnuczak_2021; @Walzer_2022], and the quantms
workflow made such reanalysis practical at scale by running DDA and DIA analyses
reproducibly on high-performance and cloud infrastructure [@Dai_2024]. Sample metadata
annotated in the SDRF-Proteomics format link each MS run to its biological sample and
experimental design [@Dai_2021]. The remaining bottleneck is the representation of the
results. The community standard for reporting final results, mzTab [@Griss_2014], is a
tab-separated text file that interleaves protein, peptide and PSM sections. It was designed
for exchanging and reading results of a single study, not for querying hundreds of millions
of records across many studies: every query requires decompressing and parsing the whole
file, and files grow quickly with the number of runs.

Here we describe QPX, an open format for MS-based proteomics results, and a corpus of public
datasets reprocessed and stored in it. QPX splits results into views, each stored as an
Apache Parquet table with a typed schema: PSMs, quantified peptide features, protein groups,
a peptide-to-protein map, modification sites and proteoforms, together with sample, run,
dataset, ontology and provenance metadata. Peptidoforms are written in ProForma notation
[@LeDuc_2022], metadata fields are mapped to PSI-MS and other controlled vocabulary terms
[@Mayer_2013], and the original SDRF is kept alongside the Parquet files. Expression results
are exported as AnnData and MuData objects for use with single-cell and multi-omics analysis
tools [@Virshup_2024; @Bredikhin_2022]. Because Parquet is a columnar format with
per-column statistics, analytical engines such as DuckDB [@Raasveldt_2019] can answer typical
queries by reading only the columns and row groups they need. Converters write QPX from the
outputs of the main DDA and DIA tools, so the format is not tied to one workflow. QPX does
not replace mzTab; it is a performance-oriented layer for integrating results across tools
and studies, in the spirit of community data structures such as BIDS in neuroimaging
[@Gorgolewski_2016] and of the FAIR principles [@Wilkinson_2016].

The corpus contains 103 public datasets with 23,204 samples and 51,023 MS runs
[TODO: update after regeneration]. Forty-six datasets carry full quantification results: 27
processed with DIA-NN and 19 (10 label-free and 9 TMT) processed with the OpenMS-based
quantms workflows for DDA data. The remaining 57 datasets provide identification results
only, about 500 million PSM records. All files are available over HTTP and can be explored in
the browser with the QPX Explorer of the quantms portal or queried directly with SQL. We
expect the corpus to support cross-study protein expression atlases, meta-analyses,
benchmarking of quantification methods and the training of machine learning models for
peptide property prediction and PSM rescoring.
