# Composition Derivation Workflow

## On-demand options

Use the per-run options in `SKILL.md`. In brief, `matrix_fractions` changes the
stored numeric expression, while `composition_derive` decides whether missing
Composition cells may be derived; these are independent choices. Preserve
paper-reported cells even when derivation is off. For each Composition
coefficient, preserve a reported value unless its exact replacement follows
from an independent equation or unit-basis derivation. Never approximate a
fraction from a decimal alone.

Use this workflow only when a paper does not provide a SIMPO Composition table
and the user requests a derivation, or when the source evidence is sufficient to
derive it without inventing model facts. Composition is a vector of conserved
or accounting properties for every Component. It is not the backend's read-only
`Balance` output.

## 1. Establish the basis before calculating

Create an evidence table for every Component with:

- SIMPO symbol and dissolved/particulate state;
- reported concentration basis, such as gCOD, gN, gP, gS, g compound, mol, or
  gTSS;
- chemical or empirical formula and protonation/ionic form at the modeled pH;
- molar mass on the chosen basis;
- net charge;
- whether the Component is measured as TSS/VSS or as a dissolved quantity;
- source page, table, equation, supplement, or clearly labeled external domain
  convention.

Normalize all coefficients to "amount of balance property per unit of that
Component's modeled concentration." Do not mix, for example, gN/gN with
gN/gNO3, or gS/gS with gS/gSO4. A generic unit such as `mg/l` is insufficient
by itself; recover the chemical reporting basis from the definition or methods.

Do not discard the entire Composition just because one Component or one property
has an unknown basis. Work cell by cell. Fill every cell for which the paper,
an explicitly cited chemical reference, or a transparent derivation supplies a
defensible value, including a defensible zero. Leave a cell `null` when its
value cannot be established without guessing, and record the missing basis in
the audit note. A `null` cell is not evidence that the real coefficient is zero:
the current SIMPO parser normalizes empty Composition cells to zero while
calculating `Balance`, so the resulting residual must be interpreted as a
diagnostic under the known-coefficients-only assumption.

## 2. Derive each row independently

Keep the exact row order `ThOD`, `N`, `P`, `S`, `Charge`, `TSS`.

### Element rows: N, P, and S

For a Component reported as mass of the complete compound, compute the element
coefficient as:

```text
(number of target-element atoms * target-element atomic mass)
/ component molar mass
```

If its concentration is already reported as the target element (for example,
NO3-N or SO4-S), the corresponding coefficient is `1`, not the elemental mass
fraction of the full ion. Use `0` only when the formula proves the element is
absent. Use a declared model Parameter when the paper represents variable
biomass or substrate content through that Parameter.

### Charge

Use signed mole equivalents of positive charge per mass unit of the modeled
Component:

```text
ionic charge / component basis molar mass
```

For an ion reported on an elemental basis, use the atomic mass associated with
that reporting basis rather than the full ion molar mass. State the modeled
protonation/speciation. Do not derive a fixed charge coefficient when pH-dependent
speciation is material and the model does not specify how to represent it.

### TSS

Set dissolved Components to `0`. For particulate Components, use a reported
TSS/VSS conversion or an explicit parameter. Use `1` only when the Component's
own concentration basis is explicitly TSS (or the model explicitly defines one
unit of the Component as one unit of TSS). Do not assume all `X_` Components have
a TSS coefficient of `1`.

### ThOD

Prefer an explicit COD/ThOD definition from the paper or its adopted model. If
the Component is already expressed as COD, its coefficient is normally `1`
subject to the paper's convention. Otherwise derive electron equivalents only
after defining the common terminal/reference states for C, H, O, N, P, and S,
the nitrogen convention (for example NH3, N2, or NO3), sulfur convention (for
example sulphide or sulphate), ionic/protonation state, and sign convention.

For a verified half-reaction transferring `n_e` electrons per mole of
Component, the oxygen-equivalent magnitude is:

```text
n_e * 8 / component basis molar mass
```

Apply the documented SIMPO sign convention consistently. Do not combine values
from references that use different terminal states. The backend-prompt values
such as `S_NO3=-64/14`, `S_NO2=-48/14`, `S_SO4=-2`, and `S_O2=-1` are convention
checks, not universal facts to copy into every model. If the reference state or
reporting basis cannot be established, leave ThOD unsupported and disclose it.

## 3. Use stoichiometric conservation as a diagnostic

For stoichiometric matrix `N` with processes as rows and Components as columns,
every supported Composition row vector `c` should satisfy:

```text
N * c^T = 0
```

Use exact rational or symbolic arithmetic. Substitute neither fitted default
parameter values nor rounded decimals when a symbolic formula can be retained.
Do not make a Composition row, Component, or Matrix coefficient fit the
stoichiometry merely to remove a residual.

Apply this equation in three ways:

1. Validate coefficients derived independently from formulas and reporting
   bases.
2. Identify a conflict or an omitted balance contribution in Composition,
   stoichiometry, component basis, or the paper itself.
3. If a missing coefficient can also be derived independently from a documented
   formula or reporting basis, show that derivation separately; never infer it
   solely from `N * c^T = 0`.

Do not choose an arbitrary null-space vector, normalize a free variable without
a physical definition, or change a coefficient merely to make the residual
zero. A homogeneous equation always permits the all-zero vector; that is not a
scientific derivation. If the system is underdetermined, report its degrees of
freedom and the missing physical assumptions. If it is inconsistent, preserve
the evidence and ask for review instead of silently changing Matrix, Component,
or Composition values.

## 4. Represent evidence and uncertainty

For each nonzero or parameterized cell, record:

- the formula or balance used;
- the concentration and terminal-state bases;
- the source or explicit derivation;
- whether it is extracted, derived, or dependent on an assumption.

Use `null` for a genuinely unavailable coefficient, not for a guessed zero.
SIMPO currently normalizes empty Composition cells to zero during balance
calculation. Therefore it is valid to submit a partially evidenced table, but
the description must say which cells are unknown and that their diagnostic
contribution is currently treated as zero. Include the canonical rows in order
(`ThOD`, `N`, `P`, `S`, `Charge`, `TSS`) when a Composition table is submitted;
unsupported cells may be `null`. If no Composition cell has any defensible
evidence, omit the entire table rather than submitting an empty claim.

Never describe a derived value as if the paper reported it. Material assumptions
require user approval before creating the BioModel. A nonzero `Balance` is an
important review result, not by itself a reason to omit the supported cells or
to reject creation.

## 5. Validate with SIMPO

Build the exact header and Component order required by the main analysis rules.
Check formula identifiers and parse the full BioModel locally when possible.
Then inspect the backend-derived `Balance` after creation or update:

- `Balance = null` means the supplied rows are symbolically balanced under the
  parser's calculation; it does not prove the chemistry or chosen bases are
  scientifically correct.
- A nonzero `Balance` identifies process/row residuals under the submitted
  coefficients, with unknown cells effectively contributing zero. Report the
  affected process and row, then recheck source formulas, units, component
  bases, speciation, sign conventions, and whether a Component or coefficient is
  missing from the paper extraction. Do not suppress the result by submitting
  `Balance`, fitting arbitrary Composition values, adding an unreported
  Component, or changing the Matrix without evidence.

Include the derivation audit and unresolved limitations in the BioModel
description, and keep the new model Private, Draft, and version 0.
