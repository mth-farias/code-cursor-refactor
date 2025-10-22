# How To Run An Audit

**Version**: 1.0.0  
**Purpose**: Operational guide for executing audit plans  
**Estimated Time**: Varies by audit (typically 2-4 hours)

---

## Purpose

This guide covers HOW to execute an audit plan once it's created.

**Prerequisites**: You have an audit plan (see HOW-TO-PLAN-AN-AUDIT.md)  
**Output**: Completed audit with verified results

---

## Execution Workflow

### Phase Execution Loop

```
For each phase in plan:
  1. Read phase rule (CAN/CANNOT)
  2. Prepare inputs (outputs from previous phase)
  3. Execute phase process
  4. Generate phase output
  5. Validate against gate criteria
  6. If gate passes: proceed to next phase
  7. If gate fails: complete current phase first
```

---

## Phase Execution Steps

### 1. Preparation

**Before starting any phase**:
- [ ] Read the phase description in audit plan
- [ ] Understand the phase rule (what you CAN and CANNOT do)
- [ ] Verify inputs are available (from previous phase)
- [ ] Review output format expected
- [ ] Check gate criteria (know what "done" looks like)

**Time**: 5 minutes per phase

---

### 2. Execution

**During phase execution**:
- [ ] Follow the phase rule strictly
- [ ] Document all findings (good and bad)
- [ ] Record errors exactly as encountered
- [ ] Don't skip items to save time
- [ ] Don't interpret beyond phase scope
- [ ] Track progress (use progress/phase-tracker.md)

**Time**: Varies by phase

---

### 3. Output Generation

**Creating phase outputs**:
- [ ] Use specified output format (JSON, markdown, etc.)
- [ ] Include all required fields
- [ ] Validate output structure (JSON valid, fields present)
- [ ] Save to designated location
- [ ] Include timestamp and phase identifier

**Validation**: Run validation command if provided

---

### 4. Gate Validation

**Before proceeding to next phase**:
- [ ] Review gate checklist (in progress/gate-checklist.md)
- [ ] Verify all gate criteria met
- [ ] Check for blockers or unresolved issues
- [ ] Confirm no shortcuts taken
- [ ] Get approval if required

**Decision**: Pass → Next phase | Fail → Complete current phase

---

## Evidence Collection

### What Counts as Evidence

**Valid Evidence**:
- File paths with line numbers
- Test execution results
- Scan outputs (JSON, logs)
- Error messages (exact text)
- Timestamps and metrics

**Invalid Evidence**:
- "I think it works"
- "Probably configured correctly"
- "Should be fine"
- "Looks like it does X"

---

### Evidence Citation Format

**File reference**: `path/to/file.py:123` (file + line number)  
**Test result**: `Phase 2: import SUCCESS, 45ms`  
**Scan output**: `Phase 1: Found in code-scan.json line 234`  
**Error message**: `ImportError: No module named 'x'` (exact text)

---

## Common Issues

### Issue: Phase taking longer than estimated

**Don't**: Skip items to finish faster  
**Do**: Document why it's taking longer, adjust estimates for future

### Issue: Gate criteria not met

**Don't**: Proceed anyway ("I'll fix it later")  
**Do**: Complete the phase properly, then proceed

### Issue: Unexpected findings

**Don't**: Hide or rationalize away  
**Do**: Document exactly what you found, investigate if needed

### Issue: Output format unclear

**Don't**: Guess the format  
**Do**: Review template, ask for clarification, follow examples

---

## Progress Tracking

### Use progress/phase-tracker.md

Simple checklist:
```markdown
- [x] Phase 0: Templates
- [x] Phase 1: Code scan
- [ ] Phase 2: Import test ← Current
- [ ] Phase 3: Server trace
```

### Update after each phase

Record:
- Phase completion date/time
- Duration
- Key findings
- Any issues encountered

---

## Quality Checkpoints

### During Execution

**Every phase**:
- Am I following the phase rule?
- Am I documenting evidence?
- Am I skipping anything?

**Mid-audit (after ~50%)**:
- Are outputs consistent?
- Are findings making sense?
- Any red flags or concerns?

**End of audit**:
- All gates passed?
- All phases complete?
- Truth table makes sense?

---

## When Things Go Wrong

### Scenario: Can't complete a phase

**Steps**:
1. Document the blocker specifically
2. Mark phase status as BLOCKED
3. Don't proceed to next phase
4. Resolve blocker or adjust plan
5. Resume once blocker resolved

### Scenario: Found major issue mid-audit

**Steps**:
1. Document the issue in audit outputs
2. Continue audit (don't stop to fix)
3. Issue will appear in truth table
4. Address in repair phase (separate from audit)

### Scenario: Phase outputs don't match

**Steps**:
1. Investigation mode: reconcile differences
2. Document contradiction in current phase
3. Verify previous phases weren't wrong
4. Resolve before proceeding

---

## Tips for Success

1. **Read the plan thoroughly first** - understand full flow before starting
2. **Follow phases sequentially** - don't jump ahead
3. **Document everything** - if unsure, over-document
4. **Don't fix issues** - audit observes, repair fixes
5. **Validate gates** - don't skip quality checks
6. **Take breaks** - use handoff-kit if pausing mid-audit

---

## After Audit Complete

### 1. Validate Completeness

- [ ] All phases executed
- [ ] All outputs generated
- [ ] All gates passed
- [ ] Truth table complete

### 2. Review Findings

- What's the overall health?
- What are critical issues?
- What are quick wins?
- What needs deep work?

### 3. Decide Next Steps

**Option A**: Generate documentation (Phase 7) with current state  
**Option B**: Enter repair mode (Phase 6.5) to fix issues first  
**Option C**: Save audit results and exit

### 4. Document Learnings

If this was your first audit with this kit:
- What worked well in the plan?
- What was unclear?
- What would you improve?
- Update HOW-TO-RUN guidelines if patterns found

---

## Evolution Notes

This operational guide EVOLVES based on execution experience.

**After each audit**, consider:
- Were instructions clear?
- Were estimates accurate?
- Were tips helpful?
- What would improve this guide?

Update this guide (not constitution) with improvements.

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

