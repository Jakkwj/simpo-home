# DataSet and Project Commands

Inspect `simpo --help` and the selected command's `--help` before use. These
operations require a Token with the indicated scope.

If `get-datasets` or `get-projects` is absent from the installed help, do not
fall back to direct API requests. Update SimpoCLI first; the references describe
the newer command surface without pretending it exists in every package.

## DataSets

| Task | Command | Scope |
| --- | --- | --- |
| List owned DataSet metadata | `get-datasets` | `read` |
| Read complete DataSet tables | `get-dataset DATASET_ID` | `read` |

List results are paginated. Traverse all pages when resolving a DataSet by name.
Use the positive database ID with `get-dataset`; report the identity metadata
and only the tables relevant to the user's request.

## Projects

| Task | Command | Scope |
| --- | --- | --- |
| List owned Project metadata | `get-projects` | `read` |
| Read all Solution Variable fields | `get-project-variables PROJECT_ID` | `read` |
| Update one Variable field | `set-project-variable PROJECT_ID VARIABLE VALUE` | `write` |

Use `get-projects` and traverse pagination to resolve the Project. Before a
write, run `get-project-variables` and select the row using both the exact
Variable name and `--tank` when the row is tank-specific.

## Update a Variable safely

Only an owned version 0 Draft Project is writable. Read the installed command
help for the allowed `--field` values and value syntax. Common examples include
numeric `Value`, `LowerBound`, or `UpperBound`; Boolean `Evaluation`; integer
`DecimalPoint`; and nullable metadata fields. `Variable` and `Tank` identify a
row and are not writable fields.

Before running the command, show or internally verify:

- Project ID, name, state, and version;
- exact Variable and optional Tank;
- target field, current value, and proposed value;
- bounds or type restrictions returned by the current Project data.

After success, require `success: true` and verify that the returned Project,
Variable, Tank, field, old value, and new value match the intended update. Read
the row again when the response is incomplete or the outcome is ambiguous.

Do not bulk-edit variables by constructing repeated commands unless the user
explicitly requested every change and each row/value has been validated.
