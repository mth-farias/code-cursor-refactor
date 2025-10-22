# Anti-Regression Measures

**Version**: 1.0.0  
**Purpose**: Prevent fixes from breaking what already works  
**Philosophy**: "First, do no harm"

---

## Purpose

Fixes should improve, not break.

**This document**: Techniques to prevent regressions

---

## Prevention Strategies

### 1. Surgical Fixes (Not Shotgun)

**Do**: Change only what's needed to fix the issue  
**Don't**: Refactor unrelated code while fixing

**Example**:
- Good: Remove BOM from 269 files (one change type)
- Bad: Remove BOM + reformat code + rename variables

---

### 2. Validate Unchanged Files

**Do**: Verify files outside fix scope still work  
**Don't**: Only test changed files

**Technique**: Run full test suite, not just affected tests

---

### 3. Compare Before/After

**Metrics to track**:
- Files working before fix: [N]
- Files working after fix: [N + fixed]
- Files broken by fix: [Should be 0]

**Formula**: `After ≥ Before` (never decrease working files)

---

### 4. Incremental Application

**For bulk fixes**:
- Fix 10 files → validate
- If OK → fix next 10
- If issues → rollback, investigate
- Never fix all at once without validation

---

## Red Flags (Regressions)

**Red Flag 1**: Working file stops working after fix  
**Red Flag 2**: Tests that passed now fail  
**Red Flag 3**: Import that worked now fails  
**Red Flag 4**: Metrics worse after fix  

**Action**: Immediate rollback and investigation

---

## Validation Checklist

Before merging any fix:

- [ ] All affected files still parseable
- [ ] No working files broken
- [ ] Metrics improved (not degraded)
- [ ] No new errors introduced
- [ ] Tests still pass (all, not just related)
- [ ] Rollback procedure verified

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

