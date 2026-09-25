# DataSet and Project Commands

Run the requested command directly. The CLI and backend enforce authentication,
ownership, and the indicated scope; do not perform routine help or permission
checks before a read or write.

If a requested command returns an unknown-command or unsupported-operation error,
consult its `--help` and update SimpoCLI when needed. Never fall back to direct
API requests; the references describe the newer command surface without
pretending it exists in every package.

## DataSets

| Task | Command | Scope |
| --- | --- | --- |
| Create a Draft DataSet | `create-dataset NAME [--json DETAIL.json]` | `write` |
| List owned DataSet metadata | `get-datasets` | `read` |
| Read complete DataSet tables | `get-dataset DATASET_ID` | `read` |
| Update a Draft DataSet | `update-dataset DATASET_ID --json DETAIL.json` | `write` |
| Copy a published DataSet to its Draft | `sync-dataset DATASET_ID` | `write` |
| Release a Draft DataSet | `release-dataset DATASET_ID [--privacy Private|Public]` | `write` |

List results are paginated. Traverse all pages when resolving a DataSet by name.
Use the positive database ID with `get-dataset`; report the identity metadata
and only the tables relevant to the user's request. A JSON DataSet contains the
complete editable detail object returned by `get-dataset`; updates are parsed
before saving and rebuild Projects that use the Draft.

When Target, Tank, Inflow, or Flow identifiers change, the backend compares the
stored Draft with the submitted JSON and automatically creates the same
`changeValueDataSet` dictionary used by the web editor. Tank, Inflow, and Flow
share the `TankInflowFlow` group because all three identify Project Variable and
Weight dimensions. No mapping file is required.

Updating a Draft rebuilds dependent Project detail and serialized caches, sets
`dataset_draft_changed`, preserves compatible user-entered values through the
automatically derived change-value dictionary, and marks every existing calculation engine result as requiring
recalculation.

For create and update responses, require `success: true` and a positive `id`.
For `update-dataset`, also report `affectedProjectCount`. For synchronization,
require `sourceId` to equal the input Release ID and treat `id` as the target
Draft ID. For release, require `sourceId` to equal the input Draft ID, treat
`id` as the new Release ID, and require `version >= 1`.

## Projects

| Task | Command | Scope |
| --- | --- | --- |
| Create a Draft Project | `create-project NAME --biomodel-id ID --dataset-id ID [--json DETAIL.json]` | `write` |
| List owned Project metadata | `get-projects` | `read` |
| Read complete Project detail | `get-project PROJECT_ID` | `read` |
| Read all Solution Variable fields | `get-project-variables PROJECT_ID` | `read` |
| Update one Variable field | `set-project-variable PROJECT_ID VARIABLE VALUE` | `write` |
| Update a Draft Project | `update-project PROJECT_ID --json DETAIL.json` | `write` |
| Copy a published Project to its Draft | `sync-project PROJECT_ID` | `write` |
| Release a Draft Project | `release-project PROJECT_ID [--privacy Private|Public]` | `write` |

Use `get-projects` and traverse pagination only when a name must be resolved to
an ID. When the user already supplied an exact ID, run the requested lifecycle
command directly. For `set-project-variable`, read the current Variable table
and select the row using both the exact Variable name and `--tank` when the row
is tank-specific.

`create-project` builds the Solution from the selected BioModel and DataSet.
Without `--json`, it generates the default Solution tables. With `--json`, it
parses the supplied Solution detail during creation. Use the same
detail shape returned by `get-project`: `Variable`, `Target`, `Conversion`, and
`Weight` are required; `Activator` may be omitted or empty and will be generated
when needed. Use `update-project` to replace the detail of an existing Draft.
Updating Project detail rebuilds the Solution cache and removes results that no
longer match it.

For synchronization, the command argument is the Release ID and the response
contains the target Draft ID. For release, the argument is the Draft ID and the
response contains a new Release ID. Treat these as different records.

For Project create and update responses, require `success: true` and a positive
`id`. For synchronization, require `sourceId` to equal the input Release ID and
treat `id` as the target Draft ID. For release, require `sourceId` to equal the
input Draft ID, treat `id` as the new Release ID, and require `version >= 1`.

## Update a Variable safely

Only an owned version 0 Draft Project is writable. Read the installed command
help for the allowed `--field` values and value syntax when needed. Common examples include
numeric `Value`, `LowerBound`, or `UpperBound`; Boolean `Evaluation`; integer
`DecimalPoint`; and nullable metadata fields. `Variable` and `Tank` identify a
row and are not writable fields.

Before running the command, show or internally verify:

- Project ID, name, state, and version;
- exact Variable and optional Tank;
- target field, current value, and proposed value;
- bounds or type restrictions returned by the current Project data.

After success, require `success: true` and verify that the returned Project,
Variable, Tank, field, old value, and new value match the intended update. Read
the row again when the response is incomplete or the outcome is ambiguous.

Do not bulk-edit variables by constructing repeated commands unless the user
explicitly requested every change and each row/value has been validated.
