# Model Targets and Influent Fractionation

Use a target set compatible with the BioModel that will later be used in a
Project. `simpo create-dataset` creates only the DataSet; it does not link or
clone a BioModel. Record the recommended model family in the review and
description.

## Contents

1. Selection rule
2. Target row format
3. ASM2D target set
4. ASM3 target set
5. Influent fractionation

## 1. Selection rule

- Prefer **ASM2D** when biological phosphorus removal, phosphate, PAO storage,
  or metal-phosphate precipitation is material.
- Prefer **ASM3** for carbon and nitrogen treatment without material phosphorus
  modeling.
- Honor a user-selected compatible BioModel. When it uses different component
  symbols, derive the Target rows from that model rather than silently mixing
  standard ASM symbols.

## 2. Target row format

Use the current header:

```json
{"0":"Symbol","1":"Unit","2":"Name","3":"Description","4":"Oxygen","5":"TSS"}
```

Exactly one dissolved-oxygen target should have `Oxygen: true`, normally
`S_O2`. Exactly one total-suspended-solids target should have `TSS: true`,
normally `X_TSS`. All other marker values are `false`.

## 3. ASM2D target set

Use the BioModel's exact symbols when available. A standard ASM2D-compatible
set is:

| Symbol | Unit | Meaning |
| --- | --- | --- |
| `S_O2` | `gO2/m3` | Dissolved oxygen |
| `S_F` | `gCOD/m3` | Fermentable readily biodegradable substrate |
| `S_VFA` | `gCOD/m3` | Volatile fatty acids / fermentation products |
| `S_U` | `gCOD/m3` | Soluble unbiodegradable organics |
| `S_NHx` | `gN/m3` | Ammonium plus ammonia nitrogen |
| `S_NOx` | `gN/m3` | Nitrate plus nitrite nitrogen |
| `S_N2` | `gN/m3` | Dissolved nitrogen gas |
| `S_PO4` | `gP/m3` | Soluble inorganic phosphorus |
| `S_Alk` | `molHCO3-/m3` | Alkalinity |
| `X_U_E` | `gCOD/m3` | Particulate unbiodegradable organics |
| `X_B` | `gCOD/m3` | Slowly biodegradable substrate |
| `X_OHO` | `gCOD/m3` | Ordinary heterotrophic organisms |
| `X_PAO` | `gCOD/m3` | Phosphate-accumulating organisms |
| `X_PAO_PP` | `gP/m3` | PAO polyphosphate |
| `X_PAO_PHA` | `gCOD/m3` | PAO storage product |
| `X_ANO` | `gCOD/m3` | Autotrophic nitrifying organisms |
| `X_MeOH` | `gMeOH/m3` | Metal hydroxide precipitate |
| `X_MeP` | `gMeP/m3` | Metal phosphate compound |
| `X_TSS` | `gTSS/m3` | Total suspended solids |

## 4. ASM3 target set

| Symbol | Unit | Meaning |
| --- | --- | --- |
| `S_O2` | `gO2/m3` | Dissolved oxygen |
| `S_F` | `gCOD/m3` | Readily biodegradable substrate |
| `S_U` | `gCOD/m3` | Soluble unbiodegradable organics |
| `S_NHx` | `gN/m3` | Ammonium plus ammonia nitrogen |
| `S_NOx` | `gN/m3` | Nitrate plus nitrite nitrogen |
| `S_N2` | `gN/m3` | Dissolved nitrogen gas |
| `S_Alk` | `molHCO3-/m3` | Alkalinity |
| `X_U_E` | `gCOD/m3` | Particulate unbiodegradable organics |
| `X_B` | `gCOD/m3` | Slowly biodegradable substrate |
| `X_OHO` | `gCOD/m3` | Ordinary heterotrophic organisms |
| `X_OHO_Stor` | `gCOD/m3` | Heterotrophic storage product |
| `X_ANO` | `gCOD/m3` | Autotrophic nitrifying organisms |
| `X_TSS` | `gTSS/m3` | Total suspended solids |

## 5. Influent fractionation

Do not invent a unique fractionation from aggregate COD, nitrogen, phosphorus,
and solids values: the system is normally underdetermined. Use measurements,
the selected model's characterization procedure, a cited source, or explicitly
reviewed assumptions.

For an ASM2D-style check, common aggregate relationships are:

```text
COD = S_F + S_VFA + S_U + X_U_E + X_B
TN  = S_NHx + S_NOx
      + i_N_S_U*S_U + i_N_S_F*S_F
      + i_N_X_U_E*X_U_E + i_N_X_B*X_B
TP  = S_PO4
      + i_P_S_U*S_U + i_P_S_F*S_F
      + i_P_X_U_E*X_U_E + i_P_X_B*X_B
TSS = i_TSS_X_U_E*X_U_E + i_TSS_X_B*X_B + i_TSS_OHO*X_OHO
```

Reference coefficients sometimes used for preliminary checks include
`i_N_S_U=0.01`, `i_N_S_F=0.03`, `i_N_X_U_E=0.02`, `i_N_X_B=0.04`,
`i_P_S_U=0`, `i_P_S_F=0.01`, `i_P_X_U_E=0.01`, `i_P_X_B=0.01`,
`i_TSS_X_U_E=0.75`, `i_TSS_X_B=0.75`, and `i_TSS_OHO=0.9` in their
corresponding mass bases. Treat these as model/reference assumptions unless the
chosen BioModel or source explicitly defines them.

Show the aggregate reconstruction residuals for COD, TN, TP, and TSS. If the
supplied measurements cannot be reconciled, retain the discrepancy and request
review; do not force closure by changing an independently measured value.
