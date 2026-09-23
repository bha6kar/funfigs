# Changes

## Implement the intended behaviour

We read nearby code and the build configuration to follow the project's conventions. We trace the normal path and the relevant failure paths. We keep input parsing, business decisions and external side effects separable enough to verify without unnecessary ceremony.

We validate untrusted data where it enters a trusted boundary. We distinguish absent, empty, invalid and unauthorised values when their meanings differ. We avoid catching failures so broadly that a broken operation appears successful.

We make resource lifetimes visible: files close, locks release, requests cancel and temporary state has an owner. Repeated operations need an explicit answer for duplication, retries and partially completed work.

## Tests that constrain the result

We select checks from the behaviour at risk:

- Pure transformations: representative values, boundaries and invalid inputs.
- State changes: permitted transitions, rejected transitions and repeated requests.
- Storage or service boundaries: contract shape, partial failures and recovery.
- Concurrent work: ordering assumptions, cancellation and shared-state ownership.
- User-facing flows: one realistic path through the affected integration.

We use small deterministic examples where possible. We do not replace a dependency with a mock so broad that it assumes the very contract under test. We distinguish local unit confidence from integration confidence.

For a defect, we try to capture a failing case before changing behaviour. For a refactor, we preserve observed behaviour with focused checks, except where a separately identified bug is intentionally corrected. If checks cannot run, we state the exact limitation and the next useful check.

## Refactoring and legacy code

We isolate structure changes from behaviour changes when that makes review safer. We inspect callers and hidden coupling through persistence, environment, ordering and global state. We introduce the smallest seam needed to observe or control the dependency in question.

We do not remove an awkward branch until its purpose is understood. An undocumented compatibility constraint is still a constraint. We remove dead code only with evidence that it is unreachable or obsolete within the task's scope.

## Migration and handoff

We account for existing data and mixed versions. Destructive migrations require an explicit target, recovery strategy and approval appropriate to the impact. A code rollback does not necessarily reverse a data migration.

We review the final diff for accidental files, secrets, unrelated formatting and changed permissions. We summarise externally visible behaviour and remaining risks. Repository documentation describes current operation and the rationale that future maintenance needs.
