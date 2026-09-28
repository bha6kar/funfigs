# Funfigs

Our shared rules, memory and engineering workflows for Claude Code and Codex.

## Setup

Our global instructions stay local and are excluded from Git. On a fresh clone, we create `shared/AGENTS.md` with our own rules before running the shared installer. We review existing global instructions before replacing them. The optional `funfigs-claude-template.md` snapshot is local-only too.

```sh
uv run --no-project scripts/shared_setup.py check
uv run --no-project scripts/shared_setup.py install
```

We start fresh sessions after installation. Both clients' global instruction files link to `shared/AGENTS.md`. Claude's file-memory directory and Codex's shared-memory instructions point to `memory/`. Saved changes become available at the next read; active responses and private conversation histories are not synchronised.

The installer preserves existing settings and backs up replaced files. We grant workspace access when another project's session needs to edit these shared files. For Codex CLI, `sh /absolute/path/to/funfigs/scripts/codex.sh` retains the working directory and grants access to this repository.

## Use

- `ff plan this feature`
- `ff review my changes`
- `ff debug this error`
- `ff finish this feature`
- `ff review-plan`
- `ff polish this message`
- `ff doctor`
- `Use funfigs-memory to remember this decision for both agents`

`ff` is a shared prompt shorthand for the engineering skill, not a registered slash command. Company skills stay separately managed and are not combined unless requested.

We use [agent experience setup](docs/agent-experience.md) for the coloured Claude context bar, native Codex CLI footer, quiet tool environment and optional local work/personal launch profiles. These settings are activated locally, not by committing our private client configuration.

## Contents

| Location | Purpose |
| --- | --- |
| shared/AGENTS.md | Local-only common working rules and shorthand, excluded from Git |
| memory/ | Durable notes shared by both clients |
| skills/funfigs/ | 19 engineering topics, 23 design-pattern recipes, checklists and workflows, plus four concise guides |
| skills/funfigs-memory/ | Shared-note maintenance |
| skills/docs/ | Document drafting and editing |
| skills/import-memory/ | Confirmed import into shared local notes |
| skills/morning/ | A source-grounded daily brief |
| skills/docx/, skills/pdf/, skills/pptx/, skills/xlsx/ | Local-only office and PDF workflows with supporting tools |
| skills/skill-creator/ | Local-only skill authoring and evaluation tools |
| scripts/shared_setup.py | Shared installation with preview and backups |
| scripts/config.py | Legacy copy installer for separate Claude destinations |

We keep this repository private. Credentials, sessions and company skill contents do not belong here. Our local installation contains all ten skills listed above. The five local-only bundles remain excluded from Git, so a fresh clone contains five entrypoints, not the complete local installation. The engineering library and the original docs, memory-import and morning references are bundled locally; installation does not fetch another repository. Source and licence notices remain with bundled material.

We use [engineering guidance](docs/engineering.md), [shared-memory details](docs/shared-memory.md) and [maintenance instructions](docs/maintenance.md) for operational details. The legacy template is an optional snapshot, not the live source of truth.
