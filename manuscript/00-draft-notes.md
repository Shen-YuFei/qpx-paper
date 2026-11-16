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
- **QPX UI.** The desktop viewer is described in the Usage Notes and Fig. 5; decide the
  version cited and whether its authors join the author list.
- **Check of 16 November 2026.** Reading the draft against the journal's referee questions and
  the 29 October snapshot turned up the following; each needs a decision or the regenerated
  corpus.
  - *Dataset parts counted as versions.* Some datasets were processed in parts (by organism,
    enzyme or fragmentation), each in its own hash folder, and taking the latest folder keeps
    one part: PXD012636 keeps Rat and drops Homo, Mouse, Pig, Horse and Danio rerio;
    PXD004452 keeps the GluC part (154,347 PSMs) and drops the main part (5.5 million);
    PXD024364 keeps LysC and drops Trypsin (7.1 million); PXD019483 keeps RVFV (1,429 PSMs)
    and drops the main part (4.0 million); PXD000865 keeps LysC. Every corpus number depends
    on this; "zebrafish" in Methods occurs only in dropped parts.
  - *Truncated feature views.* The latest versions of PXD025864, PXD027008 and PXD028251 have
    exactly 500,000 feature rows, the signature of the quantms converter bug fixed in QPX
    1.1.0 (commit 77a79412: rows cut at 500,000 and duplicated). The benchmark input
    (PXD007683, "500,000 features"; the source has 425,594) has the same defect, and
    PXD007683 is not in the corpus.
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
    limited to 110 characters; the abstract has 178 words against a recommended 170; summary
    statistics such as Table 1 belong in the optional Data Overview section (one paragraph and
    one or two tables or figures), not in Data Records; every input dataset is to be cited in
    the journal's data citation format; Data Availability and Funding sections are required
    (placeholders added).
