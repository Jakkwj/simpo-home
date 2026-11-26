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
| Create a Draft DataSet | `create-dataset NAME [--json DETAIL.json] [--async]` | `write` |
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

### Typed Tank/Pump tables and water temperature

The base tables are `Unit`, `Target`, `Measured`, `Inflow`, `Flow`, and
`Connection`. Include at least one tank row across `CSTRTank`,
`PointSettlingTank`, `TakacsSettlerTank` or legacy `Tank`. Include `AirPump`
and `KLaPump` when the process uses them. Preserve optional `Environment`, `Controller`,
`ControllerConfig`, `PerformanceMetric` and `jointGraphJson` when present.
Legacy `Tank` and Air `Pump` tables remain
readable. Use the existing `--json` create/update commands; there is no separate
temperature or KLa command. Preserve all existing tables when replacing the
full detail, including when editing an unrelated field. A supporting backend
and calculation package are needed; do not drop new tables to fit an old server.

Types come from the table names, without a repeated Type column. AirPump uses
`Name | SOTEa | SOTEb | SOTEc | θ`; KLaPump uses `Name | θ | TRef`. Legacy and
typed Pump rows merge only when names are unique; empty/header-only optional
tables cannot mask populated ones. Do not duplicate Tanks in legacy/type tables.
In the `CSTRTank` JSON table, set `InletLagSeconds` to a positive time
constant to filter the combined liquid flow and each incoming component's mass
load. Zero means instantaneous mixing. The eight BSM1 cases use 8.64 s at
Tank1. The workbook exposes this choice as `MixedInletResponse` and
`TimeConstant` (seconds). Its `OxygenSaturationModel` and `SaturationValue`
columns correspond to JSON `SaturationModel` and `SaturationValue`.
Linear input interpolation is a separate calculation option. Preserve reviewed
BioCalculated and ConstantVolume choices. Direct Tank.KLa input fields are rejected, including zero.
Migrate old files offline to new copies using Flow plus KLaPump and θ=1
when preserving the prior uncorrected coefficient.

Takács tables keep one physical tank with LayerCount internal layers.
`ConstantVolume` must be true. Volume is Area times Height (`Total Height`
in the worksheet).
LayerCount is a strict integer 3…10 and FeedLayer is 2…N−1. The upper
bound of 10 is the current product support limit, not a physical settling limit; BSM templates
retain the official 10-layer discretization.
Connection.Into uses its physical name and FeedLayer, while From uses explicit
`Name_1` (bottom) through `Name_N` (top). BSM1 uses 10 layers and feed layer 6
counted from the bottom. Do not turn the layers into independent physical Tanks.

Add the sixth Unit column after Height as `"5":"T"` in the header and
`"5":"℃"` in its value row. Temperature is fixed to Celsius (`°C` and `degC`
are also accepted); legacy files without this column default to Celsius.
The optional seventh JSON column is `"6":"KLa"` with value `"6":"/d"`.
The Unit worksheet shows Flow fixed to m³/d and KLa fixed to /d.
Use this as the `Environment` value inside a complete DataSet detail:

```json
[
  {"0":"Tank","1":"Tank1","2":"Tank","3":"Clarifier_Blanket"},
  {"0":"Environment","1":"T","2":"Environment","3":"T"},
  {"0":0,"1":20,"2":0,"3":18},
  {"0":1,"1":22,"2":0.5,"3":19}
]
```

Tank names must exist; point-settler zone names are `Name_Outlet` /
`Name_Blanket`, and Takács layer names are `Name_1` through `Name_N`.
Each `(Tank, Environment)` pair is unique. Each series' first valid value is at
time 0, times increase strictly within its block in `Unit.Time`, and values are
finite numbers from 0 to 40°C. Different blocks may have independent times;
null values mean no sample. Only uppercase `T` is supported, not `Temperature`
or the old `Property` table/header. `T` and `t` are reserved user-defined names,
including Tank names. Omitted or empty Environment uses 20°C; an unspecified
settler zone first falls back to its parent Tank series.

Pump's public `θ` maps to internal `ThetaFactor` (also accepted as a legacy
header). Missing or blank θ defaults to **1**; use source/test evidence for an
explicit value such as 1.024. θ must be finite and positive and produce finite,
positive multipliers over 0–40°C. AirPump uses `θ**(T-20)` and has no TRef
field. KLaPump uses `θ**(T-TRef)` with TRef defaulting to 20°C. Each receiving
Tank uses its own water temperature; omitted T still means 20°C, so KLaPump
applies `θ**(20-TRef)`.

CSTR `SaturationModel` is Freshwater (default), Constant or BSM2. Freshwater
uses the existing relation at 1 atm, with a 20°C value of
9.092426042885567 mg O₂/L; only AirPump also multiplies by Tank BetaFactor.
Constant requires a finite nonnegative SaturationValue in mg O₂/L. Constant
and BSM2 return final effective saturation and do not multiply Beta again.
Classic BSM1 uses fixed biological parameters, Constant saturation 8 and
KLaPump θ=1, with no dynamic temperature state or required temperature series.
BSM2 transfer can use TRef=15 and θ=1.024 plus the BSM2 saturation relation;
this is not the full BSM2 thermal model. Water-temperature input does not
correct the air-meter gas-volume basis or implement pressure/ORP inputs.

KLaPump values are Flow time series in **/d**, independent of Unit.Time;
volume-flow signals remain m3/d. Connection stays `From | Flow | Into`, with
the KLaPump name as From and a CSTR as Into. Its Flow entry must be one named
signal, without an expression or constant. One signal can drive several Tanks
at its full value, without splitting it by volume; shared KLaPumps must agree
on TRef. A signal cannot also be hydraulic/air volume flow. Each Tank can
receive one KLaPump connection. The receiving tank must use a single aeration
method. In Assessment expressions, `Tank5.KLa` reads the effective coefficient
computed for that tank. It is distinct from the named input signal `KLa_5`.
KLa is excluded from hydraulic, HRT/SRT and air-volume statistics.

### Controllers

Each row of the current `Controller` table binds a measurement at
`SensorLocation` to a continuous PI controller and its named Flow or KLa
handle. JSON and Excel use the same table name and columns.

```text
Name | SensorPreset | SensorLocation | SensorTarget | SensorUpperLimit |
ControllerSetpoint | ControllerGain | ControllerIntegralTime | ControllerTrackingTime |
ControlHandle | HandleLowerLimit | HandleUpperLimit | SensorLowerLimit
```

`SensorLowerLimit` defaults to zero on older 12-column rows. The sensor range
must contain the setpoint. The six instrument presets are `BSM_Class_A`,
`BSM_Class_B0`, `BSM_Class_B1`, `BSM_Class_C0`, `BSM_Class_C1` and
`BSM_Class_D`. Integral and tracking times use days even for hourly inputs.

Preserve the companion `ControllerConfig` when editing a full detail. It
carries controller identity, per-sensor noise, PI initialization and actuator
settings. The BSM reference noise spans days 0–14 at one-minute intervals.
The dynamic benchmark uses that sequence. The 500-day closed-loop startup
uses ideal noise-free sensing. Other cases can use random noise, retaining
its seed, standard deviation and update interval, or choose no noise.
Excel stores it in the `SimpoControllerConfig` document property. For an
open-loop DataSet the table can be empty. The previous compact JSON keys
`ControlLoop` and `ControlLoopConfig` are accepted on input.

### Assessment definitions

In a DataSet JSON passed to the CLI, use `detail.PerformanceMetric` from the
read response as the table to edit, then submit the complete detail object.
Its canonical header is `Name | Formula | Unit | StartDay | EndDay`. Dash and
the workbook call the feature **Assessment**. The current worksheet order is
`Name | Unit | StartDay | EndDay | Formula`. Provide a unique name, scalar
formula and unit for each metric. Blank endpoints use the corresponding
boundary of the saved trajectory, and supplied endpoints use simulation days.

For example, `Mean(0.004 * Q_a + 0.008 * Q_r + 0.05 * Q_w)` computes the
BSM1 pumping energy (PE) in kWh/d. `5 * SP + AE + PE + 3 * EC + ME` uses
metrics evaluated for the same window to obtain OCI. Use
`Branch("Tank6_10", "Outflow")` for the recorded physical effluent flow in the
dynamic benchmark. `Tank6_10.TSS` reads a Target, `Tank3.Volume` reads tank
volume and `Tank3.KLa` reads the effective oxygen-transfer coefficient. Use
case-sensitive function names such as `Mean`, `Integral`, `Change` and `If`.

`Change(x)` and `Change(x, 0)` subtract the opening value from the closing
value. `Change(x, -1)` uses the previous saved output sample for the closing
value and keeps the opening value. An offset must be 0 or a negative integer
that leaves the closing sample inside the window. BSM1 SP applies `-1` to
the whole-plant sludge inventory. That moves the endpoint back 15 minutes
in cases 03–08 and 4 hours in cases 01–02. The wasting term and averaging
period still span the full seven days.

### Earlier module-based DataSets

A `Controller` table with PI-only headers such as `Type` and `Setpoint` belongs
to the earlier split format. Preserve its `Sensor`, `Actuator` and signal
connections together when updating it. The following rules apply to those files.

SignalConnection uses the standard two columns `From | To`, containing module
names. Optional `FromPort` and `ToPort` columns preserve explicit port choices;
when omitted, ports are inferred only when the module types identify a unique
supported connection. Current connections are Sensor.Output to
Controller.Measurement and Controller.Output to Actuator.Input. A controller
may drive several actuators. Each Actuator has optional `InputGain` (default 1,
finite and positive), applied to its incoming command before actuator response
and limits; its InitialValue and limits remain in actuator-output units.
SignalConnection has no Gain field. Controller.Gain remains the PI parameter.
Module names are globally unique. Sensor declares its location in separate
`Tank` and `Component` columns; Component is a BioModel component symbol.
Actuator.Target is a named Flow. Controller no longer repeats either endpoint
or Sensor/Actuator names. Each input has one source, each Flow has one writer;
shared sensors share state, while actuators keep independent state. Current PI
has fixed Setpoint and SampleTime=0; dynamic setpoints, feedforward, cascade
and MPC are not implemented. Sensor noise is explicitly none/random/predefined;
BSM1 requires NoiseFile=builtin:BSM1, NoiseColumn=1 (DO) or 2 (nitrate). KLa Bias, output, limits and actuator initial/output
values are /d at TRef; temperature correction follows the actuator. KLa lower
limits and actuator initial values must be finite and nonnegative. Existing
control time parameters remain in days. Fully controlled Flow inputs cannot
also be selected for estimation. Runtime control replaces only the effective
current input, preserving the original samples. KLaPump and closed-loop
calculations require Forward Euler.

For offline migration, write a new workbook and retain the source. Rename old
ControlConnection to SignalConnection and move each Controller-to-Actuator
edge Gain to that actuator's InputGain. Preserve explicit ports. Reject mixed
old/new connection tables, non-unit Sensor-to-Controller Gain, or simultaneous
non-default edge Gain and InputGain; do not guess whether to multiply them.
The split-table template protocol is `signal-connections-v3`, with
`sensor_source_format=split-tank-component`. Older Sensor.Source values remain
readable and are split at the last dot; new workbooks contain Tank and Component
instead of Source. If both formats are supplied, a populated Tank/Component
pair must be complete and agree with Source. Reject conflicts or partially
filled pairs rather than selecting a definition silently.

For the complete schema and scientific rules, use `simpo-create-dataset`'s
`dataset-json-format` reference when available. See
[Calculation input methods](calculation.md#environmental-temperature-at-runtime)
for switching/averaging, and [BioModel Rate T](biomodel.md#water-temperature-in-rate)
for biological corrections. Do not add T to Project Variables or Conversion.

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
| Create a Draft Project | `create-project NAME --biomodel-id ID --dataset-id ID [--json DETAIL.json] [--async]` | `write` |
| List owned Project metadata | `get-projects` | `read` |
| Read complete Project detail | `get-project PROJECT_ID` | `read` |
| Read all Solution Variable fields | `get-project-variables PROJECT_ID` | `read` |
| Update one Variable field | `set-project-variable PROJECT_ID VARIABLE VALUE` | `write` |
| Update a Draft Project | `update-project PROJECT_ID --json DETAIL.json [--async]` | `write` |
| Update only the description | `update-project-description PROJECT_ID --description-file REPORT.md` | `write` |
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
`Weight` are required; `Activator`, `Constraint`, and legacy `Retention` may be omitted.
Activator will be generated when needed. Use `update-project` to replace the detail of an existing Draft.
Updating Project detail rebuilds the Solution cache and removes results that no
longer match it.

To write an analysis report without invalidating results, use
`update-project-description PROJECT_ID --description-file REPORT.md`, with a
UTF-8 file, or `--description TEXT` for short text. Exactly one input option is
required. The target must be an owned version 0 Draft. This replaces the entire
description; read and merge existing user content before submitting, and use
empty text only to clear it intentionally. The command sends only `description` to the Project metadata endpoint;
it preserves Solution detail, calculation settings, and saved results. Verify
the returned success, ID, `resultsPreserved: true`, and exact description, then
read `get-project PROJECT_ID` to confirm the saved description. When reporting
completed calculations, also verify that their result directory remains
available. After a timeout, read before retrying.

This command needs a supporting CLI and backend. If either is too old, keep the
report locally and identify the required update. Never fall back to a complete
`update-project` request solely to save the description, because that operation
rebuilds the Solution and invalidates results.

`Constraint` is an optional list of named records with exactly `Tank`,
`Component`, `Target`, and `Interpolation`. It forces the selected Component in
the Tank to follow the matching DataSet Measured Target. References must exist,
Target and Component units must match, each Tank/Component pair must be unique,
and `Interpolation` must be `Previous` or `Linear`. The first Measured value
cannot be empty; a constrained Measured series is removed from the weighted
fitting objective. A common candidate is tank-specific measured DO when the
case lacks sufficient aeration/oxygen-transfer inputs such as kLa or Qair:
map the actual DO Target and Component, propose the Constraint, and document
the imposed-DO assumption instead of inventing aeration data. A measured scalar
needs a justified time interval/constant-series assumption. Do not constrain
all observations by default; other uses need a source/user-defined reason.
Configured Constraints are enabled in `dynamic`, `steady_state`, and both
phases of `steady_state_then_dynamic`. Steady state uses the original
observations averaged with `steadyStateInputAverageMethod`, without Flow
weighting; dynamic simulation uses the time series and the selected
Constraint interpolation. Measured DO alone does not create a Constraint,
and its compensating source/sink is not measured aeration.

`Retention` is a named-record list with exactly one row per DataSet Tank and
fields `Tank`, `HRT`, and `SRT`. HRT/SRT are booleans. HRT selects Tank volumes
for the system hydraulic-retention numerator; SRT selects Tank TSS inventories
for the solids-retention numerator. SRT requires a DataSet Target with
`StandardTarget: "Total Suspended Solids"` and a nonempty Conversion row.
For a settling tank, set `HRT=false` when `BioCalculated=false` (the usual case),
and `HRT=true` when `BioCalculated=true`. With the TSS StandardTarget and a valid
Conversion, enable SRT for tanks holding the system sludge inventory, including
settling tanks even if their HRT/BioCalculated flags are false. Without the TSS
mapping, leave SRT off and report the missing prerequisite. Auxiliary virtual
tanks, such as a dedicated chemical phosphorus removal tank, normally use
`HRT=true` and `SRT=false`, even when TSS mapping exists. Identify them by their
documented modeling role and record any case-specific exception; do not enable
SRT for every tank solely because the TSS Target is present. Legacy input may
generate HRT=true for every tank; review and explicitly set the intended
accounting boundary. These flags select statistics, not biological activity or
physical solids retention, and cannot fix bacterial washout.

`create-dataset` and `update-dataset` also accept `--async`, `--wait`,
`--operation-wait-timeout`, `--operation-poll-interval`, and
`--idempotency-key`. The backend performs the same parsing, automatic
`changeValueDataSet` mapping, and linked Project synchronization in either
mode.

When a Project is later calculated, `Solution.Variable.Value` is the runtime
baseline for `Inflow` and `Flow`. The backend additively shifts each complete
series from its DataSet `time=0` value (`Inflow` first resolves and applies its
selected Conversion expression), clips negative values, and converts volume
Flow to `m3/s` and KLa Flow to `/s`. Every new KLa signal needs its matching
Solution Variable row; preserve /d in public Value/bounds and synchronize its
initial value deliberately when migrating an existing Solution.
`Measured` is not shifted; it remains the original observation series. See
[Calculation commands](calculation.md) for the formulas and an example.

When inspecting calculated aeration, use the `runtime_inputs` result, also
saved as `Result__RuntimeInputs__.json` and Excel RuntimeInputs/Aeration/
TankAeration tables. `signals` distinguishes RawValue from EffectiveValue with
Kind/Unit; `aeration` records source/reference KLa, final corrected KLa, water
temperature and saturation; `tank_aeration` provides per-Tank transfer. KLa is
/d, saturation mg O₂/L and modeled oxygen transfer kg O₂/d. Respect the status,
units and output-time sampling metadata. If runtime evidence is unavailable,
report that absence instead of treating raw input as closed-loop output or
inferring real blower power from KLa alone.

The default Solution only provides identity mappings for Targets whose symbols
match BioModel Components. For aggregate Targets such as `COD`, `TIN`, `TN`,
`TP`, `TSS`, or `TS`, inspect and complete `Conversion` explicitly before
creating the Project. Use coefficients supported by the source definition,
BioModel Composition, or a transparent unit conversion; coefficients may be
literal numbers or expressions/direct BioModel Parameter references. Preserve a
defined Parameter such as `i_N_S_U` in the Conversion cell instead of forcing
its current value into a number. The calculation resolves it from the current
Project Variable values. Verify that referenced Parameters exist, are finite,
and are unit-compatible; do not infer a formula from the Target abbreviation
alone. For example, standard `TIN` may map to
`S_NHx=1` and `S_NOx=1`, while `TSS` normally uses model-specific `i_TSS_*`
coefficients for particulate Components. Do not add `S_N2` to TIN without a
source definition, and in this BioModel context interpret `TS` as total sulfur,
not total solids or a synonym for TSS. Use `--json` for
reviewed mappings and record formulas and units in the Project description. A
structurally valid but blank or all-zero Conversion row is not a valid
scientific mapping. The same rule applies to any other Target: resolve its
meaning and units, use direct identity first, derive only source/Composition-
supported coefficients, and stop as `unresolved` when candidates conflict or
the component fractionation is underdetermined. Nonlinear definitions or
definitions requiring an absent state variable cannot be represented by
Conversion alone.

For synchronization, the command argument is the Release ID and the response
contains the target Draft ID. For release, the argument is the Draft ID and the
response contains a new Release ID. Treat these as different records.

For Project create and update responses, require `success: true` and a positive
`id`. For synchronization, require `sourceId` to equal the input Release ID and
treat `id` as the target Draft ID. For release, require `sourceId` to equal the
input Draft ID, treat `id` as the new Release ID, and require `version >= 1`.

With `--async`, Project create/update returns `operationId` and an initial
`status` instead of a Project result. Add `--wait` to wait for the operation and
receive the final Project JSON, or use `wait-operation` separately. For retries,
pass a stable `--idempotency-key`; reusing it with a different payload is a
backend conflict and must be corrected rather than retried blindly.

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
