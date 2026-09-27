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
Before using the backend-generated Solution, close the Target/Conversion mapping
for every DataSet Target. The backend's blank/default Conversion is identity-only:
it fills `1` when a Target symbol is exactly the same as a BioModel Component,
but it does not infer aggregate targets. A Target may be present structurally
while its entire Conversion row is empty, which is not a usable scientific
mapping.

For aggregate Targets, derive a row only from an explicit source definition,
BioModel Composition, or transparent unit conversion. Conversion cells may be
literal numbers, exact expressions, or direct BioModel Parameter references.
Preserve a defined Parameter such as `i_N_S_U` in the submitted row instead of
evaluating it to a default or rounded number. The calculation resolves it from
the current Project Variable values. Verify the Parameter exists, evaluates to
a finite value, and is unit-compatible before submission. Use the following
common patterns only when their stated basis is satisfied:

| Target | Mapping rule |
| --- | --- |
| `COD`/`TCOD` | Sum the Components that the source defines as COD. For the standard ASM2D influent example this can be `S_F + S_VFA + S_U + X_U_E + X_B`; add biomass or other fractions only when documented. |
| `SCOD` | Sum the documented soluble COD Components only; exclude particulate `X_*` terms. |
| `TIN` | `S_NHx + S_NOx`, or `S_NH4 + S_NO2 + S_NO3` for separate species, on the same `gN/m3` basis. Exclude `S_N2` unless the source includes dissolved N2 in TIN. |
| `TN` | Sum inorganic nitrogen and source-defined organic-nitrogen Composition terms; it is not interchangeable with TIN. |
| `TP` | Include `S_PO4` plus all documented organic-phosphorus and polyphosphate terms, such as `X_PAO_PP`. |
| `TSS` | Use documented `i_TSS_*` coefficients for particulate Components; dissolved Components are normally zero. |
| `TS` | In this BioModel context, treat as total sulfur. Sum sulfur-bearing Components using the BioModel `S` Composition coefficients or source-defined sulfur species; do not treat it as total solids. |

Apply the same procedure to any Target not listed above:

1. Resolve its meaning from `Symbol`, `Name`, `Description`, units, and the
   source definition; do not classify it from the abbreviation alone.
2. Match direct Components first. For an aggregate, select only Components
   explicitly included by the source or the relevant Composition row.
3. Apply the reported or derived coefficient or Parameter expression and any
   declared unit factor, then verify that every referenced Component and
   Parameter exists in the BioModel and that the output unit matches the DataSet
   Target unit.
4. Reject an empty/all-zero row, conflicting candidate formulas, or an
   underdetermined fractionation. If the relation is nonlinear or requires a
   state/measurement absent from the BioModel, Conversion cannot represent it;
   record the row as `unresolved` until the user or source resolves it.

Record the formula, units, source definition, and classification (`calculated`
or `reported`) in the Project Description and evidence map. A formula with
several components is still not a unique influent fractionation: if measured
aggregate Targets do not determine all component values, retain the residual
and disclose the approved assumptions.

Use the backend-generated Solution only when all targets are direct compatible
components or when no custom Target/Conversion mapping is needed. Otherwise
submit a reviewed complete `Variable`, `Target`, `Conversion`, and `Weight`
detail with `--json`. If a derived Target cannot be mapped from the selected
BioModel and source definition, stop with `unresolved` rather than submitting an
empty Conversion row.

When assembling a custom `Conversion` table, retain the BioModel Component
header exactly and retain one row for every DataSet Target. For example, with
components `S_NHx`, `S_NOx`, and `S_N2`, the standard `TIN` row is:

```text
header: [Target, S_NHx, S_NOx, S_N2]
TIN:    [TIN,    1,     1,     0]
```

Use numeric zero for non-participating cells and preserve any additional
components in the header. This is the mapping to submit, not merely a note in
the Description. Check every resulting matrix row before `create-project`; an
empty or all-blank aggregate row means the Project is not ready.

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
