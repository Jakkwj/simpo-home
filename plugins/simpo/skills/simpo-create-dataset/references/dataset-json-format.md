# DataSet JSON Format

Generate a UTF-8 JSON object using the tables supported by the target parser:

```text
required base: Unit, Target, Measured, Inflow, Flow, Connection
at least one populated tank table: CSTRTank, PointSettlingTank, TakacsSettlerTank (or legacy Tank)
pumps as applicable: AirPump, KLaPump
optional: Environment, Controller, ControllerConfig, PerformanceMetric, jointGraphJson
legacy inputs: Tank, Pump, compact ControlLoop/ControlLoopConfig, and module-based control tables
```

New output uses type-specific tank and pump tables. Include a real tank row
and at least one Target. For a plant without pumps, omit the pump tables.
Unused equipment sheets may be header-only. Omit `ControllerConfig` for a
fresh controller using defaults. If supplied, its JSON header needs a data
row. Preserve the original representation when editing existing detail.

Every table is an array of row objects. Column keys are consecutive decimal
strings in natural order: `"0"`, `"1"`, ... `"10"`; never serialize them in
lexicographic order such as `"0"`, `"1"`, `"10"`, `"2"`.

## Fixed tables

### Unit

```json
[
  {"0":"Time","1":"Volume","2":"Flow","3":"Area","4":"Height","5":"T","6":"KLa"},
  {"0":"day","1":"m3","2":"m3/d","3":"m2","4":"m","5":"℃","6":"/d"}
]
```

The time value may be `day`, `hour`, `minute`, or `second`; preserve the
source time basis instead of converting a batch experiment only to satisfy a
template.

`Time` controls the timestamps and may be `hour` while volume Flow remains `m3/d`.
The current parser fixes Volume to `m3`, Flow to `m3/d`, Area to `m2`, and Height
to `m`; convert source values to these units and record the conversion. Do not
change the Flow unit to `m3/h` merely because the time-series axis uses hours.
Water and AirPump flows use `m3/d`. Flows bound to KLaPump use `/d` (d⁻¹)
independently of `Unit.Time`. The optional seventh Unit column makes that fixed
coefficient unit explicit in JSON and appears in the current workbook.
`T` is the sixth column, after `Height`, and is fixed to Celsius. Write `℃`;
the parser also accepts `°C` and `degC`. Older files without this column use
Celsius. Convert Kelvin/Fahrenheit measurements explicitly before submission.

### Target

Use the model-target reference and this header:

```json
{"0":"Symbol","1":"Unit","2":"StandardTarget","3":"Name","4":"Description"}
```

Symbols must be unique. Reserved names include `T`, `Volume` and `KLa`
(case-insensitive) for Targets, Tanks, Pumps, Inflows and Flows. Store water
temperature in `Environment`, not as a Target. `StandardTarget`
is `""`, `"Dissolved Oxygen"`, or `"Total Suspended Solids"`. At most one Target
may use each nonempty value; use `""` when neither role applies. Historical
Oxygen/TSS boolean columns are accepted only while reading old data and must not
be written by this workflow.

### Tank type tables

Use the following input fields in new JSON tables:

```text
CSTRTank:
Name | BioCalculated | ConstantVolume | Volume | DiffuserNumber |
DiffuserDepth(m) | AlphaFactor | BetaFactor | SaturationModel | SaturationValue |
InletLagSeconds

PointSettlingTank:
Name | BioCalculated | ConstantVolume | OutletVolume | BlanketVolume | SettlingFactor

TakacsSettlerTank:
Name | BioCalculated | ConstantVolume | Area | Height | FeedLayer | LayerCount |
V0Max(m/d) | V0(m/d) | Rh(m3/gSS) | Rp(m3/gSS) | Fns | Xt(gSS/m3)
```

The sheet name determines the type; do not add a `Type` column. Names must be
unique. Set `BioCalculated` from the process model. For a CSTR or point
settler, preserve the reviewed `ConstantVolume` setting. The Takács model
uses fixed water depth and requires `ConstantVolume=true`. An explicit
`false` fails validation. CSTR volume and Takács area/height
must be positive; diffuser count/depth are nonnegative and alpha/beta are from
0 to 1. Point-settler `SettlingFactor` is from 0 to 1. Type-specific units in
headers are fixed; shared geometry units come from Unit.

A Takács physical tank expands to `Name_1` through `Name_N`, numbered bottom to
top. `LayerCount` is a strict integer in 3…10 (10 is the current product support limit, not a physical limit); `FeedLayer` is a strict integer in 2…N−1. For BSM1,
use ten layers and `FeedLayer=6` counted from the bottom, with `Area=1500 m2`,
`Height=4 m`, `V0Max=250 m/d`, `V0=474 m/d`, `Rh=0.000576 m3/gSS`,
`Rp=0.00286 m3/gSS`, `Fns=0.00228`, and `Xt=3000 gSS/m3`. These are benchmark
parameters, not general clarifier design defaults. Inflow uses the physical
name and is routed by FeedLayer; outlets use explicit layer names. Measured
states use the layer names. The tank volume is Area × Height, and each layer
has one equal share (600 m³ for a BSM1 layer). In the workbook, `Total Height`
maps to JSON `Height` and `Volume` is calculated from the geometry. Dash sets
the layer count at creation. Select it before mapping observations and branch endpoints.
Preserve the official initial states for each
benchmark case instead of inventing a uniform layer profile.

The legacy unified Tank header remains readable:

```json
{"0":"Name","1":"Type","2":"BioCalculated","3":"Volume","4":"ConstantVolume","5":"SettlingFactor","6":"DiffuserNumber","7":"DiffuserDepth","8":"AlphaFactor","9":"BetaFactor"}
```

- `CSTR`: normally `BioCalculated=true`; numeric `Volume`; `SettlingFactor=null`;
  nonnegative diffuser count/depth; alpha and beta from 0 to 1.
- `Point Settling`: normally `BioCalculated=false`; use `true` when biological
  reactions in the settler are part of the reviewed model;
  `Volume=[outlet, blanket]`;
  `SettlingFactor` from 0 to 1; diffuser/alpha/beta cells are `null`.

Use one tank representation throughout. Populated typed Tank tables take
precedence over the legacy Tank table. When converting, carry every legacy
tank into its type table. `KLa`/`KLa(/d)` Tank input fields are rejected,
including a header over blank cells or an explicit zero.
Migrate old files offline to new copies using Flow plus KLaPump; preserve the
source and use θ=1 when preserving the old uncorrected transfer coefficient.

For CSTR workbook input, `AlphaFactor(α)` and `BetaFactor(β)` map to JSON
`AlphaFactor` and `BetaFactor`. The `OxygenSaturationModel` column maps to
`SaturationModel`. `SaturationValue` uses the same name in both formats.
Choose the saturation model from the process specification:

- `Freshwater` (default): the existing Benson–Krause freshwater relation at
  1 atm. AirPump uses the Tank's BetaFactor; KLaPump does
  not add that AirPump-specific factor.
- `Constant`: `SaturationValue` is required, finite and nonnegative, fixed
  unit mg O₂/L; it is already the final effective saturation.
- `BSM2`: the benchmark temperature-dependent saturation relation, calibrated
  to approximately 8 mg O₂/L at 15°C. It also returns the final effective value.

Do not multiply Constant or BSM2 saturation by BetaFactor again.
`SaturationValue` only applies to Constant. Classic BSM1 uses fixed biological
parameters, `SaturationModel=Constant`, `SaturationValue=8`, and KLaPump `θ=1`;
it has no dynamic temperature state and needs no water-temperature series.

**Mixed Inlet Response.** Set `InletLagSeconds` on the receiving CSTR. Zero
or blank gives instantaneous mixing. A positive value sets a first-order lag
on the combined liquid flow and on each component's mass loading. The BSM1
Simulink reproduction sets 8.64 seconds on Tank1 only. This is independent of
the input interpolation and output sampling interval. Use Forward Euler and
constant-volume hydraulics. Along the downstream route, a split needs one
identifiable residual outlet expression alongside any prescribed branches.

In the workbook, select `Instantaneous` or `First-order lag` in
`MixedInletResponse`. Enter a positive `TimeConstant` in seconds for the
latter. When reproducing an existing benchmark, start from its saved DataSet
so the case retains its original startup conditions.

For later Project Retention, a settling tank with `BioCalculated=false` should
have HRT off; if `BioCalculated=true`, HRT should be on. Its SRT inclusion is
independent: include relevant sludge inventories when a TSS StandardTarget and
valid Project Conversion exist.

Auxiliary virtual tanks, for example a dedicated tank simulating chemical
phosphorus removal, normally have Project Retention `HRT=true`, `SRT=false`.
Record their modeling role so Project creation includes their volume in HRT
but excludes their solids inventory from SRT, even when TSS mapping is present.
Document any case-specific exception rather than inferring one from the name.

### AirPump and KLaPump

New AirPump output starts with:

```json
{"0":"Name","1":"SOTEa","2":"SOTEb","3":"SOTEc","4":"θ"}
```

New KLaPump output starts with:

```json
{"0":"Name","1":"θ","2":"TRef"}
```

Both use the Pump name as Connection.From. The type comes from the table name;
KLaPump does not store the KLa value or its series in the Pump row. AirPump has
a fixed 20°C reference and must not contain TRef. KLaPump TRef defaults to 20°C
and means the reference temperature of its supplied coefficient.

The public JSON/XLSX header is `θ`, after `SOTEc`; the internal field is
`ThetaFactor` (`θ` follows Name in KLaPump). The legacy `ThetaFactor` header is
readable, but new output uses `θ`. It must be finite and positive, with a finite
positive multiplier across 0–40°C. Missing columns or blank cells default to
**1**. Use source/test evidence for an explicit value such as 1.024.

AirPump multiplies its transfer coefficient by `θ**(T - 20)`; KLaPump uses
`θ**(T - TRef)`. Each receiving Tank uses its own water temperature. Missing T
means 20°C, so KLaPump still applies `θ**(20 - TRef)`, not automatically 1.
The multiplier applies to the complete oxygen driving force. Set θ to 1 to
disable it. Legacy direct `Tank.KLa` is no longer supported.
For BSM2 transfer compatibility explicitly use `TRef=15`, `θ=1.024` and the
reviewed temperature data; this does not implement BSM2's complete thermal model.
Kinetic factors such as `theta_H` in BioModel Rate are separate parameters;
never substitute the Pump coefficient for a biological temperature factor.

Legacy `Pump` rows with header `Name | Type | SOTEa | SOTEb | SOTEc | θ` and
`Type=Air` remain readable. Populated legacy and typed Pump tables are merged;
duplicate names are errors, and an empty table cannot hide populated siblings.
Do not re-export a pump in both its typed and legacy tables.

### Connection

```json
{"0":"From","1":"Flow","2":"Into"}
```

`From` is an Inflow, Pump, CSTR name, or a point settler's `_Outlet` or
`_Blanket`, or a Takács explicit layer name. `Into` is a physical tank name,
`Outflow`, or `Wasted`; Takács inputs use the parent name, not the feed-layer
name. Generated hydraulic
expressions use defined Flow names with `+` and `-`. Pump connections describe
aeration and are excluded from liquid-flow balance.

KLaPump connections must name one Flow signal directly, without expressions or
numeric constants, and target a CSTR. A single signal may serve multiple Tanks;
each receives the full coefficient, with no split by volume or number of links.
All KLaPumps sharing a signal must use the same TRef. Signal kinds and units
are inferred from all connections; a signal cannot also be used as volume
flow. Each Tank may receive only one KLaPump connection and cannot combine it
with AirPump. Old Tank.KLa fields and controller targets are rejected. KLa does not contribute to hydraulic flow, HRT/SRT or
air-volume accounting, and cannot alone determine real blower power.

For BSM1, set the `Flow` block named `KLa_34` to 240 at time zero.
Add the two Connection rows `KLaPump34 | KLa_34 | Tank3` and
`KLaPump34 | KLa_34 | Tank4`. With θ = 1 each reactor receives 240 d⁻¹.
Use a separate `KLa_5` Flow and pump for Tank5, fixed at 84 d⁻¹ in open loop.

### Controller

Each compact `Controller` row binds one sensor, one continuous PI and one
actuator. New JSON and Excel use these 13 columns in the same order.

```text
Name | SensorPreset | SensorLocation | SensorTarget | SensorUpperLimit |
ControllerSetpoint | ControllerGain | ControllerIntegralTime | ControllerTrackingTime |
ControlHandle | HandleLowerLimit | HandleUpperLimit | SensorLowerLimit
```

`SensorLocation` names a Tank, settler layer/zone or Inflow. `SensorTarget`
names a DataSet Target. Feedback reads its simulated value at that location.
Use an independent named Flow for `ControlHandle`. A hydraulic expression
such as `Q_0+Q_r` belongs to Connection. A KLa handle such as `KLa_5`
carries d⁻¹ at the pump reference temperature. Each handle has one writer.
The setpoint must be within the sensor range, with upper > lower. A missing
or blank `SensorLowerLimit` defaults to zero, including on older 12-column
rows. Provide a finite PI gain in handle units per sensor unit, positive
integral and tracking times **in days**, and nonnegative ordered handle limits.
Keep the Flow definition and a numeric sample at time zero for a controlled
handle. For the BSM1 closed loops, zero suffices for both `Q_a` and `KLa_5`.
During closed-loop operation the actuator supplies the effective value.

These are the two visible feedback rows of the BSM1 closed-loop cases. The
quoted column numbers refer to the header above. Open-loop cases omit the rows.

```json
[
  {"0":"BSM1_Qintr","1":"BSM_Class_B0","2":"Tank2","3":"S_NO","4":20,"5":1,"6":10000,"7":0.025,"8":0.015,"9":"Q_a","10":0,"11":92230,"12":0},
  {"0":"BSM1_KLa5","1":"BSM_Class_A","2":"Tank5","3":"S_O2","4":10,"5":2,"6":25,"7":0.002,"8":0.001,"9":"KLa_5","10":0,"11":360,"12":0}
]
```

Choose one of the six sensor presets. `BSM_Class_A`, `BSM_Class_B0` and
`BSM_Class_C0` have continuous responses with T90 of 1, 10 and 20 minutes.
`BSM_Class_B1` and `BSM_Class_C1` also have T90 of 10 and 20 minutes and
sample every 5 minutes. `BSM_Class_D` samples every 30 minutes with one
sample of delay. PI tuning and the choice of noise source are independent of
the sensor preset.

**Saved configuration.** `ControllerConfig` is a table with header
`{"0":"JSON"}` and one row containing a serialized object. Preserve its
`loops` snapshots, sensor noise channels, PI and actuator states, and any
`controllerIds` when updating a saved case. Dash uses these stable IDs when
renaming a controller. For fresh rows the parser creates zero-state controls,
ideal actuators and noise-free sensors. The two visible benchmark rows alone
therefore do not reproduce an archived run. The 500-day closed-loop startup
uses ideal measurements. The three closed-loop weather cases retain their
conditioned states and BSM1 reference noise.

For a **new** controller named `BSM1_KLa5`, this is the entire optional
configuration table for seeded random noise. In an existing DataSet, merge the
per-sensor choice into its decoded configuration before serializing it again.

```json
[
  {"0":"JSON"},
  {"0":"{\"version\":1,\"loops\":{},\"sensorNoise\":{\"BSM1_KLa5\":{\"source\":\"random\",\"std\":0.25,\"sampleTime\":0.0006944444444444445,\"seed\":42}}}"}
]
```

`sampleTime` is the noise update interval in days (one minute above).
`std` must be positive and uses the measurement unit. Keep the integer seed
from 0 through 2147483645 to reproduce the noise. For the other modes the
per-sensor entry is simply `{"source":"none"}` or `{"source":"predefined"}`.
The latter selects a bundled BSM1 noise sequence on a one-minute grid covering
days 0–14, with standard deviation 2.5% of the configured sensor span.
Preserve the assigned reference channel when matching MATLAB. Use `random`
or `none` for runs outside its coverage.

For a new process, tune its measurement/handle pair in a saved Project.
Run a trial to compare entered settings or estimate selected parameters.
For estimation, the trial settles the plant at fixed inputs and compares a
small handle step with an unperturbed run from the same state. SIMPO uses
SIMC for gain and integral time and derives tracking time separately.
A weak or unsettled response can yield no estimate. Review the curves and
diagnosis before applying a candidate.

Excel retains the configuration in the `SimpoControllerConfig` document
property. Earlier compact JSON keys `ControlLoop` and `ControlLoopConfig`
are read as aliases. Keep compact rows and populated module-based rows in
separate input formats.

### Earlier module-based control tables

Control protocol signal-connections-v3 keeps Sensor, Controller and Actuator as
independent stateful modules. Names must be globally unique across the three
tables. Sensor declares Tank and Component in separate columns; Component is
a BioModel component symbol. Actuator.Target alone
declares a named Flow. Tank.KLa is not a valid target.

```text
Controller: Name | Type | Setpoint | Gain | IntegralTime | TrackingTime | Bias |
LowerLimit | UpperLimit | SampleTime | AntiWindup | InitialIntegral | InitialAntiWindup | Direction
Sensor: Name | Type | Tank | Component | LowerLimit | UpperLimit | NoiseStd | T90 |
DelayOrder | SampleTime | Ideal | NoiseSource | NoiseSeed | NoiseFile | NoiseColumn
Actuator: Name | Type | Target | LowerLimit | UpperLimit | T90 | DelayOrder | Ideal | InitialValue | InputGain
SignalConnection: From | To
```

The sensor source format is `split-tank-component`. Legacy `Source` values
remain readable: split `Tank.Component` at the last dot and export the two
columns above. When both formats are supplied, a populated Tank/Component pair
must be complete and agree with Source. Reject conflicts and partially filled
pairs; when both new fields are empty, an explicit legacy Source can supply
the binding. New output omits Source.

`From` and `To` contain module names. Optional `FromPort` and `ToPort` columns
can specify ports explicitly; omitted ports are inferred only when the module
types identify a unique supported connection. Current edges are
Sensor.Output → Controller.Measurement and Controller.Output → Actuator.Input.
`Actuator.InputGain` defaults to 1 when omitted or blank and must be finite and
positive. It scales the incoming command before actuator response and limits;
InitialValue and limits remain in actuator-output units. SignalConnection has
no Gain field; Controller.Gain remains the PI parameter.
One output may fan out; each input has one source; each Flow has one
actuator writer. Shared sensors have one shared measurement state. Actuators
retain independent response states and limits. Output branches must have
compatible units. Type=PI currently needs one measurement, a fixed Setpoint,
and SampleTime=0 (continuous solver-step update). Do not claim dynamic
setpoints, feedforward, cascade, MPC or arbitrary algebraic loops are supported.
NoiseSource is explicit none/random/predefined, never inferred from names.
Sensor.Type currently labels the configuration; it does not load class presets.
In split-module inputs, `Sensor.SampleTime` controls the noise grid.
`MeasurementInterval` controls any sample-and-hold measurement. The default
legacy `SourceKind=component` binds a BioModel component at a Tank.
For the compact format above, new bindings use DataSet Targets. Original
weather-case snapshots use reference noise column 1 for DO or 2 for nitrate
(column 0 is time), with absolute NoiseStd values of 0.25 and 0.5.

KLa controller output, Bias, limits and actuator initial/output values use /d
at TRef; temperature correction follows the actuator. KLa lower limits and
actuator initial values must be finite and nonnegative. Controller/sensor/
actuator time parameters retain their day basis, independently of Unit.Time.
Fully controlled Flow inputs cannot also be selected for input estimation.
At runtime the actuator overrides the current effective signal; it does not
overwrite or add to the original Flow samples. KLaPump and closed-loop
calculations currently require Forward Euler.

Migrate old workbooks offline into new files, retaining the source. Rename
ControlConnection to SignalConnection and move Controller-to-Actuator edge
Gain to the corresponding Actuator.InputGain, retaining explicit ports. A
unit edge Gain leaves an existing InputGain unchanged. Reject simultaneous
non-default values in both places, mixed ControlConnection/SignalConnection
tables, and non-unit Sensor-to-Controller Gain; do not silently multiply,
discard or reinterpret them. Legacy Controller endpoint columns must instead
become Sensor.Tank/Component, Actuator.Target and SignalConnection rows.

### Assessment

The optional **JSON key is `PerformanceMetric`**. Dash and the workbook
sheet use **Assessment**. The exported sheet follows `Connection` and
`Environment`, with columns `Name | Unit | StartDay | EndDay | Formula`.
Use the following canonical JSON layout. This table can be added to a DataSet
containing the BSM1 water-flow names `Q_a`, `Q_r`, `Q_w`.

```json
[
  {"0":"Name","1":"Formula","2":"Unit","3":"StartDay","4":"EndDay"},
  {"0":"PE","1":"Mean(0.004 * Q_a + 0.008 * Q_r + 0.05 * Q_w)","2":"kWh/d","3":7,"4":14}
]
```

Give each metric a unique name, scalar formula and nonempty unit (`-` for
a dimensionless index). Times are **days** for all DataSet time units. Blank
window endpoints use the first or last dynamic result time. BSM1 evaluates
days 7–14 for weather runs and 493–500 for the two 500-day startup runs.

Write formulas as in Dash. A bare Flow name reads the effective signal,
`Tank6_10.TSS` reads a Target, `Tank6_1.Volume` reads that layer's actual
volume, and `Tank5.KLa` reads the effective transfer coefficient applied to
Tank5. The latter is a result channel even though a Tank has no KLa input
column. `Branch("Tank6_10", "Outflow")` reads the actual liquid outlet
flow when the mixed-inlet run records the branch. A bare metric name reads
its scalar result. Use distinct identifiers for metrics and flows because
a bare name matching both resolves to the Flow.

Use case-sensitive `Mean`, `Integral`, `First`, `Last`, `Change`,
`Min`, `Max` and `If`. For example `Mean(If(Tank5.S_O2 < 2, 1, 0))`
gives the fraction of the evaluation window spent below the stated DO.
Mean and Integral weight the saved output by the duration to the next sample
in days. Combine metrics from
the same window without cycles, e.g. `5 * SP + AE + PE + 3 * EC + ME` for
BSM1 OCI when the five referenced metrics exist. Match the formulas to the
plant. BSM1's seven metrics use the benchmark's effluent weights, sludge
inventory, aeration/mixing energy, pumping coefficients and carbon dosing.

`Change(x)` and `Change(x, 0)` subtract the opening value from the closing
value. An optional negative integer literal moves only the closing value
back by that number of saved output samples, within the evaluation window.
For example, `Change(Tank1.Volume * Tank1.TSS, -1)` gives the change in Tank1
solids inventory up to the previous sample. BSM1 applies `-1` to the sum of
the inventories in all five reactors and ten settler layers. In the weather
cases the offset moves the endpoint to day 13 at 23:45 (15 minutes earlier).
In the startup cases it selects day 499 at 20:00 (4 hours earlier).
The opening inventory, average wasting rate and seven-day divisor stay the same.

## Time-series tables

### Environment

`Environment` is optional and may be `[]`. Currently only the uppercase
identifier `T` is supported; do not write the old table/header `Property` or
the identifier `Temperature`. Each block starts with a time column headed
`Tank` / `Environment`; the other columns contain the Tank name / `T`:

```json
[
  {"0":"Tank","1":"AerationTank","2":"Tank","3":"Settler_Blanket"},
  {"0":"Environment","1":"T","2":"Environment","3":"T"},
  {"0":0,"1":20,"2":0,"3":18},
  {"0":1,"1":21,"2":0.5,"3":19}
]
```

- Times use `Unit.Time`; values use `Unit.T` and must be finite, non-Boolean
  numbers from **0 to 40°C**. Every populated series starts with a valid value
  at time 0. A single value at 0 represents a constant temperature.
- Every `(Tank, Environment)` pair is unique across all blocks. A subset of
  Tanks is allowed; each Tank must exist. For a point settler use the physical
  Tank name or `TankName_Outlet` / `TankName_Blanket`. Each zone first uses its
  own series, then its parent's, then the **20°C** fallback.
- Times within each block are finite, nonnegative, strictly increasing and
  unique. Different blocks may have different times. Blank values are missing
  samples, not zeros; preserve them and never align by row number alone.
- Dynamic `previous` switches at each sample; `linear` interpolates each
  column's valid samples. Both hold the final valid value. Input events are
  protected from `resolution_rate` downsampling, and Forward Euler steps stop
  at the next input event instead of skipping it.
- Steady state uses each series' average temperature with
  `steady_state_input_average_method`: `previous` time-weights the step signal,
  `linear` integrates the piecewise-linear signal, and `arithmetic` averages
  valid samples. There is no Flow weighting. Time averages cover the first-to-last
  valid sample interval; repeat the last temperature at the desired endpoint
  if its held duration should count. Combined steady/dynamic mode restores
  the original series for its dynamic phase.

Temperature is used without a `Solution.Variable.Value` offset. Do not add
a temperature Variable, Conversion, or measured-state Constraint. A missing
applicable series uses 20°C, which must be disclosed as a default, not a
measurement. Saturation and nonlinear Rate factors are evaluated at the sampled
or averaged temperature; averaging temperatures is not averaging reaction rates.

With Forward Euler and `SaturationModel=Freshwater`, aeration uses the
Benson–Krause relation at 1 atm. Its 20°C/missing-T value is
**9.092426042885567 mg O₂/L**. AirPump also uses its Tank's β.
The stored 0–40°C saturation table has 4,001 values at 0.01°C spacing: exact
grid matches use stored values; other temperatures use the equation without
rounding or table interpolation. Select Constant/BSM2 explicitly when required;
do not substitute a BSM calibration into the Freshwater model or infer
air temperature, pressure, salinity, or ORP support from this water-temperature
input. The equation is documented in the
[DataSet editing guide](https://www.simpowater.com/docs/Tutorials/DataSet/Edit#do-temperature).
For biological corrections, use `T` directly in `BioModel.Matrix.Rate` under
the BioModel analysis rules; these Rates currently require Forward Euler.

### Measured

`Measured` may be an empty array when no initial or observed tank values are
available. If it is nonempty, every monitoring-point block must contain every
symbol from `Target` exactly once. The first data row at time `0` must contain a
numeric value for every target; do not use `null` merely to avoid documenting an
initial-condition assumption.

Each monitoring-point block begins with a separator column. Example with two
targets at two points:

```json
[
  {"0":"Tank","1":"AerationTank","2":"AerationTank","3":"Tank","4":"Settler_Outlet","5":"Settler_Outlet"},
  {"0":"Target","1":"S_O2","2":"X_TSS","3":"Target","4":"S_O2","5":"X_TSS"},
  {"0":0,"1":2,"2":3000,"3":0,"4":0,"5":20}
]
```

Use the exact CSTR name. A point settler has separate `Name_Outlet` and
`Name_Blanket` monitoring points. Initial values must have an evidence or
assumption basis; later rows may contain `null` result cells.

### Inflow

`Inflow` may be empty only when the DataSet has no external material inflow. If
it is nonempty, every named inflow block must contain every symbol from
`Target` exactly once. Use numeric zero for a known absent constituent; do not
omit target columns. This mirrors the backend parser's complete-target rule.

Use the same block shape, with `Inflow` as the first-row separator and `Target`
as the second-row separator:

```json
[
  {"0":"Inflow","1":"Influent","2":"Influent"},
  {"0":"Target","1":"S_F","2":"S_NHx"},
  {"0":0,"1":60,"2":28}
]
```

Define external carbon or chemical addition as a separate named Inflow when it
has a composition and flow.

### Flow

Each flow block is a time/value pair:

```json
[
  {"0":"Flow","1":"Qin","2":"Flow","3":"Qr"},
  {"0":0,"1":10000,"2":0,"3":10000}
]
```

Use m3/d for volume flows and /d for signals identified by KLaPump connections.
KLa samples must be finite, non-Boolean and nonnegative. Every Connection
expression identifier must be a
defined Flow name. The required `Connection` header may be the only row for a
closed batch reactor with no external inflow, flow, or liquid connection.

## Validation and submission

The SIMPO DataSet parser is the authoritative
validator and follows the backend version currently in use. Before submission,
review the JSON in the current session for headers, naturally ordered numeric
keys, names, table references, initial flow values, expression syntax, and
constant-volume hydraulic balance. Do not treat a copied local validator as a
guarantee of compatibility with a newer backend format. Parser acceptance still
does not prove biological performance or equipment adequacy.

For calculated results, distinguish the configured input from actual control
action. `runtime_inputs` / `Result__RuntimeInputs__.json` contains `signals`
(RawValue and EffectiveValue with Kind/Unit), `aeration` (per-source/reference
and temperature-corrected KLa), and `tank_aeration` (per-Tank transfer). Excel
uses RuntimeInputs, Aeration, TankAeration and their metadata/unit sheets. KLa
is /d, saturation is mg O₂/L, and modeled oxygen transfer is kg O₂/d. Missing
runtime evidence is `status=unavailable`, not permission to label raw Flow as
the closed-loop result. These are sampled output times, not every solver substep.

Submit the JSON object itself, not a wrapper containing `DataSet`, `Answer`,
`Description`, metadata, or a BioModel recommendation. Put narrative material
in Description instead.
