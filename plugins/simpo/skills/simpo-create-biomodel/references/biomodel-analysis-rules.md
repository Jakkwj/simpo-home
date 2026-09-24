# BioModel Analysis Rules

Use this reference when turning a wastewater-treatment model paper into SIMPO
tables. It preserves the domain requirements used by the backend AI prompt,
adapted for an assistant analysis followed by the SimpoCLI JSON interface.

## Paper eligibility

- Confirm that the source is a research paper about a wastewater-treatment
  model, not merely a general treatment paper.
- Search a reliable bibliographic source for the paper's DOI when network access
  is available. If no DOI can be verified, report `Not SCI` and stop unless the
  user explicitly overrides this eligibility check. If network access is not
  available, state that DOI eligibility remains unverified rather than guessing.
- Never let a missing DOI or a failed search turn into an invented citation.

## Evidence and reporting

- Prefer the paper's Components, Parameters, process, and stoichiometric tables.
  Also inspect equations, appendices, and supplements when tables are missing or
  incomplete.
- Do not invent model content. For every correction or derived value, cite the
  source page/table/equation and explain the derivation or correction.
- Return a concise, evidence-based Markdown audit note, not private chain of
  thought. Record extraction choices, corrections, assumptions, and unresolved
  items. Use English for an English paper and Chinese for a Chinese paper.
- This workflow avoids the SIMPO backend AI endpoint, but it does not imply that
  paper contents stay on-device. Follow the data-handling policy of the model
  configured for the user's assistant session.
- Keep the paper title and DOI/citation in this note. A paper DOI is not a
  SIMPO `sourcepaperId`; only pass `--sourcepaper-id` when the user knows the
  database ID.

## Source correction

`source_correction` is a per-run Skill option and defaults to `on`. It is an
evidence-preserving transcription check, not permission to rewrite a paper's
scientific conclusions.

- With `on`, automatically apply only high-confidence corrections supported by
  a direct cross-check: an OCR character error, an obvious copied digit, a
  decimal separator error, a unit-label mismatch confirmed by the same table or
  equation, or a value that is unambiguously contradicted by the paper's own
  adjacent definition. Use the corrected value in the model.
- Do not correct a fitted parameter, empirical coefficient, stoichiometric
  choice, or scientific conclusion merely because it looks unusual, conflicts
  with an external expectation, or improves `Balance`. If evidence conflicts,
  retain the source value and report the conflict as unresolved.
- With `off`, preserve the source representation exactly. Report suspected
  errors, but do not change the extracted value or formula.
- Every applied correction must be written in Markdown in the `--description`
  audit note, including the source location, original value, corrected value,
  evidence, and confidence. Use this compact format:

  ```markdown
  ## Source corrections
  - Status: applied
  - Location: p. 7, Table 2, `S_NO3` coefficient
    - Original: `0.57`
    - Corrected: `8/14`
    - Evidence: Equation (4) defines a nitrogen-mass basis; the same coefficient is `8/14` in the supplementary table.
    - Confidence: high
  ```

- If no correction is applied, record `## Source corrections` with
  `- Status: none` (or `not applied` when the option is off) and briefly list
  any unresolved suspicion. This keeps the BioModel's provenance auditable.

## Components

Use this exact header row:

```json
{"0":"Symbol","1":"Unit","2":"Name","3":"Description"}
```

- Use the paper's component set. Use `S_` for dissolved components and `X_` for
  particulate components. Place dissolved components before particulate ones.
- If dissolved oxygen is in the model, put `S_O2` or the paper's `S_O` first.
  Preserve the paper's convention; do not add dissolved oxygen when absent.
- Keep oxidation/reduction order meaningful; place nitrate (`S_NO3`) before
  nitrite (`S_NO2`) when both occur. Use a consistent order for remaining
  components and do not duplicate symbols.
- Symbols contain only ASCII letters, digits, and underscores. Do not include
  charge signs, parentheses, hyphens, spaces, or Greek characters. Approximate
  Greek letters with Latin names where appropriate (for example, `u` for
  `mu`).
- Use the paper's unit without spaces. Use `-` for dimensionless values. Use
  `UNKNOWN` only when the paper does not make the unit recoverable, and disclose
  it in the audit note.
- Names and descriptions may be null when absent. Do not fabricate a name or
  description.
- If a symbol truly cannot be recovered, use sequential `S_UNKNOWN_1` or
  `X_UNKNOWN_1` placeholders only after telling the user. Never silently turn an
  uncertain symbol into a factual claim.

## Parameters

Use this exact header row:

```json
{"0":"Symbol","1":"Unit","2":"DefaultValue","3":"LowerBound","4":"UpperBound","5":"Name","6":"Description"}
```

- Parameter symbols start with an ASCII letter and contain only ASCII letters,
  digits, and underscores. Keep them unique and preserve capitalization.
- Use the value reported by the paper for `DefaultValue` when available. A
  missing lower or upper bound may be null. Do not infer bounds without an
  explicit derivation.
- For time-based units, follow the source prompt's `/d`, `/h`, `/m`, `/s`
  suffix convention. Do not insert spaces. Use `-` for a dimensionless unit.
- If a unit or value cannot be recovered, do not hide that fact. The legacy
  extraction prompt permits `UNKNOWN` for an unknown unit and `-10000` for an
  unknown default; use such sentinels only when necessary, flag each occurrence,
  and obtain user approval before submitting.
- Use sequential `Para_UNKNOWN_1` placeholders only when unavoidable and only
  after disclosing them.

## Stoichiometric Matrix

The header's first cell is `Name`, followed by exactly one column per Component
in the same order, followed by `Rate`:

```json
{"0":"Name","1":"S_O2","2":"S_NO3","3":"X_B","4":"Rate"}
```

- Use a unique process name in the first cell of every data row. Prefer the
  paper's process names; if absent, use `Process1`, `Process2`, and so on and
  disclose the fallback.
- Stoichiometric coefficient cells may be null when the process has no
  coefficient for that Component. Otherwise use formulas containing only
  declared Parameter symbols, numeric literals, and `. + - * / ( )` operators.
  Do not place Component symbols in these cells. Make multiplication explicit
  with `*` and preserve symbol capitalization.
- `Rate` formulas may use declared Component and Parameter symbols, numeric
  literals, and `. + - * / ( )` operators. Do not invent identifiers. If a
  rate cannot be recovered, use `-10000` only as an explicitly disclosed
  placeholder and require user approval.
- Convert stoichiometric decimals to simple exact fractions when the paper's
  convention supports it. Common nitrogen-basis conversions include `0.57` to
  `8/14`, `1.71` to `24/14`, `2.29` to `32/14`, `3.43` to `48/14`, `4.57` to
  `64/14`, and `6.85` to `96/14`. Do not replace `1` with `14/14`.
- Apply the per-run `matrix_fractions` option. When enabled, normalize a rounded
  coefficient in Matrix or Composition only if its exact value follows from a
  cited equation, molecular/elemental basis, or transparent derivation. For
  example, the Xu et al. (2016) AD equations and biomass formula support
  `1.239 -> 140/113`, `0.826 -> 280/339`, `2.832 -> 320/113`, and
  `0.944 -> 320/339`; preserve the paper's rounded values in the audit note and
  identify the derivation for the stored fractions. Never infer a rational
  value from a decimal alone (including with a bounded-denominator
  approximation), and never convert fitted estimates or empirical coefficients
  without an independent exact derivation. When the option is off, preserve the
  source notation.

## Composition

`Composition` contains balance coefficients; it is distinct from the
read-only `Balance` result. If the paper omits it and derivation is requested or
useful, read `references/composition-derivation.md` and follow that workflow in
full. Derive and submit supported cells independently; do not require the table
to be balanced before creation.
When included:

- Use the exact first header value `Balances \\ Components` (one literal
  backslash, escaped as `\\` in JSON), then one column per Component in the
  same order as the Matrix:

  ```json
  {"0":"Balances \\ Components","1":"S_O2","2":"S_NO3"}
  ```
- Include balance rows in this order: `ThOD`, `N`, `P`, `S`, `Charge`, `TSS`.
  Keep all six rows in this order when providing a Composition table; use
  `null` only when a coefficient is genuinely unavailable. A defensible zero is
  different from an unknown `null`.
- Composition cells contain only declared Parameter symbols, numeric literals,
  and `. + - * / ( )` operators. Do not use Component symbols inside formulas.
- Derive coefficients from the paper or explicit elemental, charge, oxygen
  demand, or solids balances. Cite the source or derivation. Do not present a
  guessed balance as extracted fact.
- Treat an absent Composition as missing information, not permission to insert
  generic ASM coefficients. Establish the reporting basis, formula/speciation,
  charge, and solids basis separately for each supported cell. Leave unsupported
  cells `null` and explain them in the audit note. Omit the whole table only when
  no cell has defensible evidence.
- Do not remove a supported Component or coefficient because it makes
  `Balance` nonzero. `Balance` is a backend diagnostic that can expose an
  omitted Component, an unknown coefficient, a basis mismatch, or a genuinely
  non-closed paper model. Do not fit coefficients, add unreported Components, or
  alter the Matrix solely to force zero residuals.
- Examples of SIMPO reference checks include ThOD coefficients
  for `S_NO3=-64/14`, `S_NO2=-48/14`, `S_NO=-40/14`, `S_N2O=-32/14`,
  `S_N2=-24/14`, `S_NH2OH=-16/14`, `S_SO4=-2`, `S_CH4=1`, and `S_O2=-1`;
  nitrogen or phosphorus content parameters must be referenced by their exact
  declared Parameter symbols. These are checks, not values to add when the
  model does not contain those Components.

## Ionization

`Ionization` defines the acid/base contribution of dissolved Components to
SIMPO's RIIC/pH calculation. Omit it when the paper and defensible chemical
references do not establish the species, concentration basis, equilibrium
constants, and temperature assumptions. If Ionization is requested or useful,
read `references/ionization-derivation.md` and follow it in full.

- Use the exact header `Symbol`, `Compound`, `Step`, `Ionization`, `Factor`,
  `pK1`, `pK2`, `pK3`, `pKw` in that order.
- Include only unique dissolved `S_` Component symbols, matching the frontend
  workflow.
- Derive `Factor` from the Component's actual reporting basis; for example,
  NO3-N uses the molar mass of N, not the full nitrate ion.
- Treat all selected pK values, conversions, temperature assumptions, and
  external references as auditable model decisions. Do not guess them.
- Put pKw only in the first data row and keep unused pK fields null.
- Do not add `pH` to Component. A Project needs a DataSet `pH` Target and a
  Project Conversion mapping to expose pH results.

## JSON submission shape

Submit model tables only. Do not include the paper title, `Description`, or
`Balance` as root keys in the `--json` file. Put citation and concise analysis
notes in `simpo create-biomodel --description`.

```json
{
  "Component": [
    {"0":"Symbol","1":"Unit","2":"Name","3":"Description"},
    {"0":"S_O2","1":"gO2/m3","2":"Dissolved oxygen","3":null}
  ],
  "Parameter": [
    {"0":"Symbol","1":"Unit","2":"DefaultValue","3":"LowerBound","4":"UpperBound","5":"Name","6":"Description"},
    {"0":"k","1":"/d","2":0.1,"3":0,"4":1,"5":"Rate coefficient","6":null}
  ],
  "Matrix": [
    {"0":"Name","1":"S_O2","2":"Rate"},
    {"0":"Removal","1":"-1","2":"k*S_O2"}
  ],
  "Composition": [],
  "Ionization": []
}
```

`Component`, `Parameter`, and `Matrix` are required. `Composition` and
`Ionization` are optional. Do not create an `Ionization` table from guesswork;
use the dedicated derivation workflow and omit the table when evidence is
insufficient. Never include `Balance`, even
when reusing a `simpo get-biomodel` response: the API rejects it and computes
the result itself.
