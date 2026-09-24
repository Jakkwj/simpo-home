# Calculation Commands

Calculations require a Token with `calculate` scope. `calculate` also requires
the matching platform's SimpoClient unless `--no-launch` is used. Read the
installed `--help` because engine choices and ranges may change.

## Workflow

1. Resolve and inspect the owned Project. Only its version 0 Draft is calculable.
2. Read current Project Variables when the requested calculation depends on
   calibration bounds or evaluation flags.
3. Run `simpo calculate PROJECT_ID --help`, select an engine and only its
   relevant options, then show the material settings before starting work.
4. Start the calculation. Do not use `--print-protocol` unless an explicit
   integration needs it; the protocol contains a short-lived credential and
   must not be logged or shared.
5. Use `--wait` or `calculation-status` to determine completion. A successful
   launch is not a completed calculation.
6. Use `stop-calculation` only when the user asks to stop the exact Project.

## Engines

The current development interface includes these case-sensitive families, but
the installed help is authoritative:

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

When waiting separately, call `calculation-status PROJECT_ID` at a reasonable
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
