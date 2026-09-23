# Reference material

Read through the funfigs skill. Its adaptation rules govern workflow, tools, commits and reporting. This file is supporting material, not an independently registered skill.

# Checklists: aposd-simplifying-complexity

Source: A Philosophy of Software Design (Ousterhout), Chapters 8, 10, 18

---

## Pull Complexity Downward - Decision

- [ ] PD-1: "Is this complexity closely related to the module's existing functionality?"
- [ ] PD-2: "Will pulling down simplify code elsewhere in the application?"
- [ ] PD-3: "Will pulling down simplify the module's interface?"
- [ ] PD-4: "Are ALL THREE conditions YES?"  to  Pull complexity down

---

## Configuration Parameters

- [ ] CP-1: "Am I exporting a parameter because I'm uncertain what value to use?"  to  Compute automatically instead
- [ ] CP-2: "Am I exporting because different contexts need different values?"  to  Use reasonable default, expose only for exceptions
- [ ] CP-3: "Am I letting user decide because policy decision is unclear?"  to  Make a decision and own it

---

## Error Reduction Hierarchy (Apply in Order)

- [ ] ER-1: "Can semantics be redefined to eliminate the error condition?"  to  Define out of existence
- [ ] ER-2: "Can exception be handled at low level without exposing?"  to  Mask
- [ ] ER-3: "Can multiple exceptions share the same handling?"  to  Aggregate
- [ ] ER-4: "Is error rare, unrecoverable, and non-value-critical?"  to  Just crash (app-level only)
- [ ] ER-5: "None of above?"  to  Must expose (exception information needed outside module)

---

## When NOT to Apply Hierarchy

- [ ] NA-1: "Security-critical errors?"  to  Keep distinct types for audit/logging
- [ ] NA-2: "Retry-differentiated errors?"  to  Expose type info for retry decisions
- [ ] NA-3: "Silent data loss risk?"  to  Fail fast for essential data errors
- [ ] NA-4: "Library code?"  to  Expose errors; let app-level code crash

---

## Validation Gates

- [ ] VG-1: "For Define out: Does anyone NEED to detect this error case?"
- [ ] VG-2: "For Mask: Does the caller have ANY useful response to this error?"
- [ ] VG-3: "For Aggregate: Do callers handle these errors identically?"
- [ ] VG-4: "For Crash: Is this (a) application-level, (b) truly unrecoverable, AND (c) crash acceptable?"

---

## Define-Out Appropriateness Test

- [ ] DO-1: "Would this state occur in normal, correct operation?"  to  Safe to define out
- [ ] DO-2: "Can the caller proceed meaningfully with the 'defined out' state?"  to  Safe
- [ ] DO-3: "Does the user/system have another way to detect this condition if needed?"  to  Safe

---

## Obviousness Techniques

- [ ] OT-1: "Can I reduce information needed?" (Abstraction, eliminate special cases)
- [ ] OT-2: "Can I leverage reader knowledge?" (Follow conventions, meet expectations)
- [ ] OT-3: "Can I present explicitly?" (Good names, strategic comments)

---

## Common Obviousness Problems

- [ ] OP-1: "Generic containers (Pair, Tuple)?"  to  Define specific class with named fields
- [ ] OP-2: "Event-driven handlers (hidden control flow)?"  to  Document invocation context
- [ ] OP-3: "Type mismatches (List declared, ArrayList allocated)?"  to  Match declaration to allocation
- [ ] OP-4: "Violated expectations (code doesn't do what reader assumes)?"  to  Document or refactor

---

## Transformation Checklist (Mandatory Gate)

- [ ] TC-4: Complexity moved to fewer places (not just relocated)?
- [ ] TC-5: Interfaces simpler than before?
- [ ] TC-6: Callers do less work than before?
- [ ] TC-7: Error handling consolidated or eliminated?
- [ ] TC-8: Reader needs less context to understand?

---

## Red Flags

- [ ] RF-1: "Scattered exceptions?" - Same error handled in many places  to  Aggregate to single handler
- [ ] RF-2: "Configuration explosion?" - Many parameters exported  to  Compute automatically, provide defaults
- [ ] RF-3: "Caller doing module's work?" - Logic outside that belongs inside  to  Pull complexity down
- [ ] RF-4: "Over-defensive code?" - Checks for impossible conditions  to  Define errors out
- [ ] RF-5: "Generic containers?" - `Pair<X,Y>` obscures meaning  to  Create named structure
- [ ] RF-6: "Comment-dependent understanding?" - Code unreadable without comments  to  Refactor for obviousness
- [ ] RF-7: "Error masked without observability?" - Applying Mask or Define-out but no logging, metrics, or alternate signal when the error actually occurs  to  Every masked error needs an observability escape hatch (log, metric, health check) so operators can detect when masking hides a real problem

---
