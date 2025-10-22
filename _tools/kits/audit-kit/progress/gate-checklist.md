# Gate Validation Checklist

**Audit**: [Audit Name]  
**Phase**: [Phase Number and Name]  
**Date**: YYYY-MM-DD

---

## Purpose

Validate phase completion before proceeding to next phase.

**All items must be checked** to pass gate.

---

## Completeness Checks

- [ ] All items in scope processed
- [ ] No files/items skipped
- [ ] Output file generated
- [ ] Output file valid (JSON parseable, markdown renders, etc.)
- [ ] All required fields present in output

**Completeness**: [X/5] (5/5 required to pass)

---

## Quality Checks

- [ ] Evidence cited for all findings
- [ ] Error messages recorded (not hidden)
- [ ] Metrics calculated correctly
- [ ] No assumptions made
- [ ] Process followed phase rule

**Quality**: [X/5] (4/5 minimum to pass)

---

## Validation Checks

- [ ] Automated validation passed (if applicable)
- [ ] Manual spot-check passed (sample verification)
- [ ] Count matching (totals consistent across outputs)
- [ ] No contradictions with previous phases

**Validation**: [X/4] (4/4 required to pass)

---

## Anti-Gaming Checks

- [ ] No selective auditing (all items processed)
- [ ] No hidden failures
- [ ] No "probably works" statuses
- [ ] Evidence is specific (file:line, not vague)
- [ ] Reproducible (someone else could verify)

**Anti-Gaming**: [X/5] (5/5 required to pass)

---

## Overall Gate Status

**Total Score**: [X/19]

- 19/19 (100%): ✅ PASS - Proceed to next phase
- 17-18/19 (89-94%): ⚠️ CONDITIONAL - Address issues then proceed
- <17/19 (<89%): ❌ FAIL - Complete phase properly before proceeding

---

## Decision

**Gate Status**: [ ] PASS [ ] CONDITIONAL [ ] FAIL

**Action**: [Proceed / Address Issues / Redo Phase]

**Issues to Address** (if conditional/fail):
1. [Issue 1]
2. [Issue 2]

---

## Approver

**Validated By**: [Name]  
**Date**: YYYY-MM-DD  
**Approved**: [ ] Yes [ ] No

---

**Template Version**: 1.0.0

