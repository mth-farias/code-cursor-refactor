# [Fix Name] - Fix Plan

**Version**: 1.0.0  
**Created**: YYYY-MM-DD  
**Fix Lead**: [Name]  
**Priority**: BLOCKER | CRITICAL | HIGH | MEDIUM | LOW  
**Estimated Duration**: [X minutes/hours]

---

## Issue Summary

**Problem**: [What's broken]

**Root Cause**: [Why it's broken]

**Impact**:
- Files Affected: [N]
- Features Blocked: [List]
- Users Impacted: [Who/what]

**Priority Justification**: [Why this priority level]

---

## Solution Design

**Approach**: [How you'll fix it]

**Alternatives Considered**:
- Option A: [Approach] - [Why chosen/not chosen]
- Option B: [Approach] - [Why chosen/not chosen]

**Selected**: [Which option and why]

**Risk Level**: Low | Medium | High

---

## Affected Files

**Total**: [N] files

**List**:
1. `path/to/file1.py` - [What will change]
2. `path/to/file2.py` - [What will change]

**Verification**: [How list was generated - scan/manual/automated]

---

## Fix Phases

### Phase 0: Preparation
- [ ] Create fix templates
- [ ] Define success metrics
- [ ] Prepare rollback procedure

### Phase 1: Backup
- [ ] Create branch: `fix/[issue-name]`
- [ ] Backup files to `.fix-backups/[timestamp]/`
- [ ] Verify backup integrity

### Phase 2: Execute Fix
- [ ] [Specific step 1]
- [ ] [Specific step 2]
- [ ] [Specific step 3]

### Phase 3: Validate Syntax
- [ ] Run syntax checks
- [ ] Verify no new errors
- [ ] Check file integrity

### Phase 4: Partial Re-Audit
- [ ] Re-run Phase 2 (imports) on affected files
- [ ] Re-run Phase 3 (integration) if needed
- [ ] Compare before/after metrics

### Phase 5: Approval
- [ ] Generate before/after report
- [ ] User reviews
- [ ] Decision: Merge | Rollback | Iterate

---

## Rollback Procedure

**If fix fails**:
```bash
git checkout main -- [files]
git branch -D fix/[issue-name]
```

**Verify rollback**:
```bash
git diff main  # Should show no changes
```

**Rollback Time**: [X minutes]

---

## Success Criteria

**Must Achieve**:
- [ ] [Metric 1]: Before [X] → After [Y]
- [ ] [Metric 2]: Before [X] → After [Y]
- [ ] No new errors introduced
- [ ] No regressions in working files

**Must NOT Happen**:
- [ ] Any working file breaks
- [ ] Any new syntax errors
- [ ] Metrics degrade

---

## Before/After Metrics

| Metric | Before | Target | Risk If Fails |
|--------|--------|--------|---------------|
| [Metric 1] | [Value] | [Value] | [Impact] |
| [Metric 2] | [Value] | [Value] | [Impact] |

---

## Approval

**Plan Approved By**: [Name]  
**Date**: YYYY-MM-DD  
**Ready to Execute**: [ ] Yes [ ] No

---

## Execution Log

[Document actual execution - times, issues, deviations]

---

**Version**: 1.0.0 | **Created**: YYYY-MM-DD

