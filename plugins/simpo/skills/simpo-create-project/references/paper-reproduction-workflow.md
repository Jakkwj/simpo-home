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
6. Judge convergence and identifiability
7. Report the result

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
2. Run `LHS` for uncertain states and influential parameters when requested.
   LHS explores uncertainty but does not prove identifiability.
3. Estimate only a small justified set with `GA` or `RFGA`. Each estimated
   Project Variable needs a finite initial value, `Evaluation=true`, and finite
   bounds satisfying lower < initial < upper. Fixed variables remain
   `Evaluation=false`. Use field names returned by `simpo get-project-variables`.
4. Use only relevant engine options. A `--wait` timeout does not stop the client
   or calculation, and `--wait` must not be combined with `--no-launch`.
5. Accept estimates only after reviewing completed results and preserving prior
   values. Re-run `SIM` and compare calibration and validation separately.

Do not tune against validation data unless the run is explicitly reclassified as
exploratory. Do not fit many correlated parameters merely to improve an overlay.

## 6. Judge convergence and identifiability

Check repeated-run stability, bound-hitting, correlations, uncertainty response,
residual structure, and independent validation. Stop expanding the fit when
variables trade off, multiple parameter sets produce similar outputs, estimates
hit bounds, or calibration improves while validation fails. Preserve failed runs.

Record any switch function, clipping rule, event, reset, or undocumented equation
change needed for the published result as an implementation discrepancy. Compare
the literal-paper and corrected scenarios when feasible.

## 7. Report the result

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
