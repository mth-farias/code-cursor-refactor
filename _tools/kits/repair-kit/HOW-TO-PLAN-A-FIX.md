# How To Plan A Fix

**Version**: 1.0.0  
**Purpose**: Step-by-step guide to creating systematic fix plans  
**Estimated Time**: 20-40 minutes per fix plan

---

## Purpose

This guide teaches you how to CREATE a fix plan, not how to EXECUTE one.

**Use this when**: Issue identified, need to plan the fix  
**Output**: Complete, safe fix plan ready to execute

---

## The Planning Process

### Step 1: Issue Analysis (5 minutes)

**Questions to answer**:
- What exactly is broken?
- What's the root cause?
- How many files/components affected?
- What's the priority level?
- What's blocking because of this?

**Output**: Issue summary

**Example**:
```markdown
## Issue: BOM Encoding

**Problem**: 269 files have UTF-8 BOM causing import failures
**Root Cause**: Files saved with BOM by editor
**Affected**: 269 Python files across 3 directories
**Priority**: BLOCKER (prevents 85% of imports)
**Impact**: Cannot import → cannot use → 0.3% production rate
```

---

### Step 2: Solution Design (10 minutes)

**Questions to answer**:
- What's the fix approach?
- Are there multiple approaches? (compare)
- What's the least risky?
- What could go wrong?
- How to detect if fix worked?

**Output**: Solution specification

**Example**:
```markdown
## Solution: Remove BOM

**Approach**: Read each file, detect BOM (0xEF 0xBB 0xBF), rewrite without BOM

**Alternatives Considered**:
- A) Manual editor config → Too slow, error-prone
- B) Bulk script → Chosen (fast, consistent, verifiable)

**Risk Level**: Low (non-destructive, reversible)

**Success Indicator**: Files import without syntax errors
```

---

### Step 3: Affected Files Inventory (5 minutes)

**Questions to answer**:
- Exactly which files need changes?
- Can this be automated?
- Any files that shouldn't be touched?
- How to verify complete list?

**Output**: File list with verification method

---

### Step 4: Design Fix Phases (10 minutes)

**Standard Fix Phases**:

```
Phase 0: Plan Preparation
  - Create fix templates
  - Define success criteria
  - Design rollback procedure

Phase 1: Backup
  - Create git branch
  - Backup affected files
  - Verify backup complete

Phase 2: Execute Fix
  - Apply fix to all affected files
  - Verify each file after fix
  - Document any failures

Phase 3: Validate Syntax
  - Run syntax checks
  - Ensure files still valid
  - No new errors introduced

Phase 4: Partial Re-Audit
  - Re-test affected components
  - Compare before/after metrics
  - Verify improvement

Phase 5: Approval & Merge
  - Present before/after report
  - User reviews and approves
  - Merge to main OR rollback
```

**Customize** based on fix complexity.

---

### Step 5: Rollback Strategy (5 minutes)

**Questions to answer**:
- How to undo if fix fails?
- What's the rollback command?
- How to verify rollback worked?
- What state returns to after rollback?

**Output**: Rollback procedure

**Example**:
```markdown
## Rollback Procedure

**If fix fails validation**:
1. `git checkout main -- [affected files]`
2. Verify files restored: `git diff main`
3. Delete fix branch: `git branch -D fix/remove-bom`
4. Confirm import status unchanged

**Rollback Time**: <1 minute
**Rollback Risk**: None (git managed)
```

---

### Step 6: Success Criteria (5 minutes)

**Define specific, measurable criteria**:

```markdown
## Success Criteria

**Must achieve**:
- [ ] Import success rate: 13% → 98%+ (target: 85% improvement)
- [ ] No new syntax errors introduced
- [ ] All 269 files processable by AST
- [ ] Git diff shows only BOM removal (no code changes)

**Must NOT happen**:
- [ ] Any file becomes unreadable
- [ ] Any working file breaks
- [ ] Any code logic changes
```

---

### Step 7: Create Fix Plan Document (5 minutes)

**Use**: `templates/fix-plan-template.md`

**Required sections**:
- Issue summary
- Root cause analysis
- Solution design
- Affected files (exact list)
- Fix phases (step by step)
- Rollback procedure
- Success criteria
- Approval section

**Validation**:
- [ ] Issue clearly defined
- [ ] Solution addresses root cause
- [ ] All affected files identified
- [ ] Rollback procedure tested (mentally)
- [ ] Success criteria measurable
- [ ] No ambiguous steps

---

## Fix Planning Patterns

### Pattern 1: Bulk Correction (Same fix, many files)

**Example**: Remove BOM from 269 files

**Approach**:
- Automated script
- Process all files
- Validate each one
- Report successes/failures

**Duration**: Usually quick (minutes)

---

### Pattern 2: Integration Fix (Connect components)

**Example**: Wire 41 working files to server

**Approach**:
- Identify connection points
- Add import statements
- Update initialization
- Validate integration

**Duration**: Medium (30-60 minutes)

---

### Pattern 3: Structural Fix (Refactoring)

**Example**: Reorganize module structure

**Approach**:
- Plan new structure
- Move files incrementally
- Update imports after each move
- Validate at each step

**Duration**: Long (hours)

---

## Anti-Patterns to Avoid

### Bad Plan 1: "Let's Try This"

No clear solution → improvisation → unpredictable results

**Better**: Research solutions, pick best, plan steps

### Bad Plan 2: Fix Everything

Bundling 5 different issues → can't tell what fixed what

**Better**: One issue per fix cycle

### Bad Plan 3: No Rollback Plan

"If it fails, we'll figure it out" → panic mode later

**Better**: Rollback designed upfront, tested mentally

### Bad Plan 4: Vague Success

"Fix looks good" → subjective judgment

**Better**: Specific metrics (import rate 13% → 98%)

---

## Validation Checklist

Before executing your fix plan:

- [ ] Issue clearly defined
- [ ] Root cause identified
- [ ] Solution designed (not just "try stuff")
- [ ] Affected files listed completely
- [ ] Fix phases defined (5-6 phases typical)
- [ ] Rollback procedure ready
- [ ] Success criteria measurable
- [ ] All steps clear and actionable
- [ ] Risk level assessed
- [ ] Approval process defined

**If all checked**: Plan ready to execute  
**If any unchecked**: Refine before starting

---

## Evolution

After completing fixes using this guide:
- Extract patterns (what fix types common)
- Identify anti-patterns (what went wrong)
- Update HOW-TO-RUN-A-FIX.md (guidelines evolve)
- Rarely update this constitution (principles stable)

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

