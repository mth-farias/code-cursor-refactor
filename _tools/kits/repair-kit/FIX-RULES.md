# Fix Rules

**Version**: 1.0.0  
**Purpose**: Clear CAN/CANNOT rules for each fix phase  
**Status**: Enforcement document

---

## Universal Rules (All Fix Phases)

### CAN

- Follow the fix plan
- Validate at each step
- Rollback if needed
- Document deviations
- Request approval before merge

### CANNOT

- Deviate from plan without documenting
- Skip validation steps
- Merge without approval
- Bundle unrelated fixes
- Proceed with failed validation

---

## Phase 0: Plan Preparation

### CAN

- Create fix templates
- Define success criteria
- Design rollback procedure
- Prepare tools/scripts

### CANNOT

- Start fixing without plan
- Skip rollback design
- Use vague success criteria

---

## Phase 1: Backup

### CAN

- Create git branch
- Backup affected files
- Verify backup integrity
- Test rollback procedure

### CANNOT

- Modify without backup
- Proceed with failed backup
- Skip branch creation

---

## Phase 2: Execute Fix

### CAN

- Modify affected files per plan
- One change type at a time
- Verify each file after change
- Document exact changes

### CANNOT

- Change files outside plan
- Bundle different fix types
- Skip per-file validation
- Modify during validation phase

---

## Phase 3: Validate Syntax

### CAN

- Run automated syntax checks
- Verify all files parseable
- Check for new errors
- Document any issues found

### CANNOT

- Assume syntax is fine
- Skip validation to save time
- Hide new errors

---

## Phase 4: Partial Re-Audit

### CAN

- Re-run audit phases on affected files
- Compare before/after metrics
- Verify improvement
- Check for regressions

### CANNOT

- Skip re-audit
- Modify results to look better
- Hide regressions

---

## Phase 5: Approval & Merge

### CAN

- Present complete before/after report
- Show all changes
- Wait for user approval
- Merge if approved
- Rollback if rejected

### CANNOT

- Merge without approval
- Hide changes or failures
- Proceed with user rejection
- Skip rollback if failed

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

