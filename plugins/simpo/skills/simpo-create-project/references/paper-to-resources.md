# Paper-to-resource evidence map

The unified workflow creates dependent resources in this order. There may be
multiple DataSets and Projects for one paper:

```text
paper and supplements
       |
       +--> BioModel Draft -------------------+
       |                                      +--> Project Draft (per pairing/variant)
       +--> DataSet Draft (per experiment) ---+
```

Do not create a Project until its source BioModel and DataSet Drafts are
accepted. A Project uses the BioModel and DataSet IDs returned by SIMPO; it is
not a second copy of their JSON. Distinct experiments, initial conditions,
source studies, or calibration/validation roles normally require distinct
DataSets. Alternative equation variants normally require distinct Projects and
may require distinct BioModels.

## Evidence map

Keep a machine-readable or Markdown map with one row per nontrivial value:

| Resource | Field/table | Value | Classification | Source | Transformation | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| DataSet | Measured/S_NH4 | ... | digitized | Fig. 4b, p. 7 | calibrated CSV | medium |

Use these classifications exactly:

- `reported`: stated in text, table, equation, caption, or supplement;
- `calculated`: calculated from reported values with a visible formula;
- `digitized`: reconstructed from plotted pixels after calibration;
- `assumed`: added only after the user approves an engineering assumption;
- `unresolved`: required but not established by the source.

Record original units and converted units. A conversion does not change the
classification of the underlying value.

## Object boundaries

BioModel contains the biological state variables, parameters, equations,
stoichiometry, Composition, and Ionization supported by the model paper.

DataSet contains the documented process train, tanks, streams, operating
conditions, influent/measurement time series, and figure-derived observations
for one compatible scenario or explicitly linked reactor group. Do not combine
unrelated figures merely because they use the same symbols.
Do not copy kinetic equations into DataSet tables. Do not map aggregate water
quality to model components without a characterization basis or explicit user
approval.

Project contains the Solution generated from the selected BioModel and DataSet.
Use the backend-generated Solution unless the source and user provide enough
evidence for reviewed Variable, Target, Conversion, and Weight edits.

Each object's Markdown Description is part of the evidence package. BioModel
Description records model and Composition/Ionization derivations; DataSet
Description records figure calibration, source classifications, grouping, and
hydraulic assumptions; Project Description records linked IDs, figure roles,
variables, calculation settings, and comparison conclusions. Store reviewed
reasoning and decisions, not private conversational chain-of-thought.

## Dependency and failure handling

1. Validate the BioModel JSON and DataSet JSON independently.
2. Create each as a Private version-0 Draft and record its returned ID.
3. Check that both IDs refer to the intended owned Drafts before Project create.
4. If Project creation fails, leave the earlier Drafts intact and report the
   exact dependency or parser error. Do not recreate them blindly.
5. Never release any of the three resources automatically.

Parser acceptance only proves that SIMPO can represent the JSON. It does not
prove that the paper was reproduced, that digitized points are exact, or that a
simulation will meet the paper's performance claims.
