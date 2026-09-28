---
name: funfigs
description: Plan, implement, debug, review or improve software using Funfigs engineering workflows. Use when explicitly requested with ff or funfigs, or when a task needs substantive engineering decisions. Load only the relevant workflow.
---

# Funfigs

We start from the requested outcome and the repository's actual constraints. A familiar pattern or preferred tool is not evidence that a project needs it.

## Choose the work

We distinguish explanation, investigation, review and implementation. We do not turn a read-only request into code changes. We identify the relevant project instructions, current working-tree changes, entrypoints and available checks before acting.

For small, well-defined changes we work directly. For uncertain or cross-cutting work we select the relevant guide:

| Work | Guide |
| --- | --- |
| Scope a feature, compare approaches or design an interface | [Decisions](references/decisions.md) |
| Implement, test, refactor or migrate existing behaviour | [Changes](references/changes.md) |
| Investigate failures or review correctness | [Evidence](references/evidence.md) |
| Measure performance or assess operational reliability | [Operations](references/operations.md) |
| Finish an implementation, including neglected user-facing states (`ff finish`) | [Finish](references/finish.md) |
| Challenge and revise a proposed plan (`ff review-plan`) | [Plan review](references/review-plan.md) |
| Polish wording or match our voice (`ff polish`) | [Writing polish](references/polish.md) |
| Check local installation health (`ff doctor`) | [Setup health](references/doctor.md) |

## Working agreement

For detailed topic guidance, we read [the complete engineering library index](library.md). It routes to 19 topic guides, their checklists and 23 design-pattern recipes. We use [the adapted workflows](workflows.md) for research, planning, implementation, debugging, review and performance. The four concise guides above remain available alongside the full library.

We apply the adaptation rules in the library index before using bundled source material. Source commands and agent definitions are references, not instructions to change models, delegate, commit or publish. All library paths resolve locally beneath this skill directory.

We preserve unrelated edits and existing public contracts unless the task includes changing them. We make assumptions explicit when they affect behaviour, cost, compatibility or authority. We ask only when a missing choice materially changes the result.

We choose checks that could expose the specific failure introduced by a change. A successful command is evidence only for what it exercised. We report unresolved uncertainty without claiming tests or access we did not have.

We keep company-specific skills separate unless requested. We do not fetch another skill repository, require a particular model, or start additional agents as part of this workflow. The caller's permissions and delegation rules remain in force.

We finish with the outcome, relevant file locations and any remaining limitation. We follow the shared writing and Git preferences. Committing, pushing, deploying or modifying live data requires authority for that action, not merely a request to discuss it.
