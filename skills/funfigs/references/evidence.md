# Evidence

## Debugging

We first state the mismatch between expected and observed behaviour. We capture the input, environment, version, timing and error evidence needed to reproduce it, without copying credentials or unnecessary personal data.

We trace the failing path and form testable hypotheses. Each diagnostic should distinguish between plausible causes. We prefer a read-only observation or small local reproduction before changing configuration or adding instrumentation to a live system.

We separate the trigger from the underlying defect. A dependency timeout can trigger a failure while an unbounded retry policy causes the outage. Correlated timestamps alone do not establish causation.

When reproduction is unavailable, we label confidence and list the evidence supporting it. We do not deploy a speculative fix under a request to diagnose. When a fix is authorised, we target the cause and check both the original failure and a neighbouring valid case.

## Reviewing

We establish the intended change and compare it with the implementation. We trace modified values to their consumers, including callers outside the edited files. We pay particular attention to compatibility, authorisation, error handling, persistence, resource ownership and concurrency.

A finding includes the concrete condition, the incorrect result and a precise code location. We prioritise by likely impact and reproducibility. We distinguish confirmed defects from questions and optional improvements, and do not turn style preferences into correctness findings.

We verify that a proposed defect is not handled elsewhere before reporting it. We avoid duplicate findings that describe the same root cause. If no actionable defect is found, we say so without implying exhaustive correctness.

## Evidence discipline

We retain the connection between a claim and its observation. Test output supports only the inputs and environment exercised. An unavailable service, skipped check or synthetic result stays labelled. We do not invent benchmark figures, logs, citations or successful execution.
