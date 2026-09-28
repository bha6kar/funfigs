# Plan review

We evaluate the proposed plan against the requested outcome and the repository as it exists. A request to review or rewrite a plan does not authorise implementing it.

We read the plan, project instructions, affected interfaces and relevant tests. For each consequential assumption we seek concrete evidence in callers, dependencies, data models or configuration. External research is limited to unresolved compatibility or API questions and uses primary sources; we keep private code out of search queries.

We challenge:

- Work that does not contribute to an acceptance criterion.
- New layers, services or dependencies where an existing mechanism suffices.
- Incorrect sequencing, hidden prerequisites and changes with overlapping ownership.
- Missing error paths, authentication boundaries, concurrency, retries or cleanup.
- Data migration, backwards compatibility, mixed-version operation and rollback gaps.
- Verification expressed as activities rather than observable pass/fail conditions.
- Estimates or performance claims unsupported by the actual workload.

We distinguish blockers from preferences and cite the relevant code for actionable concerns. We retain sound decisions rather than rewriting for style. When revision is requested, we produce the smallest viable plan with scope, ordered changes, acceptance checks and unresolved decisions. We preserve the original unless asked to edit its file. We do not require another model, multiple reviewers or a fixed number of passes.
