# Ionization Derivation Workflow

Use this workflow when the paper defines acid/base species and pH must be
calculated in SIMPO. `ionization_derive` controls whether missing Ionization
data may be derived; preserve rows explicitly reported by the paper even when
derivation is off. Include it only when the modeled
Component, its concentration basis, acid/base system, and equilibrium constants
are supported by the paper or by an explicitly disclosed external chemical
reference. Do not infer it from a Component name alone.

## 1. Use the exact SIMPO schema

Use this header row:

```json
{"0":"Symbol","1":"Compound","2":"Step","3":"Ionization","4":"Factor","5":"pK1","6":"pK2","7":"pK3","8":"pKw"}
```

- `Symbol` must be unique, must exist in `Component`, and must be a dissolved
  `S_` Component to match the frontend workflow. Do not add `pH` to `Component`
  or Ionization.
- `Compound` must be `Strong Acid`, `Weak Acid`, `Strong Base`, or `Weak Base`.
- `Step` must be `Mono`, `Di`, or `Tri`.
- `Ionization` must be `Complete`, `One Step`, or `Stepwise`.
- `Factor`, every used pK field, and `pKw` must be numeric values or simple
  slash fractions accepted by SIMPO, such as `1/14000` or `1/14/1000`.
  Parenthesized arithmetic such as `1/(14*1000)` is shown in the reference
  spreadsheet but is not accepted by the current JSON parser; simplify it
  before submission. Do not copy parenthetical literature
  alternatives such as `9.24(9.23)` into JSON; choose one documented value and
  explain the choice in the audit note.
- Put `pKw` in the first data row only. It must be non-null there and null in
  every later row. Row order therefore affects storage of `pKw` but does not
  establish chemical priority.

## 2. Select a parser-valid combination

Use these combinations:

| Compound | Step | Ionization | Required pK fields |
|---|---|---|---|
| Strong Acid/Base | Mono, Di, or Tri | Complete | none |
| Weak Acid/Base | Mono | One Step | pK1 |
| Weak Acid/Base | Di | Stepwise | pK1 and pK2 |
| Weak Acid/Base | Tri | Stepwise | pK1, pK2, and pK3 |

Set every unused pK field to `null`. Strong species must use `Complete`; weak
species must not. Mono weak species must use `One Step`, while Di/Tri weak
species must use `Stepwise`. These rules match the current SIMPO parser.

## 3. Establish the chemical and concentration basis

For every proposed row, record:

- the total dissolved Component represented by the state variable;
- its acid/base family and number of modeled dissociation steps;
- the Component's mass basis, such as mgN/L, mgS/L, mgC/L, or mg compound/L;
- the temperature and source for pK and pKw values;
- whether the supplied weak-base constant is pKb or the pKa of its conjugate
  acid.

Do not add Ionization for a mixed COD pool, an empirical Component, or a state
variable whose mass basis or acid/base family is unknown. Ask for review or omit
the whole table when the uncertainty materially changes pH.

## 4. Derive Factor

`Factor` converts the Component concentration from mg/L to mol/L. For a mass
basis with molar mass `M_basis` in g/mol:

```text
Factor = 1 / (M_basis * 1000)  mol/mg
```

Use the molar mass of the **reported concentration basis**, not automatically
the complete ion molar mass. Examples:

- nitrate or nitrite reported as N: derive `1/(14*1000)`, submit `1/14000`;
- sulfate or sulfide reported as S: derive `1/(32*1000)`, submit `1/32000`;
- carbonate reported as C: derive `1/(12*1000)`, submit `1/12000`;
- chloride reported as Cl: derive `1/(35.5*1000)`, submit `1/35500`.

If nitrate is reported as mg NO3/L rather than mg N/L, use the full nitrate
molar mass instead. State the basis explicitly in the audit note. Do not choose
a Factor merely because a similarly named row appears in a reference table.

## 5. Select pK values consistently

- For weak acids, enter stepwise pKa values in `pK1`, `pK2`, and `pK3`.
- SIMPO's weak-base formulas use pKb. If a source gives the conjugate-acid pKa,
  convert it at the same temperature:

  ```text
  pKb = pKw - pKa(conjugate acid)
  ```

- Preserve the order of stepwise constants. Do not average alternative values
  or combine constants measured under incompatible temperature/ionic-strength
  conditions.
- Use a pKw appropriate to the model temperature. `14` is a common value near
  25 °C, not a universal constant.

## 6. JSON example

The following illustrates schema and concentration-basis handling. The pK
values are examples and require source verification for the target model:

```json
"Ionization": [
  {"0":"Symbol","1":"Compound","2":"Step","3":"Ionization","4":"Factor","5":"pK1","6":"pK2","7":"pK3","8":"pKw"},
  {"0":"S_NO3","1":"Strong Acid","2":"Mono","3":"Complete","4":"1/14000","5":null,"6":null,"7":null,"8":14},
  {"0":"S_NO2","1":"Weak Acid","2":"Mono","3":"One Step","4":"1/14000","5":3.15,"6":null,"7":null,"8":null},
  {"0":"S_S2","1":"Weak Acid","2":"Di","3":"Stepwise","4":"1/32000","5":7.02,"6":13.9,"7":null,"8":null},
  {"0":"S_SO4","1":"Strong Acid","2":"Di","3":"Complete","4":"1/32000","5":null,"6":null,"7":null,"8":null}
]
```

## 7. Review and downstream setup

Show the proposed Ionization rows, Factor derivations, pK/pKw sources,
temperature, and material assumptions to the user before submission. Mark every
externally sourced value as derived/reference data rather than paper-extracted.

Ionization defines SIMPO's RIIC/pH relationship but is not sufficient by itself
to expose pH in a Project. Define `pH` as a DataSet Target and map it in Project
Conversion (normally with coefficient `1`). Rate formulas may reference `pH`
directly; do not create a `pH` Component.

Validate the complete BioModel with the current SIMPO parser. Parser acceptance
checks representation and syntax only; it does not prove that the selected
species, constants, or concentration bases are scientifically appropriate.
