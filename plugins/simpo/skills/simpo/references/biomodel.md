# BioModel Commands

Run the requested command directly using the syntax below. The CLI and backend
enforce authentication, ownership, and the required `read` or `write` scope;
do not run `--help` or `simpo me` as routine preflight checks.

## Choose an operation

| Task | Command | Scope | Important constraint |
| --- | --- | --- | --- |
| Create a Draft | `create-biomodel` | `write` | Always Private, Draft, version 0 |
| List metadata | `get-biomodels` | `read` | Paginated; no complete tables |
| Read tables | `get-biomodel ID` | `read` | Owned model ID |
| Replace Draft tables | `update-biomodel ID --json FILE` | `write` | Owned version 0 Draft |
| Copy Release/Standard to Draft | `sync-biomodel ID` | `write` | Source ID is published; result is a Draft |
| Create immutable Release | `release-biomodel ID` | `write` | Source is owned version 0 Draft |

If a command returns an unknown-command or unsupported-operation error, consult
that command's `--help` and request a SimpoCLI update when the operation is not
available. Do not emulate it with direct HTTP requests.

## Resolve and inspect

Use `get-biomodels` to find IDs, traversing all pages when searching by name.
Use `get-biomodel` before a mutation to verify the ID, ownership, state, version,
privacy, description, source-paper association, and current tables.

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

## Update

`update-biomodel ID --json FILE` replaces model tables rather than patching one
cell. Inspect the JSON and target first. The input object must omit `Balance`
and be at most 20 MiB. Updating can synchronize dependent Projects; report
`affectedProjectCount` and do not run it for an informational request.

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

Create, sync, and release are not safe to repeat blindly. After a timeout or
dropped connection, list and inspect BioModels across every page to determine
whether the operation already succeeded. For an update, read the target and
compare its tables and metadata before retrying.
