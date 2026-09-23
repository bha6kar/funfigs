# Engineering agreements

We use these principles for code changes. Our project instructions supply the concrete commands and architecture.

For detailed engineering work, we use the installed funfigs skill and load only the relevant guides and checklists. It covers architecture, module design, control flow, defensive programming, legacy code, refactoring, design patterns, testing, performance, documentation and planning.

## Debugging

We establish a reproducible failure, inspect the relevant logs and call path, and state a hypothesis before changing code. We choose an observation or experiment that can disprove it. We fix the cause, exercise the failing case, and check nearby code for the same defect. Temporary instrumentation is removed when it no longer serves the product.

## Design

We follow existing abstractions and keep implementation details inside the module that owns them. We judge an abstraction by whether its callers become simpler. We expose configuration when callers have different requirements, and choose a sensible default. We preserve meaningful error distinctions when recovery, security or data integrity depends on them.

## Verification

We connect each requested behaviour to its implementation and appropriate evidence. Tests exercise observable behaviour and useful failure cases. We inspect empty inputs, invalid values, resource cleanup and partial failures when the change touches those paths. For concurrent work, we identify shared state and check cancellation, ordering and stale writes. We report incomplete verification honestly.

## Scope

We scale planning and verification to the change. Small changes use the direct workflow; larger changes benefit from explicit acceptance criteria and implementation stages. We keep unrelated edits intact. Our existing global Git and writing rules govern commits and deliverables.
