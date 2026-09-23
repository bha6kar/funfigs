# Operations

## Performance

We define the measure before optimising: workload, input size, concurrency, latency distribution, throughput, memory or cost. We collect a baseline in a representative environment and identify the dominant constraint using appropriate profiling or tracing.

We change one meaningful factor at a time when comparing results. We preserve correctness checks, use repeated measurements and distinguish measurement noise from a reliable improvement. We consider cold versus warm behaviour and tail latency rather than reporting only an average.

We inspect algorithmic work, data movement, query shape and repeated remote calls before introducing caching or concurrency. Caches need ownership, keys, invalidation, bounds and stale-data semantics. Parallel work needs bounded fan-out, cancellation and backpressure.

We report the observed workload and trade-offs alongside any result. An improvement on a local fixture is not a production guarantee.

## Reliability

We identify which failures are expected and which must propagate. We bound retries by attempts or time, distinguish retryable from permanent errors and avoid duplicating non-idempotent effects. Timeouts should leave enough budget for callers to recover.

We assess failure isolation, queue growth, connection limits and recovery after interruption. A fallback must preserve the contract or make degraded behaviour explicit. We do not silently return success when a required write failed.

## Security and observability

We inspect trust boundaries relevant to the change: identity, object-level access, secret handling, input interpretation and outbound destinations. We avoid logging tokens or complete sensitive payloads. We use synthetic fixtures for security checks unless the user has authorised a defined live target.

We add telemetry that answers a concrete operational question. We keep identifiers useful for correlation while controlling cardinality and data exposure. An alert needs an actionable condition and a clear owner; a dashboard does not by itself establish service health.

## Rollout

We distinguish building a change from releasing it. For an authorised release we confirm the target environment, compatibility assumptions, success signals and a rollback or containment path. We stop if execution requires broader permissions or a different target than approved.
