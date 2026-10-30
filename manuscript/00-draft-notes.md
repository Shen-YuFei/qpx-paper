# Draft notes (remove before submission)

This is the first draft of the Data Descriptor.
Text in square brackets starting with TODO needs input from the named people or a decision
from the team.

- **Corpus numbers are provisional.** They come from a read-only inventory of
  browse.quantms.org taken on 29 October 2026, using the most recent QPX version of each
  dataset (`data/portal-snapshot-2026-10-29`). Of these 103 versions, 54 were written with
  QPX specification 1.0.1, 24 with 1.0.2 and 25 with 1.1. The deposited record should be
  regenerated with the QPX release cited in the paper (1.2.0 or later), and every number
  updated from the regenerated files.
- **MSNet subset.** 57 of the 103 datasets (88% of the PSM records and 94% of the bytes)
  were produced by the `quantms-msnet` recipe and contain identifications only. What MSNet
  is, how these datasets were searched, and whether they belong in the deposited record
  needs to come from the people who produced them.
- **Not yet in the portal.** No dataset in the snapshot is identifiable as
  immunopeptidomics, and the dataset folders hold no pmultiqc reports. The planned paper
  covers both, so either the data are added before deposition or these parts are cut.
- **Specification version.** The package on main still writes `qpx_version` 1.1, although
  the site and proteoform views were added after the 1.1.6 release. Decide whether the
  release cited here also bumps the specification version.
