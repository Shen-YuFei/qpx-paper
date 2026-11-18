# Draft notes (remove before submission)

This is the first draft of the Data Descriptor.
Text in square brackets starting with TODO needs input from the named people or a decision
from the team.

- **Corpus numbers are provisional.** They come from a read-only inventory of
  browse.quantms.org taken on 29 October 2026, using the most recent QPX version of each
  dataset (`data/portal-snapshot-2026-10-29`). Of these 103 versions, 54 were written with
  QPX specification 1.0.1, 24 with 1.0.2 and 24 with 1.1; one mixes 1.0.2 and 1.1 files.
  The deposited record should be regenerated with QPX 1.4.0, the release cited in the paper,
  and every number updated from the regenerated files.
- **MSNet subset.** 57 of the 103 datasets (88% of the PSM records and 94% of the bytes)
  were produced by the `quantms-msnet` recipe and contain identifications only. What MSNet
  is, how these datasets were searched, and whether they belong in the deposited record
  needs to come from the people who produced them. Lead to confirm: the QPX UI README calls
  PSM views that store fragment peaks the π-MSNet collection
  (https://github.com/PHOENIXcenter/pi-MSnet).
- **Not yet in the portal.** No dataset in the snapshot is identifiable as
  immunopeptidomics, and the dataset folders hold no pmultiqc reports. The planned paper
  covers both, so either the data are added before deposition or these parts are cut.
- **Release.** The paper cites QPX 1.4.0, which writes specification version 1.3 and is not
  released yet. After the release, fill in its date, check the container image and the Zenodo
  DOI, and check the views, converters and options described here against the released
  documentation. QPX 1.2.0 (30 October 2026) and 1.3.0 (7 November 2026) write specification
  1.2; 1.3.0 added the `xic` view.
- **QPX UI.** The desktop viewer is described in the Usage Notes and Fig. 4; decide the
  version cited and whether its authors join the author list. Fig. 4b shows the main branch at
  commit fff2999 (10 November 2026), newer than and different from the only release, v0.2.0;
  a release from main is needed before it can be cited.
- **Figures (17 November 2026).** Scripts in `scripts/figures/` draw every figure in one style
  (Liberation Sans, 5.5-6.5 pt with panel letters at the size of the panel titles, as the
  journal asks, Okabe-Ito colours for the three routes, embedded TrueType fonts).
  - Fig. 1 is final apart from wording. Fig. 2 is drawn from the snapshot; panel f shows runs,
    not samples, because six identification-only datasets record one sample for up to 1,460
    runs. Its repositories and release dates are in `data/dataset_public_dates.csv`, with
    sources. Nine datasets have no date: the two HuiYan datasets, PMID23933261 (dated only by
    its 2013 paper), PDC000127 (first released on the former CPTAC Data Portal) and five iProX
    subprojects whose release iProX does not return. Methods count datasets by accession (89
    PXD), Fig. 2a by hosting repository (87 PRIDE, 2 of the PXD datasets in MassIVE).
  - Fig. 3 (`qc_stats.py`, then `fig3_quality.py`) needs the regenerated corpus. It was tried
    on four datasets migrated to specification 1.3 (one per route, plus TMT). Two choices to
    confirm: rows are cut at q <= 0.01 where q-values exist, because the pipelines export at 1%
    or 5% (TMT PSMs and DIA-NN precursors and protein groups reach 0.05); and the mass error
    leaves out DIA-NN, whose feature view has no psm and whose `mass_error_ppm` is near zero, as
    is that of the OpenMS feature view.
  - Fig. 4 uses screenshots taken by the Portal session (scripts and notes in
    `/data/shenyufei/Bigbio_data/qpx_paper_figures/fig4/`). At 183 mm they are 289 dpi; retake
    at 3x scale for the final version. The Explorer shows a notice that the portal catalogue
    lists PXD048538/41b03dd48c8b as the current version, while the corpus takes e60b9e9aa4c8,
    published later on 28 September 2026; the two disagree on which version is current.
- **Check of 16 November 2026.** Reading the draft against the journal's referee questions and
  the 29 October snapshot turned up the following; each needs a decision or the regenerated
  corpus.
  - *Dataset parts counted as versions.* Some datasets were processed in parts (by organism,
    enzyme or fragmentation), each in its own hash folder, and taking the latest folder keeps
    one part: PXD012636 keeps Rat and drops Homo, Mouse, Pig, Horse and Danio rerio;
    PXD004452 keeps the GluC part (154,347 PSMs) and drops the main part (5.5 million);
    PXD024364 keeps LysC and drops Trypsin (7.1 million); PXD019483 keeps RVFV (1,429 PSMs)
    and drops the main part (4.0 million); PXD000865 keeps LysC. Every corpus number depends
    on this; "zebrafish" in Methods occurs only in dropped parts. If the parts do not overlap,
    the rule leaves out 54 parts of 8 datasets with 626 samples, 2,269 runs and 25.4 million PSM
    rows; the snapshot keeps no run file names, so overlap could not be checked.
  - *Truncated feature views.* The latest versions of PXD025864, PXD027008 and PXD028251 have
    exactly 500,000 feature rows, the signature of the quantms converter bug fixed in QPX
    1.1.0 (commit 77a79412: rows cut at 500,000 and duplicated). The earlier benchmark numbers for
    PXD007683 (500,000 features, see a82ea5f; commit 77a79412 gives 425,594 for its source) fit the
    same defect, and PXD007683 is not in the corpus.
  - *DIA-NN subset.* Seven DIA-NN datasets (PXD000672, PXD003497, PXD004684, PXD018830,
    PXD021394, PXD027817, PXD028618; 4.8 million rows) have a psm view with exactly as many
    rows as the feature view, written through the quantms route of qpx 1.0.2, whereas Methods
    says DIA-NN conversions have no psm view. Thirteen of the 27 record a
    `quantmsdiann-2.5.1-enterprise` recipe, so Methods should say which DIA-NN build was used.
  - *Counts.* HuiYanAstralMouse has no pg view, so 45, not 46, datasets carry protein
    quantification. The TMT counts in Background (9) and Methods (7 + 1) use different bases.
  - *Layout.* In 18 of the 103 latest folders the views sit in a nested `qpx/` folder next to
    mzTab, MSstats and SDRF files; 3 use the prefix `openms`; several split the PSM view
    (`-P1`, `-P2`, ...) or carry part suffixes; 42 hold an SDRF. Background and Methods say the
    SDRF is kept next to the views, Data Records says it is in a separate subfolder.
  - *Provenance and code.* The 57 MSNet datasets were written by `scripts/convert_msnet.py` in
    the QPX repository, which is not a `qpxc` command and is not named in Code Availability.
    The dataset view of all 103 latest versions leaves the title, description and PubMed ID
    empty.
  - *Sample annotations.* Organism values differ in case ("Homo sapiens", "homo sapiens",
    "Homo Sapiens"), PXD010595 and PXD019643 have "unknown", PXD019483 gives "Rift valley
    Fever", and the PXD054415 samples list strains that count up ("Escherichia coli K24",
    "K25", ...), which looks like a spreadsheet fill in the SDRF.
  - *Journal format.* Titles may not contain colons or self-constructed acronyms and are
    limited to 110 characters, so the title "QPX: a columnar format and a corpus of reprocessed
    public proteomics data for large-scale reuse" was replaced (co-authors to confirm); the
    abstract was cut below the recommended 170 words by dropping the query-speed claim, whose
    numbers come from the defective PXD007683 conversion; summary
    statistics such as Table 1 belong in the optional Data Overview section (one paragraph and
    one or two tables or figures), not in Data Records; every input dataset is to be cited in
    the journal's data citation format; Data Availability and Funding sections are required
    (placeholders added).
- **Software content trimmed (16 November 2026).** The software material was cut until two
  review agents, one reading as a data reuser and one as an editor, both judged it appropriate
  for a Data Descriptor (five rounds; commits 06fd7a5 and 61b5363; the verdict applies to
  5714e54). Cut: the converter sentence in the abstract; the encoding details, the
  specification 1.3 changelog, the open-development sentence and the `qpxc validate` options in
  Methods; the `llms.txt` and MCP sentences and the feature lists of the two viewers in Usage
  Notes; the benchmark, now Supplementary Fig. 1 and still to be rerun, so Figs 4 and 5 became
  Figs 3 and 4. Added: how the views join, and TODOs on the conversion route, views, relayout,
  decoys, q-value levels and primary quantities of each subset. Anything cut can be restored
  from a82ea5f. The agents had also cut the converters, which left no statement that the
  outputs of other tools can be converted; at the drafting author's decision, and against both
  round-3 reviewers, they were then brought back as a shorter sentence in Background, the list
  of converters with its citations in Methods, and the former Table 3 as Supplementary Table 1.
  The agents did not review this version. The abstract still does not name the converters
  (co-authors to confirm). Once the TODOs are resolved, the relayout and `qpxc migrate`
  passages should say what was done to the deposited files, and views absent from the deposit
  could shrink to one sentence. Remarks not acted on: move the `qpxc validate` description to
  Technical Validation; say how `provenance.json` relates to the provenance view; add a second
  SQL example that joins feature intensities to samples.
