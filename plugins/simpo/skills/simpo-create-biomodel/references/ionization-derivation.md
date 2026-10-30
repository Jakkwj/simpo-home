# Ionization Derivation Workflow

In paper and user-defined modes, assess dissolved Components when
`ionization_derive=on` (the default), even if the paper has no pH submodel.
Read this workflow before deciding to omit Ionization. Match the actual species
and concentration basis to the built-in SIMPO parameter table in section 6.
Its values are available reference defaults: their absence from the paper or
lack of live web access is not a reason to skip a matching row.

Use explicit, applicable paper/user values when provided; otherwise use the
built-in defaults and identify them as SIMPO reference data in the audit.
Unknown reference temperature does not block using an acknowledged SIMPO
default; do not claim a temperature-specific validation or invent a correction.
A known incompatible species, mass basis, or explicitly required condition must
be resolved or reported separately. Do not infer species from its symbol alone.
With derivation off, retain only source-reported rows. Verified workbook imports
preserve their original rows and values, including values different from these
defaults. Never overwrite them merely to match the reference table.

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
  alternatives into JSON; the built-in table already selects the primary value.
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
- the source for pK/pKw (built-in SIMPO defaults or applicable paper/user data);
- any explicitly given temperature conditions; disclose unspecified conditions
  without making them an automatic veto on built-in defaults;
- whether the supplied weak-base constant is pKb or the pKa of its conjugate
  acid.

Do not add Ionization for a mixed COD pool, an empirical Component, or a state
variable whose mass basis or acid/base family is unknown. Report unsupported
candidates separately; one unresolved species does not erase other supported
rows. Disclose the resulting limitation on pH coverage.

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

- Use the primary values in section 6 for supported species; the parenthetical
  alternatives from the original website are not selected or averaged.
- For weak acids, enter stepwise pKa values. SIMPO weak-base rows use pKb;
  the built-in Weak Base entries already use that convention, so do not
  convert them again. If a separate source gives conjugate-acid pKa, convert
  consistently using `pKb = pKw - pKa(conjugate acid)`.
- Use the built-in pKw default unless applicable paper/user data specifies
  another value. Store pKw in the first data row only. Do not mix it with
  incompatible condition-specific constants or invent temperature corrections.
- Record built-in defaults as SIMPO reference values, not values extracted
  from the paper. A missing paper pH model, pK table, or Project pH Target
  does not itself prevent preparing BioModel Ionization rows.

## 6. Built-in SIMPO parameter reference

<!-- BEGIN GENERATED IONIZATION -->
<!-- Generated from SimpoHome/data/ionization/ionization.json; version 1; sha256 b95db023316a3dfb1afdc52204bc2a2a0fab1834e4f8c9e6042edc00091a2478. Do not edit this block. -->

SIMPO built-in parameter set v1. [Documentation](https://www.simpowater.com/zh/docs/Tutorials/BioModel/Edit#4-ionization). Default pKw: **14**.

These are approved SIMPO reference defaults for derivation, not dummy examples. The primary values outside parentheses in the source table are selected; do not average or substitute the parenthetical alternatives. Use these local values without a live webpage lookup.

| Species | Compound | Step | Ionization | Factor (mol/mg) | pK1 | pK2 | pK3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Borate / 硼酸盐 | Weak Acid | Mono | One Step | 1/10800 | 9.24 |  |  |
| Nitrite / 亚硝酸盐 | Weak Acid | Mono | One Step | 1/14000 | 3.15 |  |  |
| Arsenite / 亚砷酸盐 | Weak Acid | Mono | One Step | 1/75000 | 9.29 |  |  |
| Formate / 甲酸盐 | Weak Acid | Mono | One Step | 1/16000 | 3.74 |  |  |
| Acetate / 乙酸盐 | Weak Acid | Mono | One Step | 1/64000 | 4.76 |  |  |
| Propionate / 丙酸盐 | Weak Acid | Mono | One Step | 1/112000 | 4.87 |  |  |
| Butyrate / 丁酸盐 | Weak Acid | Mono | One Step | 1/160000 | 4.82 |  |  |
| Valerate / 戊酸盐 | Weak Acid | Mono | One Step | 1/208000 | 4.84 |  |  |
| Hexanoate / 己酸盐 | Weak Acid | Mono | One Step | 1/256000 | 4.86 |  |  |
| Lactate / 乳酸盐 | Weak Acid | Mono | One Step | 1/96000 | 3.86 |  |  |
| Carbonate / 碳酸盐 | Weak Acid | Di | Stepwise | 1/12000 | 6.35 | 10.33 |  |
| Sulfide / 硫化物 | Weak Acid | Di | Stepwise | 1/32000 | 7.02 | 13.9 |  |
| Silicate / 硅酸盐 | Weak Acid | Di | Stepwise | 1/28000 | 9.84 | 13.2 |  |
| Sulfite / 亚硫酸盐 | Weak Acid | Di | Stepwise | 1/32000 | 1.86 | 7.19 |  |
| Thiosulfate / 硫代硫酸盐 | Weak Acid | Di | Stepwise | 1/64000 | 0.6 | 1.6 |  |
| Oxalate / 草酸盐 | Weak Acid | Di | Stepwise | 1/16000 | 1.25 | 4.72 |  |
| Phosphate / 磷酸盐 | Weak Acid | Tri | Stepwise | 1/31000 | 2.15 | 7.2 | 12.38 |
| Arsenate / 砷酸盐 | Weak Acid | Tri | Stepwise | 1/75000 | 2.24 | 6.96 | 11.5 |
| Ammonium / 铵盐 | Weak Base | Mono | One Step | 1/14000 | 4.76 |  |  |
| Nitrate / 硝酸盐 | Strong Acid | Mono | Complete | 1/14000 |  |  |  |
| Chloride / 氯化物 | Strong Acid | Mono | Complete | 1/35500 |  |  |  |
| Sulfate / 硫酸盐 | Strong Acid | Di | Complete | 1/32000 |  |  |  |
| Magnesium / 镁盐 | Strong Base | Di | Complete | 1/24000 |  |  |  |
| Calcium / 钙盐 | Strong Base | Di | Complete | 1/40000 |  |  |  |
<!-- END GENERATED IONIZATION -->

## 7. Review and downstream setup

Show the proposed Ionization rows, Factor derivations, pK/pKw sources,
available temperature information, and material assumptions before submission.
Identify built-in values by SIMPO parameter-set version; do not call them
paper-extracted or freshly verified external data.

Ionization defines SIMPO's RIIC/pH relationship but is not sufficient by itself
to expose pH in a Project. Define `pH` as a DataSet Target and map it in Project
Conversion (normally with coefficient `1`). Rate formulas may reference `pH`
directly; do not create a `pH` Component.

Validate the complete BioModel with the current SIMPO parser. Parser acceptance
checks representation and syntax only; it does not prove that the selected
species, constants, or concentration bases are scientifically appropriate.
