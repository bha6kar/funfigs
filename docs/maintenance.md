# Maintenance

## Shared rules

We edit `shared/AGENTS.md` when changing a shared global preference. Both global instruction files link to it. This file and `funfigs-claude-template.md` are ignored by Git and stay local. Notes live in `memory/`. The shared installer keeps backups under `~/.local/state/funfigs/backups/`; the restore section below describes the legacy copy installer. To refresh the optional local snapshot from the repository root:

```sh
cp shared/AGENTS.md funfigs-claude-template.md
```

We do not commit either global instruction file. A fresh clone needs a locally created `shared/AGENTS.md` before shared installation. The copy installer's `--include-rules` option requires a locally created snapshot.

## Portable settings

We update `settings.json` with deliberate portable choices. We do not copy the entire live settings file: its trust context can describe private repositories and local data locations. The existing notification keys are preserved from our installation; their effect can depend on the Claude client and version.

## Restore

Each installation stores previous versions of changed files under the destination's `backups/funfigs-<UTC timestamp>/` directory. We restore a specific file from the printed backup directory to the matching destination after closing active sessions. A file newly created by installation has no previous version in that backup.

Backups may contain local settings and stay outside this repository.

## Project configuration

We keep build commands, architecture and test instructions in each project's `CLAUDE.md` or `AGENTS.md`. Project permissions and hooks belong in `.claude/settings.json`, with machine-specific overrides in `.claude/settings.local.json`.

We keep company guidance in the existing Maisa engineering plugin, managed separately. This repository maintains only our Funfigs configuration and bundled engineering resources. Our Conventional Commit conventions remain instructions rather than commit-message enforcement hooks.
