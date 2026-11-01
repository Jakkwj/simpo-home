# Paper reproduction workflow

Use this reference after extracting the paper evidence and before treating a
Project as a successful reproduction. The objective is to test whether the
published equations, conditions, and observations are sufficient to recreate
the reported model behavior.

## Contents

1. Classify figures
2. Select reproduction targets
3. Separate observations and predictions
4. Handle missing values
5. Configure the calculation loop
6. Diagnose failure to accumulate biomass
7. Judge convergence and identifiability
8. Report the result

## 1. Classify figures

Create a complete figure inventory before digitizing data. Assign every figure
or panel one primary role:

- `calibration`: experimental observations used to fit parameters or states.
- `validation`: independent observations used to test the fitted model.
- `prediction`: a model scenario without paired observations.
- `diagnostic`: residuals, correlations, uncertainty bands, or model-quality evidence.
- `operation`: monitoring or contextual data the authors did not simulate.
- `conceptual`: process diagrams or other non-numeric illustrations.

Do not assume every time series is a calibration target. Use captions, methods,
results, supplementary material, and cited datasets to identify what the authors
actually simulated. Record evidence for every included and excluded figure,
including why a model-only line is not an observation.

## 2. Select reproduction targets

Prefer original machine-readable data, then tables or supplementary sheets, then
digitized experimental points. Keep calibration and validation data separate.
Each target records the figure and panel, role, experiment, quantities, units,
source classification, DataSet mapping, and use in estimation or validation.
Group targets into one DataSet only when they share a documented scenario,
compatible time basis, and topology. Use separate DataSets for different initial
conditions, source studies, calibration/validation roles, or incompatible
experiments. Multiple Tanks are reserved for genuinely parallel or linked
reactors represented by the same scenario.

When a figure compares alternative equations or model variants, keep the
observations in the appropriate DataSet and create separate Projects, or
separate reviewed BioModels when the equations differ. Do not duplicate the
same observation as if it came from multiple experiments.

## 3. Separate observations and predictions

Treat markers or explicitly described measurements as observations. Treat fitted
or simulated lines as model output unless the caption states otherwise. Never use
a digitized published model line as experimental evidence or an estimation target.
A line digitized only for visual comparison retains the classification
`published_model_output`. Figure-derived experimental series retain
`classification: digitized`, calibration details, uncertainty, and
`review_required: true`.

## 4. Handle missing values

A required but unreported value does not automatically stop the workflow. Build
a provisional scenario when a defensible finite value and bounds can be assigned.
For every provisional value record its variable, location, value, unit,
`temporary_estimate` classification, rationale, bounds, calculation stage,
evaluation status, replacement history, and reviewer.

Use zero only when absence is physically supported. Missing values such as
`X_AD` are initial guesses, never paper-reported measurements. If defensible
finite bounds cannot be constructed, conclude `insufficient_data` instead of
creating false precision.

## 5. Configure the calculation loop

Creation and calculation are separate approval gates. Create only reviewed,
Private version 0 Drafts. Run calculations only when reproduction was requested
or the reviewed calculation plan was approved. Never publish, share, release,
or delete resources automatically.

1. Run `SIM` with reported values and provisional guesses. Verify stability,
   units, event timing, mass balance, and output mapping before fitting.
   Select and record one execution mode: `dynamic`, `steady_state`, or
   `steady_state_then_dynamic`. For a dynamic phase, record
   the input interpolation method (`previous` or `linear`); for a steady-state phase, record
   the input averaging method (`previous`, `linear`, or `arithmetic`). Use the
   combined mode only when the reviewed protocol requires steady-state
   initialization before the original dynamic series.
   Before interpreting the run, audit every `Inflow` and `Flow` baseline:
   record the DataSet `time=0` value, the matching Solution `Variable.Value`,
   the selected Inflow Conversion expression and its resolved coefficient, and
   the effective offset. Preserve a BioModel Parameter reference such as
   `i_N_S_U` instead of replacing it with a rounded constant. The
   runtime uses `Variable.Value * coefficient - DataSet first value` for an
   Inflow and `Variable.Value - DataSet first value` for a Flow, adds the offset
   to the full series, clips negative values, and converts Flow to `m3/s`.
   `Measured` is not shifted and must remain the original observation series.
2. Run `LHS` for uncertain states and influential parameters when requested.
   LHS explores uncertainty but does not prove identifiability.
3. Estimate only a small justified set with `GA` or `RFGA`. Each estimated
   Project Variable needs a finite initial value, `Evaluation=true`, and finite
   bounds satisfying lower < initial < upper. Fixed variables remain
   `Evaluation=false`. Use field names returned by the current Project Variable read tool.
4. Use only relevant engine options, following the execution adapter. A timeout
   while waiting for a result does not prove the calculation stopped; query its
   actual state before continuing.
5. Accept estimates only after reviewing completed results and preserving prior
   values. Re-run `SIM` and compare calibration and validation separately.

Do not tune against validation data unless the run is explicitly reclassified as
exploratory. Do not fit many correlated parameters merely to improve an overlay.

## 6. Diagnose failure to accumulate biomass

Before changing kinetics or fitting parameters, inspect the actual bacterial
Components, their tank-specific trajectories, and the execution mode. TSS alone
does not identify viable biomass. Distinguish a low initial seed from a decline
after initialization; report evidence for a mechanism rather than declaring
washout from a low end value alone. Check these three common causes:

1. **Excessive sludge wasting (`Qw`).** Identify the actual waste Connection and
   Flow name; it need not be named Qw. Read the DataSet series and the matching
   `Solution.Variable.Value` baseline to establish the effective flow after
   runtime offsets. Check selected solids inventories, waste and effluent TSS
   mass losses, and the resulting SRT. Excessive wasting can lower SRT until
   biomass cannot accumulate; internal return sludge is not external wasting.
   Propose a supported reduction of Qw when the evidence points to this cause,
   retaining hydraulic balance and documenting the operating assumption.
2. **Insufficient particulate separation in `Point Settling`.** Read the
   effective `SettlingFactor`, outlet/blanket flow split, and effluent TSS.
   The factor directs a fraction of particulates to the blanket; too small a
   value can lose bacteria with the effluent. Its usual sludge-retaining
   reference magnitude is `0.999` to `1`, with a case-specific value reviewed
   against effluent TSS. This is not a hard validation range or evidence to
   overwrite a reported value. Assess effluent and wasting losses together.
3. **Too little initial bacterial seed.** Read each relevant bacterial
   Component/tank row in `Solution.Variable`, specifically the `Value` column.
   Check actual Inflow/Conversion as well: influent usually does not supply
   seed bacteria, so adequate initial biomass must be present in the system.
   If those initial values are too low, propose increasing them to justified
   values with units and source/assumption notes, then rerun an authorized
   calculation and compare trajectories. Do not increase every particulate
   Component, invent universal seed values, or confuse the runtime `Value`
   with the `InitialValue` column used for estimation population injection.

In `dynamic`, the component initial states come from Variable.Value. In
`steady_state_then_dynamic`, the dynamic phase starts from the computed steady
state; raising Value alone does not guarantee a larger dynamic seed. Inspect
the steady-state biomass and actual oxygen supply first. DO Constraint is
disabled during any steady-state phase, even when measured DO is available.

Retention HRT/SRT selects statistical volumes and solids inventories, not
physical separation or growth. Correct its accounting boundary when needed,
but do not claim that enabling SRT restores biomass. If TSS mapping or mass
loss data are unavailable, report that SRT/washout cannot yet be quantified.
Preserve baseline values and results, state the proposed change and expected
effect, and change/recalculate only within the user's authorized scope.

## 7. Judge convergence and identifiability

Check repeated-run stability, bound-hitting, correlations, uncertainty response,
residual structure, and independent validation. Stop expanding the fit when
variables trade off, multiple parameter sets produce similar outputs, estimates
hit bounds, or calibration improves while validation fails. Preserve failed runs.

Record any switch function, clipping rule, event, reset, or undocumented equation
change needed for the published result as an implementation discrepancy. Compare
the literal-paper and corrected scenarios when feasible.

## 8. Report the result

Report target-level RMSE, MAE, normalized error, maximum deviation, timing error,
or qualitative shape mismatch as appropriate. State data provenance and do not
imply digitized data has raw-data precision. Use explicit conclusions:

- `reproduced`
- `partially_reproduced`
- `structurally_nonidentifiable`
- `practically_nonidentifiable`
- `insufficient_equations`
- `insufficient_data`
- `implementation_discrepancy`
- `contradictory_results`
- `numerical_failure`

The final report lists evidence, target selection and exclusions, DataSet and
Project grouping decisions, temporary estimates and bounds, calculation
settings and IDs, accepted and rejected estimates, comparison metrics,
discrepancies, and missing information. The same auditable summary must be
written into each BioModel, DataSet, and Project Description; store reviewed
derivations and decisions, not private conversational chain-of-thought.
