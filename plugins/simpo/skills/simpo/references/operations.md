# Operation commands

The OpenAPI Operation protocol is opt-in. Ordinary Project and calculation
commands remain synchronous unless an asynchronous option is supplied.

## Resource writes

BioModel and DataSet JSON creation/update, as well as Project creation/update,
support the same durable protocol. Normal calls remain synchronous.

```text
simpo create-biomodel MODEL --json BioModel.json --async --idempotency-key REQUEST_KEY
simpo update-biomodel BIOMODEL_ID --json BioModel.json --async --wait
simpo create-dataset DATASET --json DataSet.json --async --idempotency-key REQUEST_KEY
simpo update-dataset DATASET_ID --json DataSet.json --async --wait
```

`create-biomodel --template` is multipart and remains synchronous; use JSON or
blank creation when a durable Operation is required. With `--async`, the command
returns immediately with `operationId` unless `--wait` is also supplied. The
backend still performs the same parsing, change-value mapping, and dependent
Project synchronization as the synchronous endpoint.

## Project writes

```text
simpo create-project NAME --biomodel-id BIOMODEL_ID --dataset-id DATASET_ID \
  --async --idempotency-key REQUEST_KEY
simpo update-project PROJECT_ID --json Solution.json \
  --async --wait --idempotency-key REQUEST_KEY
```

The first form returns immediately with `operationId` and `status=queued` or
`running`. The second polls and returns the final Project result. A failed
operation is not a successful Project mutation.

## Calculation preparation

```text
simpo calculate PROJECT_ID --engine SIM --async-preparation --no-launch
simpo wait-operation OPERATION_ID
```

When a local client should be launched automatically, use
`--async-preparation --wait-preparation`; the CLI waits for the nested
`result.launchProtocol` before starting SimpoClient. This preparation wait is
distinct from `calculate --wait`, which waits for the later calculation status.

## Inspect, wait, and cancel

```text
simpo get-operation OPERATION_ID
simpo wait-operation OPERATION_ID --wait-timeout 86400
simpo stop-operation OPERATION_ID
```

Terminal statuses are `succeeded`, `failed`, and `cancelled`. On failure, always
report `errorCode` and `errorMessage`; these fields contain the backend reason
needed to correct the input. Only a queued operation can be cancelled. Running
calculations should be stopped with `stop-calculation`.
