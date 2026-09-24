---
name: simpo
description: Operate SIMPO through the installed SimpoCLI safely and efficiently. Use when asked to install or configure SimpoCLI, inspect the current SIMPO identity or scopes, create/read/update/sync/release BioModels, list/read DataSets, list Projects, read or change Project Variables, start/monitor/stop calculations, troubleshoot a simpo command, or generate a script that consumes SimpoCLI JSON output.
---

# SimpoCLI

Treat the installed CLI as the source of truth. Use this Skill as task routing and
safety guidance, then read only the reference for the requested command group.

## Establish the installed interface

1. Run `simpo --version` and `simpo --help` before planning commands.
2. Run `simpo COMMAND --help` before invoking each command. Options and commands
   can differ between installed releases.
3. If a command described by a reference is absent from `simpo --help`, do not
   attempt it or emulate it with direct HTTP requests; explain that the
   installed SimpoCLI must be updated.
4. Use `simpo me` to verify the selected Token and its scopes before an API
   operation. Never ask the user to paste a Token into chat or place one in a
   command, script, generated file, or log. Direct the user to `simpo configure`
   for interactive hidden input when configuration is needed.

## Route the task

- For installation, Token configuration, identity, scope, logout, output, or
  authentication problems, read [Token and CLI basics](references/token-and-cli.md).
- For any BioModel create/get/update/sync/release task, read
  [BioModel commands](references/biomodel.md).
- For DataSet reads or Project/Variable operations, read
  [DataSet and Project commands](references/dataset-and-project.md).
- For calculation preparation, engine selection, status polling, or stopping,
  read [Calculation commands](references/calculation.md).

Read only the relevant references. Do not load the complete command manual for a
single operation.

## Execute and verify

1. Resolve names to IDs with list commands when necessary. Traverse pagination
   until the target is found; never assume page 1 is complete.
2. Confirm exact IDs, names, states, versions, and files before a write. Explain
   material effects before running a command, especially Project synchronization
   during BioModel updates, releases, public visibility, calculation starts, and
   calculation stops.
3. Do not perform a write merely because the user asked how a command works.
   Execute it only when the user requested the state change. Require explicit
   direction before creating a Public Release.
4. Run the command without exposing credentials. Keep stdout available for JSON
   parsing; SimpoCLI writes progress and errors to stderr.
5. Parse the JSON response and verify task-specific success fields. Do not equate
   a zero exit code for calculation launch with calculation completion.
6. On an ambiguous timeout or connection loss after a write, inspect current
   server state before retrying. Do not blindly repeat create, release, start, or
   stop operations.

## Report results

Report the command used with secrets omitted, the relevant object IDs and final
state, and any remaining uncertainty. Relay concise SIMPO domain errors without
dumping unrelated environment data. When asked for scripting help, use the
documented JSON on stdout and preserve stderr separately.
