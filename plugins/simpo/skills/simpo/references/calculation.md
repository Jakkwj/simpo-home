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
- Do not apply either offset rule to `Measured` or `Environment`. Measured values remain the
  original observations used for comparison with model outputs; they are not
  shifted to match a Solution Variable value. Environment temperatures are
  external inputs, not Solution Variables.

Before interpreting a result, record the DataSet first value, the matching
Solution value, the original Inflow Conversion expression, its resolved value,
and the resulting offset. Do not pre-shift the stored DataSet to compensate for
this runtime behavior.

## Execution mode and input methods

Use `--execution-mode` with one of three canonical values:

- `dynamic`: run the original time series;
- `steady_state`: reduce Flow, Inflow, and Environment to constant inputs and solve only the
  steady state;
- `steady_state_then_dynamic`: solve the steady state first, use that state as
  the dynamic initial condition, and then run the original time series.

Component initial states in `dynamic` come from `Solution.Variable.Value`.
Configured Solution.Constraint boundaries, including DO, are enabled in both
steady-state and dynamic phases. Steady state uses the original constraint
observations averaged with the selected steady-state input averaging method,
without Flow weighting; dynamic phases use the time series with each
Constraint's interpolation. Measured DO alone does not create a Constraint,
and constraint compensation is not a measured physical oxygen supply.
Use Forward Euler with configured Constraints; Improved Euler does not
currently support them.

Use `--input-interpolation previous|linear` (also accepted as
`--dynamic-input-interpolation-method`) for dynamic Flow/Inflow/Environment values between
samples. `previous` is zero-order hold; `linear` interpolates adjacent samples
and holds the final value after the last sample.

Use `--steady-state-input-average-method previous|linear|arithmetic` for the
steady-state phase. `previous` duration-averages a step signal, `linear`
integrates a linearly interpolated signal, and `arithmetic` averages valid rows
without time-spacing or Flow weighting. For Inflow concentrations, `previous`
and `linear` use the matching Flow as a hydraulic weight. State all three
settings before starting a calculation; do not use the old Boolean
`--steady-state` interface for new requests.

### Environmental temperature at runtime

Environment's `T` follows `--input-interpolation`: `previous` switches at each
valid sample, `linear` interpolates that Tank's valid samples, and both hold the
final value. Other Tanks' sample times do not change its interpolation.
Temperature event times are preserved under `--resolution-rate` downsampling;
Forward Euler steps stop at the next input event instead of skipping it.

The steady-state method averages each series' temperature, without Flow
weighting: previous/linear use the first-to-last valid sample interval and
arithmetic uses valid samples. A single sample is used directly. Repeat the
final temperature at an endpoint if the held period should contribute to a time
average. Saturation and Rate expressions are evaluated at that average, which
does not generally equal averaging their nonlinear dynamic values. Combined
mode restores the original temperature series during the dynamic phase.

A missing Tank/zone series uses 20°C, after checking a point settler's parent
series. Environment is not adjusted by Project Variable offsets or estimation.
Record temperature provenance, defaults, interpolation/average method, Pump θ,
and any Rate temperature factors when comparing runs. Temperature-dependent
aeration and Rates using T require Forward Euler; Improved Euler does not
support Rate T. No extra temperature CLI flag is needed; update the DataSet or
BioModel JSON through the normal commands. See their references for schemas.

For a steady-state result, inspect the `Retention` rows as well as Component
and Target. Per-Tank HRT uses each Tank's through-flow. System HRT divides the
selected HRT Tank volume by true external influent flow. System SRT divides the
selected SRT Tank TSS inventory by TSS leaving external Outflow and Wasted
connections; internal recycles are not external losses. Require `Converged=true`
before describing the result as a converged steady state.

## When bacteria fail to accumulate

Read the relevant bacterial Component/tank trajectories, initial states, and
execution mode before changing kinetics. TSS alone is not a viable-biomass
measurement. Check these common causes using the actual configuration:

1. **Qw too large:** identify the waste Connection and its actual Flow name,
   inspect the DataSet flow and runtime Variable.Value offset, and compare the
   system solids inventory with waste/effluent TSS mass loss. Excessive wasting
   can make SRT too low to retain biomass. A supported reduction of Qw must
   preserve hydraulic balance; internal recycles are not external sludge loss.
2. **Point Settling factor too small:** inspect the effective SettlingFactor,
   outlet/blanket split, and effluent TSS. The factor directs particulates to
   the blanket; too small a value can wash them out. When unspecified, the usual
   sludge-retaining value is around `0.9999`; reported effluent TSS of `0`
   allows setting it directly to `1`. Preserve a supplied factor and document
   an adopted value and its basis as an assumption. This is not a mandatory
   parser range or permission to replace source data silently.
3. **Bacterial initial Value too low:** read the exact bacterial Component/tank
   rows in `Solution.Variable.Value`. Inflow usually carries no seed bacteria;
   verify its actual Conversion rather than assuming this. Propose increasing
   inadequate initial values with justified units and source/assumption notes,
   then recalculate within the user's authorization. Do not change unrelated
   particulate Components or confuse runtime `Value` with estimation
   `InitialValue`. In combined mode, dynamic initial conditions come from the
   steady-state result, so inspect that result and its oxygen supply first.

Read before a supported variable update; use the exact returned name and tank
as described in [Project operations](dataset-and-project.md). Preserve prior
values/results and compare an authorized rerun. For analysis-only requests,
give recommendations without updating or launching calculations. Retention
flags only select HRT/SRT statistics; enabling SRT does not restore bacteria.
Missing TSS mapping or mass-loss data prevents a quantitative washout diagnosis.

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

The local evolution controls are `--sceua-subcomplex-size` and
`--sceua-evolution-steps`. The first is the number of points in each temporary
Sub-complex; it defaults to `dimension + 1` and must be no greater than the
population size of one Complex. The second is the number of Sub-complex
evolution steps performed for each Complex during one Shuffle; it defaults to
the Complex population size and must be at least `1`. They are the public names
for the algorithm's internal NPS and NSPL values: each step selects a new
Sub-complex, applies one trial update, and writes the accepted result back to
the Complex before the next step. These controls are independent of the number
of Complexes and use the common `--threads` setting only for parallel Complex
evaluation. For old Projects that do not contain these fields, Simpo uses
these same defaults automatically; no database migration is needed.

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


### Saved Balance views

Balance uses the same `get-calculation-result` command, with no new retrieval
command. After locating the actual engine sections, select the saved scope and view:

```text
simpo get-calculation-result PROJECT_ID --engine SIM \
  --section dynamic_balance --view summary --limit 5
simpo get-calculation-result PROJECT_ID --engine SIM \
  --section dynamic_balance --view diagnostics --offset 0 --limit 10
simpo get-calculation-result PROJECT_ID --engine SIM \
  --section steady_state_balance --dimension Component --key S_O2 \
  --view terms --output oxygen-balance.json
```

Use actual returned keys; these examples do not assume every model contains
S_O2. Supported views are `summary`, `diagnostics`, `terms`, `tanks`, `reactions`,
and `concentrations`. The four detail views require both `--dimension` and
`--key` and optionally accept `--tank`. Dimension is the exact `Composition`,
`Component`, or `Target`; keys and tanks are exact names. Summary/diagnostics
may be filtered by dimension and key, but not tank. Without `--view`, generic
result retrieval is unchanged and Balance filters are not accepted.

Besides `SIM`/`Simulation`, these views support the final best-solution
simulation saved under `UNC`/`LHS`/`Uncertainty` and
`GA`/`RFGA`/`SCEUA`/`Estimation`. For example, use `--engine UNC --section
dynamic_balance --view summary`; the section is at the engine root, not under
`best_result`. Check the saved `best_solution` provenance and availability.
These results represent one selected parameter set, not all candidates or the
prediction band. Historical best-fit curves alone cannot supply missing Balance
data, and another engine's SIM result must not be substituted.

Use `calculation-result-analysis` from the same Skills package when explaining
these results. It contains the shared Balance scientific rules used by SimpoAI.
The response includes saved `balance` metadata, `selection`, and ordinary
paginated `data`; an abnormal balance is not a command failure. Missing saved
Balance is unavailable, not zero or closed. These views are read-only and do
not recalculate results, modify Fortran, render charts, or trace influent origin.

This option set requires SimpoCLI 0.1.10 and the corresponding backend support.
Best-solution views additionally require an updated CLI and backend that accept
these engines; the updated 0.2.0 source includes this support, but an earlier
installed build with the same version may not. Use the command's returned
capabilities/errors rather than the version number alone.
If the installed command rejects an option, inspect its help after the error;
do not bypass it with direct API requests or automatically upgrade the user.
The saved report's `resolution_rate` is already a percentage, whereas
`calculate --resolution-rate` takes a ratio (`1` means `100%`).
