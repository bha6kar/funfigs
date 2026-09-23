# Decisions

## Frame the change

We establish the observable result: who uses it, which input starts it, what successful output looks like, and which existing behaviour must stay intact. We separate requirements stated by the user from assumptions inferred from code.

We inspect the shortest relevant path through the system before designing a replacement. Useful evidence includes callers, stored data, boundary validation, failures, tests and deployment constraints. We do not map the whole repository when one component answers the question.

When uncertainty is consequential, we propose a small experiment or ask a focused question. A plan records the decision that the answer would change, not a generic list of concerns.

## Interfaces and ownership

We assign each mutable fact one clear owner. We make boundaries explicit about input shape, output shape, failure behaviour, lifetime and who may call them. An interface should expose the decisions callers need without requiring them to coordinate implementation details.

We prefer existing project abstractions when they fit. We add a new abstraction when it isolates a concrete source of variation or enforces a useful invariant. A helper with one caller can still clarify a complicated operation; a shared helper is not automatically a good boundary.

For APIs we consider compatibility with existing clients, authentication versus authorisation, pagination, error representation, retry behaviour and data exposure. We resolve time zones, units, nullability and identifier semantics where they cross boundaries.

## Select a structure

We compare the simplest workable approach with any meaningful alternative. We explain the trade-off using the actual workload and change pressure rather than a pattern label.

- A changing external API may justify an adapter at the boundary.
- Several interchangeable policies may justify injected functions or objects.
- Durable transitions with restricted ordering may justify an explicit state model.
- Independently evolving consumers may justify events, with delivery and ordering semantics stated.
- A single straightforward operation usually needs none of these.

We make concurrency, consistency and ownership choices before hiding them behind convenience APIs. We identify where partial failure can leave observable state and how recovery works.

## Plan delivery

We split work by demonstrable behaviour, not by arbitrary file counts. Each meaningful stage identifies affected boundaries, a verification method and any compatibility or rollout step. Data migrations distinguish new writes, existing records, mixed-version operation and rollback limits.

We keep a plan proportionate. We do not introduce infrastructure, new services or frameworks solely to make the design look complete.
