# Engineering workflows

We select the workflow that matches the user's request and load relevant topic guides from SKILL.md.

## Research

We inspect the current system, identify intended users and behaviour, and separate known constraints from assumptions. We resolve material ambiguities with the user while continuing independent work. We describe options and their trade-offs when the evidence supports multiple approaches. We save a research artefact only when useful to the task.

## Plan

We inspect existing interfaces and tests, define acceptance criteria, and break larger work into coherent changes. Each stage identifies affected components, dependencies, applicable engineering guidance and suitable verification. We record a plan when the work needs durable state. We use existing authorisation to proceed; a request for a plan alone does not authorise implementation.

## Build

We establish the current behaviour and relevant test baseline. We implement the authorised changes in dependency order and keep edits scoped. Untested legacy code receives characterisation coverage where needed; new behaviour receives meaningful verification. We inspect errors, cancellation, shared state and cleanup when applicable. We assess interactions across stages before declaring completion.

Commits and publication follow the user's requested delivery scope and global Git rules. Upstream phase trailers, blanket staging commands and automated pushes do not apply.

## Debug

We reproduce the issue, narrow the affected path, and form a hypothesis with a prediction that can be tested. We use observations to distinguish competing explanations. When a fix is authorised, we change the cause, verify the intended behaviour and inspect related paths for the same defect. Diagnosis-only requests end with evidence and a proposed correction.

## Review

We compare the actual code and observable behaviour with requirements. We identify specific actionable defects and explain triggers and consequences. We distinguish correctness issues from design preferences. We use an independent reviewer when requested or otherwise authorised and useful; checks remain executable by one agent.

## Performance

We define the metric and workload, measure a baseline, and locate the bottleneck. We prefer changes to algorithms, data movement and avoidable I/O when those account for the cost. We compare repeated measurements under equivalent conditions and retain changes justified by the evidence and maintenance cost.
