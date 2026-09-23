# Shared Claude and Codex configuration

We keep our canonical rules in `shared/AGENTS.md` and durable notes in `memory/MEMORY.md` and linked topic files. Both clients' global instruction files link to the same rules. Claude's `autoMemoryDirectory` points to our memory folder; Codex reads and updates it through explicit instructions and the `funfigs-memory` skill.

## Installation

```sh
uv run --no-project scripts/shared_setup.py check
uv run --no-project scripts/shared_setup.py install
```

We restart both clients after installation. Shared edits are available on the next read, not during an already-running response. Both clients are instructed to reread at each turn and after compaction; a fresh session is the reliable activation boundary.

Existing Claude settings and Codex configuration are preserved. A baseline Codex configuration is created only when none exists. Backups are kept under `~/.local/state/funfigs/backups/`. We remove a destination symlink before restoring a regular file from backup.

Both clients receive all ten skill folders present locally. A fresh clone contains five entrypoints; the five ignored office, PDF and skill-authoring bundles remain local-only. The full engineering bundle and original utility references are included behind portable entrypoints. `docs` and `morning` use available services and report missing access. `import-memory` proposes additions to the shared file store and requires confirmation before saving them, rather than using the original reference's private cloud memory tools. Existing synced installations remain untouched and may appear alongside local skills. Company skills stay separately managed.

## Access and boundaries

For Codex CLI work in another project, we run `sh /Users/onyx/maisa/funfigs/scripts/codex.sh` from that project. It retains the working directory and adds write access to this repository. Desktop sessions may require workspace permission before writing shared memory. Project and managed configuration can override global behaviour.

This is shared file-based memory, not synchronised private product memory, conversation history or session state. Existing historical memories are not imported automatically. We can explicitly request `import-memory` to review a supplied export for additions to our shared notes.

We reread before narrow edits, preserve unrelated changes and avoid concurrent edits to the same note: there is no transactional merge. We retain user-confirmed durable information, scope project facts and omit credentials, raw conversations and company skill contents. Before publishing this repository, we review personal content.

The setup follows [Claude memory settings](https://code.claude.com/docs/en/memory), [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [Codex skills](https://learn.chatgpt.com/docs/build-skills).
