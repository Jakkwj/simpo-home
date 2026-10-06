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

## Initial DataSet value semantics

For calculation, `Solution.Variable.Value` is the baseline for `Inflow` and
`Flow`; the DataSet value at `time=0` is used only to calculate the additive
offset. The backend preserves each series' shape by applying that offset to
every row:

- For `Inflow`, use the selected `Conversion` relation for the component. The
  coefficient may be a literal or a BioModel Parameter expression; resolve it
  with the current Parameter values. The offset is `Variable.Value * resolved
  Conversion coefficient - DataSet Inflow value at `time=0`; add it to the full
  source series and clamp negative results to zero.
  If the relation is one-to-one with coefficient `1`, a DataSet series starting
  at `100` and a Solution value of `1000` becomes `1000` at the first point and
  every later point is increased by `900`.
- For `Flow`, the offset is `Variable.Value - DataSet Flow value at `time=0`;
  add it to every row, clamp negative results to zero, and then convert the
  resulting flow from `m3/d` to `m3/s` for the calculation.
- Do not apply either offset rule to `Measured`. Measured values remain the
  original observations used for comparison with model outputs; they are not
  shifted to match a Solution Variable value.

Before interpreting a result, record the DataSet first value, the matching
Solution value, the original Inflow Conversion expression, its resolved value,
and the resulting offset. Do not pre-shift the stored DataSet to compensate for
this runtime behavior.

## Engines

The available interface includes these case-sensitive families; the installed
help remains authoritative:

- `SIM`: simulation;
- `OAT_AA`, `OAT_RA`, `OAT_AR`, `OAT_RR`: one-at-a-time sensitivity analysis;
- `LHS`, `UNC`: uncertainty analysis (`UNC` is the canonical current code and
  `LHS` remains accepted for historical calculations);
- `GA`, `RFGA`, `SCEUA`: parameter estimation. `SCEUA` is the SCE-UA
  (Shuffled Complex Evolution) engine.

Do not invent tuning values. Preserve CLI defaults unless the user's scientific
goal supplies a reason to change them. Match engine-specific flags to the
selected family; for example, OAT intensity for OAT, sample count for UNC/LHS,
population/generation options for GA or RFGA, and Complex/Shuffle options for
SCEUA.

### SCE-UA and shared initialization

Use the public engine code `SCEUA` with `simpo calculate`. The initial
population options are shared with `UNC`, legacy `LHS`, `GA`, and `RFGA`; they
support `LHS`, `scrambled_sobol`, `sobol`, and `uniform` through
`--initialization-method`. Enable
`--fixed-initialization-seed --initialization-seed N` to reproduce LHS,
scrambled Sobol, or uniform initialization. Unscrambled `sobol` is deterministic
and does not use a seed. The seed range is `1` through `4294967295`.

`--inject-initial-value` is shared by GA, RFGA, and SCEUA. When enabled, the
current `Solution.Variable.InitialValue` values are inserted into the initial
population; it does not replace the remaining generated points.

The total SCE-UA population is:

```text
total population = --sceua-num-complexes * --sceua-complex-population-size
```

`--sceua-num-complexes` defaults to `min(max(2, --threads), 8)` when omitted.
`--sceua-complex-population-size` defaults to `2 * dimension + 1` when omitted,
must be at least `dimension + 1`, and determines the total population with the
number of Complexes. `--sceua-max-evaluations` defaults to `20 * total
population` when omitted and must be at least the total population. The public
convergence defaults are `10` Shuffles, `1e-4` objective tolerance, and `1e-4`
parameter tolerance. The objective and parameter criteria are an **OR**: either
criterion can stop SCE-UA. `--sceua-max-shuffles` is an optional hard cap on
outer Shuffle cycles; `0` disables that cap. `--threads` is the shared
parallelism control; Complexes can be evaluated concurrently. A positive
objective tolerance requires at least one convergence Shuffle.

### OAT correlation is opt-in

The OAT rank and weighted-integral sensitivity results do not imply that a
parameter-correlation matrix was calculated. Correlation output is disabled by
default because it can be expensive for large OAT result sets. When the user
needs Pearson correlation output or the Dashboard correlation panel, enable
both switches:

```text
simpo calculate PROJECT_ID --engine OAT_AR \
  --auto-plot --auto-plot-correlation --wait
```

`--auto-plot-correlation` alone is not sufficient in the client workflow: the
correlation payload is generated only when automatic plotting is also enabled.
At least two parameters must be marked `Evaluation=true`; with zero or one
evaluated parameter, an empty correlation result is expected and there is no
pairwise coefficient to report. State this explicitly instead of interpreting
an empty object as zero correlation.

## Launch, wait, and status

By default `calculate` prepares files and starts the installed SimpoClient.
`--no-launch` prepares without starting it and cannot be combined with `--wait`.
`--wait-timeout` limits how long the CLI polls; expiration does not stop the
client or backend calculation.

When waiting separately, call `get-calculation-status PROJECT_ID` at a reasonable
interval. Treat only the terminal statuses described by the installed help as
final. Report compilation and calculation failures with the service's concise
message.

For a preparation step that may outlive one HTTP request, use
`--async-preparation --no-launch`. The command returns an `operationId`; poll it
with `wait-operation` and inspect the nested `result.launchProtocol` only after
the operation succeeds. If the CLI should launch SimpoClient itself, add
`--wait-preparation`; this waits for preparation before starting the local
client. This preparation wait is distinct from `calculate --wait`, which waits
for the later calculation status. `--idempotency-key` makes a retried
preparation request refer to the same backend operation.

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
