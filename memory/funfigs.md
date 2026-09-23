---
name: Funfigs configuration
description: Decisions about our shared local coding-agent configuration
type: user
---

We use one local repository for our personal Claude Code and Codex configuration. Both agents share maintained instructions and file-based memory from this repository. A change made through either agent should be available to the other on its next read.

We keep the full earlier engineering bundle locally alongside the concise Funfigs workflows: 19 topic guides, 23 design-pattern recipes and supporting references. The local installation has ten skill entrypoints; five restricted utility bundles remain excluded from Git. We keep Maisa engineering company skills in the separate company-managed plugin and do not copy them into this personal repository.
