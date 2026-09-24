# Token and CLI Basics

## Command map

| Task | Command | Scope |
| --- | --- | --- |
| Show version or discover commands | `simpo --version`, `simpo --help` | none |
| Validate and save a Token | `simpo configure` | Token validation must succeed |
| Show current identity and scopes | `simpo me` | authenticated Token |
| Remove the saved local Token | `simpo logout` | none |

Always inspect the installed help. A published or development build may expose
more commands than an older local installation.

## Configure without leaking a Token

Run `simpo configure` in an interactive terminal. It reads the Token through a
hidden prompt, validates it, and saves it in the user profile. Do not pass the
Token through chat, shell history, committed environment files, or generated
scripts.

For normal use, rely on the saved Token. `--api-token` and the
`SIMPO_API_TOKEN` environment variable are temporary override mechanisms and
must not be printed or persisted. `--base-url` is a development override; omit
it unless the user explicitly targets another backend.

Run `simpo me` after configuration and check the returned `scopes` before the
requested operation:

- `read`: list/read BioModels, DataSets, Projects, and Project Variables;
- `write`: create/update/sync/release BioModels and update Project Variables;
- `calculate`: prepare, inspect, and stop calculations.

## Output and automation

Successful results are JSON on stdout. Progress and errors go to stderr. In a
script, capture them independently and parse stdout only after checking the exit
status. Never log a result field documented as secret, including a calculation
`launchProtocol` requested with `--print-protocol`.

List endpoints are paginated. Read `--help` for `--page` and `--page-size`, and
continue until the response indicates that every page has been visited.

`simpo logout` removes only the local Token file. It does not revoke the Token on
the SIMPO server; revoke it from the Dashboard when server-side invalidation is
required.

## Failure handling

- `401`: reconfigure a valid, non-expired Token; never request it in chat.
- `403`: inspect `simpo me` and obtain the missing scope through the Dashboard.
- command missing from `simpo --help`: update SimpoCLI rather than calling the
  OpenAPI directly.
- network or timeout after a write: inspect the affected resource before retrying.
