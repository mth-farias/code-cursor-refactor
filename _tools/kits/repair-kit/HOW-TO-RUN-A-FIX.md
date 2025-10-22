# How To Run A Fix

**Version**: 1.0.0  
**Purpose**: Operational guide for executing fix plans safely  
**Estimated Time**: Varies by fix complexity

---

## Execution Workflow

```
1. Review fix plan
2. Create git branch
3. Backup affected files
4. Execute fix (one step at a time)
5. Validate each step
6. Run partial re-audit
7. Generate before/after report
8. User approval
9. Merge OR rollback
```

---

## Phase-by-Phase

### Phase 0: Plan Preparation (5 min)

- [ ] Fix plan approved
- [ ] Success criteria clear
- [ ] Rollback procedure ready
- [ ] All tools/scripts prepared

---

### Phase 1: Backup (5 min)

- [ ] Create git branch: `git checkout -b fix/issue-name`
- [ ] Backup affected files to `.fix-backups/`
- [ ] Verify backup complete
- [ ] Document backup location

**Gate**: Backup verified, rollback tested

---

### Phase 2: Execute Fix (Varies)

- [ ] Follow fix plan steps exactly
- [ ] One file/component at a time
- [ ] Verify each change before next
- [ ] Document any deviations from plan
- [ ] Record actual vs estimated time

**Gate**: All steps executed, no skipped items

---

### Phase 3: Validate Syntax (5 min)

- [ ] Run syntax checker on all affected files
- [ ] Ensure no new errors introduced
- [ ] Verify files still parseable
- [ ] Check for any broken references

**Gate**: No new errors, all files valid

---

### Phase 4: Partial Re-Audit (10-20 min)

- [ ] Re-run relevant audit phases on affected files
- [ ] Compare before/after metrics
- [ ] Verify improvement shown
- [ ] Check no regressions in unaffected files

**Gate**: Metrics improved, no regressions

---

### Phase 5: Approval & Merge (10 min)

- [ ] Generate before/after report
- [ ] Present to user
- [ ] User reviews changes
- [ ] User approves OR requests changes OR rejects
- [ ] If approved: merge to main
- [ ] If rejected: rollback

**Gate**: User approval obtained

---

## Validation Techniques

**Syntax Validation**:
```bash
python -m py_compile file.py  # Python files
eslint file.js                # JavaScript
```

**Import Validation**:
```bash
python -c "import module_name"
```

**Metric Comparison**:
- Before: Import success 13%
- After: Import success 98%
- Improvement: 85% ✅

---

## When Things Go Wrong

### Fix Breaks Something

**Immediate**:
1. Stop further changes
2. Document what broke
3. Rollback this step
4. Analyze why it broke

**Next**:
5. Revise fix plan
6. Re-attempt with improved approach

### Validation Fails

**Don't**: Merge anyway  
**Do**: Rollback, investigate, fix the fix

### Unsure If Fix Worked

**Don't**: Guess or assume  
**Do**: Add more validation tests until certain

---

## Evolution Notes

After each fix execution:
- What worked well?
- What was unclear?
- What would improve process?
- Update this guide with learnings

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

