# Process Design Rules

Use these rules to convert design conditions into a preliminary wastewater
treatment process. They support transparent engineering estimates; they do not
replace local codes, detailed equipment design, pilot testing, calibration, or
simulation.

## Contents

1. Input hierarchy
2. Process selection
3. Preliminary calculations
4. Hydraulic topology
5. Assumptions and review

## 1. Input hierarchy

Keep these concepts separate:

- **Flow basis:** average daily, maximum daily, peak hourly, dry-weather, or
  wet-weather flow. State which basis sizes each unit.
- **Influent quality:** COD, BOD5, TSS, TN, TKN, NH4-N, NOx-N, TP, PO4-P,
  alkalinity, pH, temperature, and any industrial or inhibitory constituent.
- **Treatment target:** explicit effluent limits and their averaging period. Do
  not substitute a remembered regulation for a missing user requirement.
- **Constraints:** existing units, footprint, number of trains, redundancy,
  chemical availability, preferred process, discharge/reuse destination, or
  operating restrictions.

Ask for a missing flow basis or treatment target when it materially changes the
process. Secondary values may use an identified engineering assumption after
showing it to the user.

## 2. Process selection

- Use a carbon-removal process only when nitrogen and phosphorus limits do not
  require biological nutrient removal.
- Include aerobic SRT and capacity adequate for nitrification when ammonia must
  be removed. Do not assert that a selected SRT is adequate without stating the
  assumed temperature and design basis.
- Include an anoxic zone and nitrate recycle when total nitrogen removal is
  required. Check whether readily biodegradable carbon is likely sufficient;
  label any external-carbon proposal and dosing basis.
- Include an anaerobic zone and use an ASM2D-compatible target set when
  biological phosphorus removal is material. Identify chemical phosphorus
  removal separately when proposed.
- Use a point settler only as the simplified SIMPO separator representation
  documented for this workflow. Its outlet and blanket are referenced as
  `TankName_Outlet` and `TankName_Blanket`.
- Explain why the chosen configuration fits the influent ratios, limits, and
  constraints. A plausible configuration is not proof of compliance.

## 3. Preliminary calculations

Use consistent units, normally `day`, `m3`, `m3/d`, `m2`, and `m`.

### Volumes and retention times

For a zone sized from average flow:

```text
V = Q_design * HRT_hours / 24
```

State whether HRT uses plant influent only or includes recycle flow. Use the
same convention in the explanation and JSON.

### Recycle and wasting flows

Convert every ratio into an explicit flow:

```text
Q_return = return_ratio * Q_basis
Q_internal_recycle = recycle_ratio * Q_basis
```

Do not infer sludge wasting from SRT without stating the solids inventory and
waste concentration basis. If those data are unavailable, mark `Qw` as a
preliminary operating assumption rather than a calculated fact.

### Oxygen and air

Separate carbon oxidation, nitrification demand, denitrification credit, and
other material oxygen terms. Record the assumed alpha, beta, transfer
efficiency, diffuser depth, and safety/design factors used to convert oxygen
demand to air flow. The DataSet Pump row stores the SOTE correlation
coefficients; a default such as `SOTEa=0.3`, `SOTEb=0`, `SOTEc=0` is an explicit
design assumption, not manufacturer data.

### Settling

For `Point Settling`, store the two compartment volumes as
`[outlet_volume, blanket_volume]` and a `SettlingFactor` between 0 and 1. Explain
the assumed split and factor. Do not claim a detailed clarifier design from this
simplified representation.

## 4. Hydraulic topology

- Define every independent flow in `Flow` and use its exact name in
  `Connection` expressions.
- Use only addition and subtraction in generated flow expressions. Prefer
  explicit named split flows over multiplication in a connection expression.
- For every constant-volume liquid tank, the symbolic sum of incoming flows
  must equal the symbolic sum of outgoing flows.
- Treat both `Settler_Outlet` and `Settler_Blanket` as outlets of the parent
  point-settling tank when checking balance.
- Treat Pump-to-Tank connections as aeration links; exclude them from liquid
  hydraulic balance.
- Include all system boundaries: every influent, final `Outflow`, return stream,
  internal recycle, bypass if explicitly designed, and `Wasted` sludge stream.

Produce a balance table before creation:

| Tank | Inflow expression | Outflow expression | Symbolic result | Initial numeric result |
| --- | --- | --- | --- | --- |
| `ExampleTank` | `Qin+Qr` | `Qmain+Qr` | `Qin-Qmain` | value and unit |

Only report a balanced tank when both the expression and the initial values
close within reasonable numeric tolerance.

## 5. Assumptions and review

Classify important inputs as one of:

- user supplied;
- source supplied;
- calculated from stated inputs;
- engineering assumption;
- unresolved.

Place assumptions and unresolved items in the creation review and Markdown
description. Never hide an underdetermined influent fractionation, uncertain
temperature, missing peak factor, or unverified equipment coefficient behind a
single precise-looking number.
