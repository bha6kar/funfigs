---
name: funfigs
description: Apply Funfigs engineering guidance when designing architecture or APIs, refactoring legacy code, investigating bugs, selecting design patterns, reviewing correctness, planning substantial features, or measuring performance. Select only the relevant references for the requested engineering task.
---

# Funfigs engineering

We use the complete bundled engineering library through the topic index below. We load the matching guide and its linked checklists, then follow further references only when the task needs them. We do not load the entire library for routine edits.

## Adaptation rules

These rules govern every bundled source, including its examples and workflow prescriptions.

- We honour the user's task scope and existing authorisation. A diagnosis or review remains read-only unless changes are requested. A build request authorises ordinary implementation without repeated planning confirmations.
- We follow our live global rules and the current project's conventions. Commits use a single Conventional Commit subject, with no body, AI attribution, review trailers or process tallies. We stage exact intended paths. We do not run the upstream commit recipe or trust-report machinery.
- We keep the session's chosen model. Upstream model ladders, hard-coded model names, majority-vote review and agent counts are reference examples, not requirements. Delegation follows the user's preferences and the tools actually available. A solo session can perform all engineering checks.
- We treat tool names such as Skill, Read, Task and AskUserQuestion as descriptions of capabilities. We read sibling guides directly; no installed funfigs plugin or proprietary tool is required. Paths beginning skills/, references/, agents/, commands/ or docs/ in bundled text resolve beneath this skill's upstream/ directory. Other relative links resolve from the source file.
- We apply engineering criteria with judgement. Numeric thresholds and historical speedup figures in references are heuristics, not proof of a defect or a performance guarantee. We measure the actual workload before recommending performance changes.
- We use uv for Python. We write new deliverables in UK English and our own voice. We explain the resulting behaviour and relevant validation without adopting source templates that narrate review counts, model identities or development history.
- We preserve the distinction between current behaviour and intended behaviour. Characterisation tests protect existing behaviour during refactoring; a confirmed bug needs a regression assertion for the desired behaviour.

## Topic routing

References to CLAUDE_PLUGIN_ROOT resolve to this skill's upstream/ directory. Names such as funfigs:cc-debugging select the matching local guide below. These are reference aliases, not separately registered skills or slash commands. We use `ff debug`, `ff plan`, `ff review` or another ordinary prompt to select the workflow. Paths beginning `.funfigs/` in bundled examples describe optional project-local working files, not a required plugin installation.

| Task | Read |
| --- | --- |
| Clarify an underspecified request | [Clarification](upstream/skills/clarify/GUIDE.md) |
| Plan a substantial feature | [Planning](upstream/skills/planning/GUIDE.md) |
| Design service or layer boundaries | [Architecture](upstream/skills/ca-architecture-boundaries/GUIDE.md) |
| Design a new module or API | [Deep modules](upstream/skills/aposd-designing-deep-modules/GUIDE.md) |
| Assess an existing module | [Module review](upstream/skills/aposd-reviewing-module-design/GUIDE.md) |
| Simplify implementation complexity | [Complexity](upstream/skills/aposd-simplifying-complexity/GUIDE.md) |
| Verify completeness and correctness | [Correctness](upstream/skills/aposd-verifying-correctness/GUIDE.md) |
| Improve conditionals and loops | [Control flow](upstream/skills/cc-control-flow-quality/GUIDE.md) |
| Investigate a failure | [Debugging](upstream/skills/cc-debugging/GUIDE.md) |
| Validate trust boundaries and errors | [Defensive programming](upstream/skills/cc-defensive-programming/GUIDE.md) |
| Work out a nontrivial routine | [Pseudocode design](upstream/skills/cc-pseudocode-programming/GUIDE.md) |
| Plan testing and quality practices | [Quality](upstream/skills/cc-quality-practices/GUIDE.md) |
| Refactor covered code safely | [Refactoring](upstream/skills/cc-refactoring-guidance/GUIDE.md) |
| Design routines and classes | [Routine design](upstream/skills/cc-routine-and-class-design/GUIDE.md) |
| Improve naming, comments and docs | [Clarity](upstream/skills/code-clarity-and-docs/GUIDE.md) |
| Document a project's actual conventions | [Standards](upstream/skills/code-standards/GUIDE.md) |
| Select a design pattern for a concrete problem | [Patterns and 23 recipes](upstream/skills/gof-design-patterns/GUIDE.md) |
| Optimise a measured bottleneck | [Performance](upstream/skills/performance-optimization/GUIDE.md) |
| Change code without adequate tests | [Legacy code](upstream/skills/welc-legacy-code/GUIDE.md) |

## Workflows

We read [the adapted workflows](workflows.md) for research, planning, implementation and review. They replace the execution mechanics of bundled upstream commands. The engineering guides remain available in full.

We read [provenance](PROVENANCE.md) for source version, packaging changes and upstream reference locations.
