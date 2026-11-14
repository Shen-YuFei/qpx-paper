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
