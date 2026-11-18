# Figure Legends

![](figures/fig1){width=100%}

Figure 1: Overview of the corpus and of the QPX format. Public datasets from ProteomeXchange
repositories and other sources, annotated with SDRF-Proteomics files, were processed along
three routes (identification only with the `quantms-msnet` recipe, DIA with quantmsdiann and
DDA with quantms) and written as one QPX folder per dataset, holding the Parquet views, grouped
here by content, together with the SDRF and expression files. The data are read with the QPX
Explorer of the quantms portal, the QPX UI desktop viewer, SQL engines such as DuckDB or the
`qpx` Python package. Colours mark the processing routes, as in Fig. 2.

![](figures/fig2){width=100%}

Figure 2: Composition of the corpus. The 103 datasets by hosting repository (a), year of first
public release (b), organism (c), instrument family (d), acquisition and labelling as annotated
in the SDRF (e) and number of runs (f), coloured by processing route. Release dates are those
of the first announcement in ProteomeCentral or of the release by MassIVE or the PDC; nine
datasets have none. Datasets with several organisms or instrument families are counted once,
under Several. In f, each point is a dataset and the vertical bars mark the route medians.
Numbers are from the 29 October 2026 snapshot and provisional until the corpus is regenerated.

Figure 3: Identification and quantification statistics per dataset. a, Distinct target
peptidoforms per run, from the psm view, or from the feature view for DIA-NN, which writes no
psm view. b, Protein groups with a quantity per quantification unit (the runs combined into one
quantity, and the label for TMT). c, Completeness of the protein group by unit matrix. d,
Median precursor mass error of the PSMs, from their observed and calculated m/z. Each point is
the median over the runs or units of one dataset; vertical bars mark the route medians. Rows
with a q-value above 0.01 are dropped where the views carry q-values. [TODO: figure from the regenerated corpus;
the script has been run on four datasets only.]

![](figures/fig4){width=100%}

Figure 4: One dataset in the two viewers. PXD048538, processed with DIA-NN, opened in the QPX
Explorer of the quantms portal (a, overview page) and in the QPX UI desktop viewer (b, the
sample view). [TODO: retake once the corpus is regenerated; the screenshots show dataset
version e60b9e9aa4c8 and QPX UI commit fff2999.]
