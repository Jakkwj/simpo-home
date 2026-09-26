# DataSet JSON Format

Generate a UTF-8 JSON object containing these eight required tables and only the
optional graph object:

```text
Unit, Target, Tank, Pump, Measured, Inflow, Flow, Connection
optional: jointGraphJson
```

Every table is an array of row objects. Column keys are consecutive decimal
strings in natural order: `"0"`, `"1"`, ... `"10"`; never serialize them in
lexicographic order such as `"0"`, `"1"`, `"10"`, `"2"`.

## Fixed tables

### Unit

```json
[
  {"0":"Time","1":"Volume","2":"Flow","3":"Area","4":"Height"},
  {"0":"day","1":"m3","2":"m3/d","3":"m2","4":"m"}
]
```

The time value may be `day`, `hour`, `minute`, or `second`; preserve the
source time basis instead of converting a batch experiment only to satisfy a
template.

### Target

Use the model-target reference and this header:

```json
{"0":"Symbol","1":"Unit","2":"Name","3":"Description","4":"Oxygen","5":"TSS"}
```

Symbols must be unique and must not use reserved node words. Marker cells are
JSON booleans, not the strings `"true"` and `"false"`. At most one target may
be marked `Oxygen: true` and at most one may be marked `TSS: true`; leave all
markers false when the model/DataSet has no dissolved-oxygen or total-solids
target. The backend does not require either marker to be present.

### Tank

```json
{"0":"Name","1":"Type","2":"BioCalculated","3":"Volume","4":"ConstantVolume","5":"SettlingFactor","6":"DiffuserNumber","7":"DiffuserDepth","8":"AlphaFactor","9":"BetaFactor"}
```

- `CSTR`: `BioCalculated=true`; numeric `Volume`; `SettlingFactor=null`;
  nonnegative diffuser count/depth; alpha and beta from 0 to 1.
- `Point Settling`: `BioCalculated=false`; `Volume=[outlet, blanket]`;
  `SettlingFactor` from 0 to 1; diffuser/alpha/beta cells are `null`.

### Pump

Use an empty array when no pump exists. Otherwise start with:

```json
{"0":"Name","1":"Type","2":"SOTEa","3":"SOTEb","4":"SOTEc"}
```

An aeration device uses `Type: "Air"`. Its name is used as `From` in an
aeration Connection row.

### Connection

```json
{"0":"From","1":"Flow","2":"Into"}
```

`From` is an Inflow, Pump, CSTR name, or a point settler's `_Outlet` or
`_Blanket`. `Into` is a tank name, `Outflow`, or `Wasted`. Generated hydraulic
expressions use defined Flow names with `+` and `-`. Pump connections describe
aeration and are excluded from liquid-flow balance.

## Time-series tables

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

The SIMPO parser invoked by `simpo create-dataset --json` is the authoritative
validator and follows the backend version currently in use. Before submission,
review the JSON in the current session for headers, naturally ordered numeric
keys, names, table references, initial flow values, expression syntax, and
constant-volume hydraulic balance. Do not treat a copied local validator as a
guarantee of compatibility with a newer backend format. Parser acceptance still
does not prove biological performance or equipment adequacy.

Submit the JSON object itself, not a wrapper containing `DataSet`, `Answer`,
`Description`, metadata, or a BioModel recommendation. Put narrative material
in `--description` instead.
