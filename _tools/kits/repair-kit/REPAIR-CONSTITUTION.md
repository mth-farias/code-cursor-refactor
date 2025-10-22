# Repair Kit Constitution

**Version**: 1.0.0  
**Status**: Stable  
**Last Updated**: 2025-10-21

---

## Purpose

This constitution defines the immutable principles that govern all fixes conducted with this kit.

**Constitutions are STABLE** - they change rarely and only with strong justification.  
**Guidelines evolve** - they adapt based on experience (see HOW-TO-RUN-A-FIX.md).

---

## Core Principles

### 1. Plan-First Over Ad-Hoc

**Principle**: Every fix starts with a plan, never improvise on critical systems.

**This Means**:
- Create detailed fix plan before touching code
- Identify affected files upfront
- Design rollback strategy before executing
- Get approval on plan before implementation

**Rationale**: Unplanned fixes create more problems. Planning prevents cascading failures.

---

### 2. One Issue At A Time

**Principle**: Fix ONE specific issue per cycle, not multiple unrelated issues.

**This Means**:
- Each fix branch addresses single root cause
- Don't bundle unrelated fixes together
- Complete and validate one fix before starting next
- Batch similar fixes (e.g., all BOM removals) but not different fix types

**Rationale**: Multiple simultaneous fixes make debugging impossible. One issue = clear cause/effect.

---

### 3. Backup Before Modify

**Principle**: Always preserve ability to rollback, never destructive changes.

**This Means**:
- Create git branch before any fix
- Backup affected files before modification
- Document exact changes made
- Test rollback procedure before committing

**Rationale**: Fixes can fail. Rollback capability is safety net.

---

### 4. Validate After Fix

**Principle**: Prove the fix worked, don't assume success.

**This Means**:
- Re-run relevant tests after fix
- Partial re-audit of affected components
- Compare before/after metrics
- Verify no regressions introduced

**Rationale**: "Fixed" ≠ verified fixed. Validation proves success.

---

### 5. Rollback On Failure

**Principle**: If fix doesn't pass validation, rollback immediately.

**This Means**:
- Don't ship unvalidated fixes
- Don't accumulate failed fixes
- Clean rollback better than messy fix
- Learn from failure, plan better next attempt

**Rationale**: Failed fixes create technical debt. Clean state better than broken state.

---

## Quality Enforcement

Based on incremental approach from 00-know-how/implementation/01-incremental-approach.md:

### Fix → Validate → Iterate Pattern

1. **Fix**: Execute one fix step
2. **Validate**: Prove it worked
3. **If valid**: Next step
4. **If invalid**: Rollback step, fix the fix

**Never proceed without validation.**

---

## Forbidden Practices

These practices violate the constitution and must never occur:

1. **Fixing without a plan**
2. **Bundling unrelated fixes**
3. **Skipping backup step**
4. **Assuming fix worked without testing**
5. **Proceeding with failed validation**
6. **Hiding regressions**
7. **Committing without approval**
8. **Modifying code during validation**

---

## Success Criteria

A fix is successful when:

1. Fix plan created and approved
2. Backup completed before changes
3. Fix executed as planned
4. Validation shows improvement
5. No regressions introduced
6. User approves merge
7. Changes committed to main

---

## Evolution

This constitution may evolve when:
- Fundamental flaw in repair principles discovered
- Better fix methodology emerges
- Principles proven ineffective through multiple fixes

**Process**: Propose change → Validate through pilot fix → Update constitution → Version bump

**Frequency**: Rare (constitution should be stable foundation)

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

