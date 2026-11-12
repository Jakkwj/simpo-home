# DataSet JSON Format

Generate a UTF-8 JSON object containing these eight required tables, the optional
Environment table, and the optional graph object:

```text
Unit, Target, Tank, Pump, Measured, Inflow, Flow, Connection
optional: Environment, jointGraphJson
```

Every table is an array of row objects. Column keys are consecutive decimal
strings in natural order: `"0"`, `"1"`, ... `"10"`; never serialize them in
lexicographic order such as `"0"`, `"1"`, `"10"`, `"2"`.

## Fixed tables

### Unit

```json
[
  {"0":"Time","1":"Volume","2":"Flow","3":"Area","4":"Height","5":"T"},
  {"0":"day","1":"m3","2":"m3/d","3":"m2","4":"m","5":"℃"}
]
```

The time value may be `day`, `hour`, `minute`, or `second`; preserve the
source time basis instead of converting a batch experiment only to satisfy a
template.

`Time` controls the timestamps and may be `hour` while `Flow` remains `m3/d`.
The current parser fixes Volume to `m3`, Flow to `m3/d`, Area to `m2`, and Height
to `m`; convert source values to these units and record the conversion. Do not
change the Flow unit to `m3/h` merely because the time-series axis uses hours.
`T` is the sixth column, after `Height`, and is fixed to Celsius. Write `℃`;
the parser also accepts `°C` and `degC`. Older files without this column use
Celsius. Convert Kelvin/Fahrenheit measurements explicitly before submission.

### Target

Use the model-target reference and this header:

```json
{"0":"Symbol","1":"Unit","2":"StandardTarget","3":"Name","4":"Description"}
```

Symbols must be unique and must not use reserved node words. `T` and `t` are
reserved, including as Target, Tank, Pump, Inflow, and Flow names. Store water
temperature in `Environment`, not as a Target. `StandardTarget`
is `""`, `"Dissolved Oxygen"`, or `"Total Suspended Solids"`. At most one Target
may use each nonempty value; use `""` when neither role applies. Historical
Oxygen/TSS boolean columns are accepted only while reading old data and must not
be written by this workflow.

### Tank

```json
{"0":"Name","1":"Type","2":"BioCalculated","3":"Volume","4":"ConstantVolume","5":"SettlingFactor","6":"DiffuserNumber","7":"DiffuserDepth","8":"AlphaFactor","9":"BetaFactor"}
```

- `CSTR`: `BioCalculated=true`; numeric `Volume`; `SettlingFactor=null`;
  nonnegative diffuser count/depth; alpha and beta from 0 to 1.
- `Point Settling`: normally `BioCalculated=false`; use `true` when biological
  reactions in the settler are part of the reviewed model;
  `Volume=[outlet, blanket]`;
  `SettlingFactor` from 0 to 1; diffuser/alpha/beta cells are `null`.

For later Project Retention, a settling tank with `BioCalculated=false` should
have HRT off; if `BioCalculated=true`, HRT should be on. Its SRT inclusion is
independent: include relevant sludge inventories when a TSS StandardTarget and
valid Project Conversion exist.

Auxiliary virtual tanks, for example a dedicated tank simulating chemical
phosphorus removal, normally have Project Retention `HRT=true`, `SRT=false`.
Record their modeling role so Project creation includes their volume in HRT
but excludes their solids inventory from SRT, even when TSS mapping is present.
Document any case-specific exception rather than inferring one from the name.

### Pump

Use an empty array when no pump exists. Otherwise start with:

```json
{"0":"Name","1":"Type","2":"SOTEa","3":"SOTEb","4":"SOTEc","5":"θ"}
```

An aeration device uses `Type: "Air"`. Its name is used as `From` in an
aeration Connection row.

The public JSON/XLSX header is `θ`, after `SOTEc`; the internal field is
`ThetaFactor`. The legacy `ThetaFactor` header is readable, but new output uses
`θ`. It must be finite and positive, with a finite positive multiplier across
0–40°C. Missing columns or blank cells default to **1**, preserving the old
transfer coefficient. The web editor starts new Pumps at **1.024**; this is an
empirical starting assumption, not an inferred equipment measurement.

Pump aeration multiplies its transfer coefficient by `θ**(T - 20)` using the
receiving Tank's water temperature. This multiplier applies to the complete
oxygen driving force, not only its saturation term. Set θ to 1 to disable this
coefficient correction. Direct Tank `KLa` inputs are not multiplied by Pump θ.
Kinetic factors such as `theta_H` in BioModel Rate are separate parameters;
never substitute the Pump coefficient for a biological temperature factor.

### Connection

```json
{"0":"From","1":"Flow","2":"Into"}
```

`From` is an Inflow, Pump, CSTR name, or a point settler's `_Outlet` or
`_Blanket`. `Into` is a tank name, `Outflow`, or `Wasted`. Generated hydraulic
expressions use defined Flow names with `+` and `-`. Pump connections describe
aeration and are excluded from liquid-flow balance.

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

With Forward Euler, Pump and direct-KLa aeration use the Benson–Krause
freshwater saturation relation at 1 atm. The fixed 20°C reference and missing-T
value are **9.092426042885567 mg O₂/L**. Pump aeration also uses its Tank's β.
The stored 0–40°C saturation table has 4,001 values at 0.01°C spacing: exact
grid matches use stored values; other temperatures use the equation without
rounding or table interpolation. Do not substitute a BSM calibration or infer
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

Use the DataSet Flow unit. Every Connection expression identifier must be a
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

Submit the JSON object itself, not a wrapper containing `DataSet`, `Answer`,
`Description`, metadata, or a BioModel recommendation. Put narrative material
in Description instead.
