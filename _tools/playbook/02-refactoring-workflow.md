# Refactoring Workflow

**Status**: ⏳ OUTLINE (will refine during param.py refactoring)

**Prerequisites**: Read REFACTOR_GUIDE.md and 01-architecture-patterns.md

---

## Overview

Systematic 5-phase process for refactoring Config modules.

**Philosophy**: Plan → Execute → Validate → Integrate → Reflect

---

## Phase 1: Analysis

**Goal**: Understand the module completely before changing anything

**Actions**:
1. **Read thoroughly** - Understand every section
2. **Identify concerns** - What are the natural divisions?
3. **Document dependencies** - What does it import? What imports it?
4. **Note pain points** - What's confusing? What's too long?
5. **Sketch structure** - If modular, how would you split it?

**Deliverables**:
- Notes document in `plans/config-refactor/0X-module-refactor/analysis.md`
- List of concerns/sections
- Dependencies map
- Proposed structure (modular vs flat)

**Time Estimate**: 30-60 minutes for large modules

**Exit Criteria**:
- [ ] Read entire module
- [ ] Identified all major sections
- [ ] Dependencies documented
- [ ] Structure decision made (modular vs flat)

---

## Phase 2: Planning

**Goal**: Create detailed refactoring plan before touching code

**Actions**:
1. **Define split points** - What goes where? (if modular)
2. **Map public API** - What keys must the bundle have? (no breaking changes!)
3. **Plan subpackages** - How many modules? Names? Responsibilities?
4. **Identify tests** - How will you validate it works?
5. **Review plan** - Get feedback if needed

**Deliverables**:
- Refactoring plan document in `plans/config-refactor/0X-module-refactor/plan.md`
- API compatibility checklist (bundle keys must match original)
- Subpackage structure diagram (if modular)
- Testing strategy

**Time Estimate**: 30-45 minutes

**Exit Criteria**:
- [ ] Split strategy documented
- [ ] Public API mapped (no breaking changes)
- [ ] Subpackage structure defined (if modular)
- [ ] Testing plan ready

---

## Phase 3: Execution

**Goal**: Implement the refactoring following the plan

**Actions** (if modular):
1. **Create subpackage structure** - Directories and __init__.py
2. **Move sections to workers** - Copy code to submodule files
3. **Create configure()** - In __init__.py, coordinate workers
4. **Update controller** - Main file CELL 03 calls configure()
5. **Assemble bundle** - CELL 04 collects results
6. **Run linters** - Fix any formatting issues

**Actions** (if staying flat):
1. **Reorganize cells** - Apply REFACTOR_GUIDE structure
2. **Add numbered subsections** - If CELL 02 is long
3. **Update docstrings** - Follow Google style
4. **Create bundle** - MappingProxyType in CELL 04
5. **Run linters** - Fix formatting

**Deliverables**:
- Refactored module in `codes/Config/`
- Subpackage in `codes/Config/_module/` (if modular)
- Linter-clean code

**Time Estimate**: 2-4 hours (varies by complexity)

**Exit Criteria**:
- [ ] Code follows REFACTOR_GUIDE structure
- [ ] Controller pattern applied (if modular)
- [ ] Linters pass (no errors)
- [ ] Type hints present
- [ ] Docstrings complete

---

## Phase 4: Validation

**Goal**: Verify refactored module works identically to original

**Actions**:
1. **Import test** - Does it import without errors?
2. **API test** - Same bundle keys as original?
3. **Value test** - Do values match original? (spot check)
4. **Integration test** - Works with rest of codebase?
5. **Report test** - Run CELL 05 report if present

**Deliverables**:
- Validation checklist completed
- Any issues fixed
- Documentation of what was tested

**Time Estimate**: 30-60 minutes

**Exit Criteria**:
- [ ] Module imports successfully
- [ ] Bundle has same keys as original
- [ ] Spot-checked values match
- [ ] No broken imports elsewhere
- [ ] Report runs (if present)

---

## Phase 5: Integration & Documentation

**Goal**: Integrate refactored module and document learnings

**Actions**:
1. **Update `__init__.py`** - Export new module if needed
2. **Update references** - Fix any imports elsewhere
3. **Document lessons** - What worked? What didn't?
4. **Update playbook** - Refine workflow based on experience
5. **Commit** - Clear commit message

**Deliverables**:
- Module integrated into Config package
- Config/__init__.py updated
- Lessons learned documented
- Playbook refined (if applicable)
- Git commit

**Time Estimate**: 15-30 minutes

**Exit Criteria**:
- [ ] Module exported from Config
- [ ] No broken dependencies
- [ ] Lessons documented
- [ ] Playbook updated if needed
- [ ] Changes committed

---

## Workflow Summary

```
Phase 1: Analysis (30-60 min)
    ↓
Phase 2: Planning (30-45 min)
    ↓
Phase 3: Execution (2-4 hours)
    ↓
Phase 4: Validation (30-60 min)
    ↓
Phase 5: Integration (15-30 min)

Total: ~4-6 hours per module
```

---

## Decision Points

### When to Use Modular Structure?

**Always modular if**:
- Module > 400 lines
- Clear separation of concerns exists

**Consider modular if**:
- Module 200-400 lines AND getting hard to navigate
- Multiple distinct responsibilities

**Stay flat if**:
- Module < 200 lines
- Single cohesive responsibility

### How Many Submodules?

**Observed pattern**: 4-5 focused modules
- color: 4 modules (colormaps, processing, resolvers, report)
- experiment: 4 modules (periods, stimuli, time, report)

**Guidelines**:
- One per major concern
- Keep focused (single responsibility)
- Include report.py if optional reporting exists

---

## Checklist Template

Use this for each module refactored:

### Module: `________.py`

**Phase 1: Analysis** ⏳
- [ ] Read entire module
- [ ] Identified sections
- [ ] Dependencies mapped
- [ ] Structure decided

**Phase 2: Planning** ⏳
- [ ] Split strategy documented
- [ ] API mapped (no breaking changes)
- [ ] Subpackage structure defined
- [ ] Testing plan ready

**Phase 3: Execution** ⏳
- [ ] Subpackage created (if modular)
- [ ] Code refactored
- [ ] Linters pass
- [ ] Docstrings complete

**Phase 4: Validation** ⏳
- [ ] Import test passed
- [ ] API compatibility verified
- [ ] Values spot-checked
- [ ] Integration tested

**Phase 5: Integration** ⏳
- [ ] __init__.py updated
- [ ] Dependencies fixed
- [ ] Lessons documented
- [ ] Committed

---

## Notes for Refinement

**TODO: Add during param.py refactoring**:
- [ ] Specific analysis techniques (what to look for?)
- [ ] Testing strategy details (how to validate?)
- [ ] Common issues and solutions
- [ ] Time estimates refinement
- [ ] Examples from real refactoring

**TODO: Add during path.py refactoring**:
- [ ] Variations on pattern (different split strategies?)
- [ ] Edge cases encountered
- [ ] Performance considerations

---

**Status**: Basic workflow established, will refine as we use it

**Next**: Apply this workflow to param.py refactoring

**Last Updated**: 2025-10-22

