# Token and CLI Basics

## Command map

| Task | Command | Scope |
| --- | --- | --- |
| Show version or discover commands | `simpo --version`, `simpo --help` | none |
| Validate and save a Token | `simpo configure` | Token validation must succeed |
| Show current identity and scopes | `simpo me` | authenticated Token |
| Remove the saved local Token | `simpo logout` | none |

Run the requested command directly. A published or development build may expose
different commands than an older local installation; let the CLI report an
unsupported command or option instead of performing routine discovery first.

## Configure without leaking a Token

Run `simpo configure` in an interactive terminal. It reads the Token through a
hidden prompt, validates it, and saves it in the user profile. Do not pass the
Token through chat, shell history, committed environment files, or generated
scripts.

For normal use, rely on the saved Token. `--api-token` and the
`SIMPO_API_TOKEN` environment variable are temporary override mechanisms and
must not be printed or persisted. `--base-url` is a development override; omit
it unless the user explicitly targets another backend.

Use `simpo me` when the user explicitly asks for identity/scopes or when
diagnosing an authentication problem. Normal operations should be attempted
directly; the CLI and backend enforce the required scopes:

- `read`: list/read BioModels, DataSets, Projects, and Project Variables;
- `write`: create/update/sync/release BioModels and update Project Variables;
- `calculate`: prepare, inspect, and stop calculations.

## Output and automation

Successful results are JSON on stdout. Progress and errors go to stderr. In a
script, capture them independently and parse stdout only after checking the exit
status. Never log a result field documented as secret, including a calculation
`launchProtocol` requested with `--print-protocol`.

List endpoints are paginated. Use the pagination fields returned by the command
and continue until every page has been visited. Consult `--help` only when the
pagination syntax is unclear or the command reports a usage error.

`simpo logout` removes only the local Token file. It does not revoke the Token on
the SIMPO server; revoke it from the Dashboard when server-side invalidation is
required.

## Failure handling

- `401`: reconfigure a valid, non-expired Token; never request it in chat.
- `403`: relay the backend scope/permission error; use `simpo me` only when
  diagnosing the authentication or scope problem, then obtain the missing
  scope through the Dashboard.
- unknown command or unsupported option: consult the relevant `--help` and
  update SimpoCLI if the operation is not available; never call the OpenAPI
  directly to bypass the CLI.
- network or timeout after a write: inspect the affected resource before retrying.
