# Agent experience

## Shared workflows

We use ordinary prompts in either client:

- `ff finish this feature`: complete relevant first-run, empty, loading, failure and accessibility states.
- `ff review-plan`: assess the plan against the repository without implementing it.
- `ff polish this message`: improve clarity and voice without sending it.
- `ff doctor`: inspect the local setup without changing it.

These routes belong to the existing Funfigs skill. They are not new slash commands or separate plugins. Both clients read the same linked files. We use a fresh session when an existing session has already loaded an older copy.

## Local activation

We preview and activate the optional client settings separately from the shared-skill installer:

```sh
uv run --offline --no-project scripts/client_setup.py check
uv run --offline --no-project scripts/client_setup.py install
uv run --offline --no-project scripts/doctor.py
```

The installer preserves existing environment values, permission settings, models and custom status lines. It stores backups outside Git in `~/.local/state/funfigs/backups/`. We restore a specific backed-up file only after reviewing newer local changes. Both scripts need Python 3.11 or newer, available through uv. Activation requires an existing uv runtime; offline mode never downloads a dependency in a status-line refresh.

We apply the defaults in `agent-env.json` to Claude's local environment and Codex's shell environment policy. These quiet progress and update notices and make Git fail instead of waiting for terminal credentials. We authenticate separately when needed. We do not set `CI`, `NO_COLOR`, automatic package-install consent or permission-bypass flags. Codex filters or higher-priority settings can override these defaults; existing sessions may need restarting.

## Context display

Claude's terminal status line shows the model, context occupancy and estimated session cost when supplied by the client. Green means below 50% used, amber means 50% to below 80%, and red means 80% or more. Text labels remain available without colour. Missing data displays as unavailable, not zero. The bar is not a subscription quota or bill. It does not read transcripts, call APIs or persist session data.

Codex CLI uses its native footer with model, remaining context, directory and branch. We do not install an unsupported custom colour renderer into Codex desktop. Desktop UI and terminal status lines are separate surfaces.

The supported settings are described in [Claude's status-line documentation](https://code.claude.com/docs/en/statusline), [Codex's configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [Codex's sample configuration](https://learn.chatgpt.com/docs/config-file/config-sample).

## Optional local profiles

We copy `profiles.example.json` to `.local/profiles.json` when we need different launch arguments or environment values. We keep company paths and voice examples only in ignored local files. We never store credentials in profiles; credentials remain in the client's existing authenticated setup.

```sh
sh scripts/claude.sh --profile work
sh scripts/codex.sh --profile personal
```

Without `--profile`, both launchers use only the quiet defaults and existing client configuration. Profile arguments are passed as a list without shell evaluation. Native client options follow `--` if they conflict with the launcher's options. We can choose local settings files or native profiles through these argument lists without copying their contents into Funfigs.

Profiles select launch arguments; they do not automatically isolate globally installed skills, switch credentials, disable company plugins or affect an already-running desktop app. Both example profiles are empty until we deliberately configure them. We preserve project choices for runtimes, formatters and containers.
