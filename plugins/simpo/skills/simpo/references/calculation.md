# Calculation Commands

Calculations require a Token with `calculate` scope. `calculate` also requires
the matching platform's SimpoClient unless `--no-launch` is used. Run the
requested calculation directly; the CLI and backend enforce these requirements.
Consult `--help` only when syntax or engine options are unclear, or when the
command reports a usage error.

## Workflow

1. Resolve a Project name to an ID only when necessary. If the user supplied an
   exact ID, run the requested calculation command directly; the backend checks
   that it is an owned version 0 Draft.
2. Read current Project Variables only when the requested calculation depends on
   calibration bounds or evaluation flags.
3. Run `simpo calculate PROJECT_ID` directly with the requested engine and only
   its relevant options, then show the material settings before starting work.
   Do not invoke `--help` as a routine preflight check.
4. Start the calculation. Do not use `--print-protocol` unless an explicit
   integration needs it; the protocol contains a short-lived credential and
   must not be logged or shared.
5. Use `--wait` or `get-calculation-status` to determine completion. A successful
   launch is not a completed calculation.
6. Use `stop-calculation` only when the user asks to stop the exact Project.

## Engines

The available interface includes these case-sensitive families; the installed
help remains authoritative:

- `SIM`: simulation;
- `OAT_AA`, `OAT_RA`, `OAT_AR`, `OAT_RR`: one-at-a-time sensitivity analysis;
- `LHS`: uncertainty analysis;
- `GA`, `RFGA`: parameter estimation.

Do not invent tuning values. Preserve CLI defaults unless the user's scientific
goal supplies a reason to change them. Match engine-specific flags to the
selected family; for example, OAT intensity for OAT, sample count for LHS, and
population/generation options for GA or RFGA.

## Launch, wait, and status

By default `calculate` prepares files and starts the installed SimpoClient.
`--no-launch` prepares without starting it and cannot be combined with `--wait`.
`--wait-timeout` limits how long the CLI polls; expiration does not stop the
client or backend calculation.

When waiting separately, call `get-calculation-status PROJECT_ID` at a reasonable
interval. Treat only the terminal statuses described by the installed help as
final. Report compilation and calculation failures with the service's concise
message.

## Stop

Before `stop-calculation PROJECT_ID`, confirm the current status and exact
Project. The command may stop backend work and matching local SimpoClient or
calculation processes. After execution, verify both the returned stop result and
a subsequent status when available.

If a start or stop request times out, inspect status before retrying. Never
blindly launch a duplicate calculation or repeat a stop request.

## Retrieve results

After the calculation has completed, use the bounded result reader:

```text
simpo get-calculation-result PROJECT_ID [--engine ENGINE] [--section NAME] \
  [--offset N] [--limit N] [--output result.json]
```

Navigate before retrieving values:

1. Run without `--engine` to list stored result engines.
2. Add `--engine` to list that engine's top-level sections without returning
   their complete values.
3. Add a dotted `--section` path, such as
   `Tank1.Predicted.S_NH`, to select one specific result series. Each path part
   identifies the next nested result level: `Tank1`, then `Predicted`, then the
   `S_NH` series.
4. Walk `offset` while `hasNext` is true. Reduce `--limit` or select a deeper
   section if the server reports that a page exceeds its response-size limit.

The endpoint returns JSON metadata (`kind`, `mode`, `total`, `offset`, `limit`,
and `hasNext`) and the current page in `data`. Use `--output` for large pages
instead of sending them through a terminal or chat. Do not read the Project's
internal pickle directly; result access is read-only and remains subject to the
backend's Token ownership and scope checks.
