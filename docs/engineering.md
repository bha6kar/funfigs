# Funfigs engineering

We use one [entrypoint](../skills/funfigs/SKILL.md) to select the material needed for a task. The [full topic index](../skills/funfigs/library.md) covers all 19 bundled engineering guides and 23 design-pattern recipes, including architecture, module design, correctness, debugging, refactoring, legacy code, quality, performance and planning. We keep all 80 source reference files locally, including checklists, workflow commands and agent definitions. [Adapted workflows](../skills/funfigs/workflows.md) govern execution without requiring upstream models, delegation or commit recipes.

We also keep four concise guides:

- [Decisions](../skills/funfigs/references/decisions.md): scope, interfaces, architecture and delivery plans.
- [Changes](../skills/funfigs/references/changes.md): implementation, tests, refactoring and migrations.
- [Evidence](../skills/funfigs/references/evidence.md): diagnosis, review findings and confidence.
- [Operations](../skills/funfigs/references/operations.md): performance, reliability, security and rollout.

We keep workflows proportional to the task. A read-only review does not authorise edits; a local build does not authorise deployment. Project conventions and shared preferences apply throughout.

We invoke the workflow with ordinary prompts such as `ff review my changes` or `ff plan this API`. We load only the relevant references and select abstractions because a concrete problem needs them, not to satisfy a checklist. [Source details](../skills/funfigs/PROVENANCE.md) describe the bundled snapshot and packaging.
