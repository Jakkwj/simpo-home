# BioModel Commands

Run the requested command directly using the syntax below. The CLI and backend
enforce authentication, ownership, and the required `read` or `write` scope;
do not run `--help` or `simpo me` as routine preflight checks.

## Choose an operation

| Task | Command | Scope | Important constraint |
| --- | --- | --- | --- |
| Create a Draft | `create-biomodel` | `write` | Always Private, Draft, version 0; blank/JSON creation supports `--async` |
| List metadata | `get-biomodels [--scope owned|public] [--creator NAME] [--name NAME]` | `read` | Paginated; defaults to owned models |
| List a model family's versions | `get-biomodel-versions ID [--scope owned|public]` | `read` | Paginated; same creator and name, numeric version descending |
| Read tables | `get-biomodel ID` | `read` | Owned model or accessible Public Release |
| Clone a Public Release | `clone-biomodel ID --name NEW_NAME [--description TEXT]` | `write` | Creates the caller's separate Private Draft |
| Replace Draft tables | `update-biomodel ID --json FILE` | `write` | Owned version 0 Draft |
| Copy Release/Standard to Draft | `sync-biomodel ID` | `write` | Source ID is published; result is a Draft |
| Create immutable Release | `release-biomodel ID` | `write` | Source is owned version 0 Draft |

If a command returns an unknown-command or unsupported-operation error, consult
that command's `--help` and request a SimpoCLI update when the operation is not
available. Do not emulate it with direct HTTP requests.

## Resolve and inspect

Use `get-biomodels` to find IDs, traversing all pages when searching by name.
The default scope is `owned`. Use `--scope public --creator admin --name ASM2D`
to search public models by creator and name; use the actual desired name for
other models. `--creator` matches the account name exactly; `--name` is a
case-insensitive literal substring search (`%` and `_` are ordinary characters).
Inspect candidates to identify the intended family before listing its versions.
Public visibility does not imply that a model belongs to the
caller or can be modified.
Use `get-biomodel` before a mutation to verify the ID, ownership, state, version,
privacy, description, source-paper association, and current tables.
Discovery and version responses use `biomodels`, `page`, `pageSize`, `total`,
and `hasNext`. Public queries must also return `scope: "public"`, even for an
empty list; a missing or different scope does not confirm public discovery and
requires a matching backend. Default owned queries remain backward compatible.
Metadata exposes `creatorId`, `creatorName`, `isOwner`,
`canClone`, and `sourceId` (null when no clone source is recorded).

For the latest public release, inspect `get-biomodel-versions ID --scope public`
and traverse pagination. Keep the creator and name family fixed; select the
greatest numeric `version` among Public Releases. Do not choose by largest ID,
most recent update, or lexicographic version sorting. Verify the actual creator,
requested name, and `canClone` before cloning. Retain the source ID and version
as provenance in the Project description.

Do not confuse a paper DOI with a SIMPO `sourcepaperId`. The latter is an
internal positive database ID.

## Create

`create-biomodel NAME` creates the standard blank tables. Exactly one import
mode may be selected:

- `--template FILE.xlsx`: non-empty Excel template, at most 20 MiB;
- `--json FILE.json`: UTF-8 model-table object, at most 20 MiB.

The name is 1–230 characters and unique within the account. JSON must not
contain `Balance`; SIMPO derives that read-only table. After success, require a
positive `id`, the requested name, `state: "Draft"`, `privacy: "Private"`,
`version: 0`, and the expected `creationMode`.

`Component`, `Parameter`, and `Matrix` are required JSON tables. `Formula`,
`Composition`, and `Ionization` are optional. `Formula` has exactly two
columns, `Component` and `Formula`. Each target must already exist in
`Component`; expressions may use registered Components and Parameters, finite
numbers, parentheses, and `+ - * /`. A Formula Component cannot reference
itself or another Formula Component. Preserve Formula when reading, updating,
synchronizing, or reviewing a model.

Formula commonly represents TSS. If a TSS Component already exists, attempt a
weighted-sum Formula from the Composition TSS coefficients of the contributing
Components, with compatible units and registered Parameter expressions.
Exclude the target itself and other aggregate totals to avoid self-reference
and double-counting; never treat an unknown coefficient as zero. Use the
`simpo-create-biomodel` Composition derivation reference for this procedure.
Keep the derivation in the review audit; do not invent a TSS Component or
silently replace a source-defined independent differential state.

For blank or JSON creation and for `update-biomodel`, `--async` returns a durable
Operation ID; add `--wait` to receive the final BioModel result. Use an
`--idempotency-key` when retrying after a connection timeout.

## Water temperature in Rate

Create/update JSON and XLSX imports preserve plain `T` and `**` in Matrix.Rate.
`T` is the built-in water temperature in °C from the linked DataSet.Environment,
independent for each Tank and time. Do not declare it as a Parameter or Component.
For a source-supported correction, a Rate may contain:

```text
mu_H20 * theta_H**(T - 20) * S_S/(K_S + S_S) * X_H
```

Declare `mu_H20`, `theta_H`, and `K_S` as ordinary Parameters and `S_S`/`X_H` as
Components. Keep the temperature-dependent factor in Rate; T is not supported
in Parameter values/bounds, stoichiometric cells, Composition, Formula, or
Ionization. SIMPO does not automatically correct other kinetics. Biological
`theta_H` is independent of DataSet.Pump θ. The frontend badge/superscript
changes only presentation, never the exported expression.

`T` and `t` are reserved names; uppercase T alone is the runtime symbol.
`T_ref` and `k_T` are allowed. Resolve and rename any old Parameter/Component
named T or t and its references before saving; do not silently overwrite it.
Missing applicable temperature uses 20°C; inputs support 0–40°C. Rates using T
require Forward Euler. Follow [Environment input rules](dataset-and-project.md#water-temperature-and-environment)
and [runtime methods](calculation.md#environmental-temperature-at-runtime).

## Update

`update-biomodel ID --json FILE` replaces model tables rather than patching one
cell. Inspect the JSON and target first. The input object must omit `Balance`
and be at most 20 MiB. Updating synchronizes dependent Projects; report
`affectedProjectCount` and do not run it for an informational request.

When Component, Parameter, or ProcessName identifiers change, the backend
compares the stored Draft with the submitted JSON and automatically creates the
same `changeValueBioModel` dictionary used by the web editor. It uses that
dictionary to migrate Project Variable, Conversion, Activator, and formula
references and to synchronize Component names in Ionization. No mapping file is
required.

Updating a Draft rebuilds dependent Project detail and serialized caches, sets
`biomodel_draft_changed`, and marks any existing calculation engine result as
requiring recalculation.

## Clone a public model

`clone-biomodel SOURCE_ID --name NEW_NAME [--description TEXT]` clones one
accessible Public Release into the caller's account as a new Private Draft.
Owned models can also be cloned, including a Draft or private release.
Use a project-specific name and require `canClone=true` on the inspected source.
The clone does not change the published source or replace an existing Draft.
Verify success, a distinct positive `id`, `sourceId` equal to the supplied ID,
the requested name, `state: "Draft"`, `privacy: "Private"`, and `version: 0`.
The receipt includes `sourceName`, `sourceCreatorId`, `sourceCreatorName`, and
`sourceVersion`; check them against the selected release. Read the new ID back,
require `isOwner=true`, and verify the copied tables.

This operation requires both an updated CLI and a backend that supports public
discovery and cloning. If the backend rejects the operation as unsupported,
report the required backend update; do not substitute `sync-biomodel` or create
an unverified copy through a different endpoint.

## Sync

`sync-biomodel SOURCE_ID` takes an owned Release or Standard version and copies
it into the same-name Draft. Confirm the published source ID and the intended
Draft replacement before execution. Verify the result is a distinct positive
ID with `sourceId` equal to the supplied ID, `state: "Draft"`,
`privacy: "Private"`, and `version: 0`.

## Release

`release-biomodel DRAFT_ID` creates an immutable snapshot and leaves the Draft
available for later work. Default to `--privacy Private`. Use Public only when
the user explicitly requests public visibility after the exact Draft has been
reviewed. Verify a distinct positive result ID, `state: "Release"`, requested
privacy, and a version of at least 1.

## Ambiguous outcomes

Create, clone, sync, and release are not safe to repeat blindly. After a timeout or
dropped connection, list and inspect BioModels across every page to determine
whether the operation already succeeded. For an update, read the target and
compare its tables and metadata before retrying.
