# Config Refactoring Playbook v1.0

**Purpose**: Project-specific patterns and workflow for Config package refactoring

**Status**: Living document (will evolve as we refactor)

---

## 📚 Relationship to REFACTOR_GUIDE.md

**REFACTOR_GUIDE** = Base Standards (What)
- Location: `../../references/original/REFACTOR_GUIDE.md`
- Covers: Core philosophy, cell structure, formatting, anti-patterns
- Status: Authoritative baseline (do not modify)

**This Playbook** = Application Patterns (How)
- Extends REFACTOR_GUIDE with architecture patterns
- Documents proven controller + subpackage approach
- Provides systematic refactoring workflow
- Records decisions made during refactoring

**Integration**: This playbook assumes you've read REFACTOR_GUIDE.md and builds on top of it.

---

## 📖 Documents in This Playbook

### Prerequisites
**Start here**: Read `../../references/original/REFACTOR_GUIDE.md` first!

### Core Playbook Documents

1. **01-architecture-patterns.md** ✅ ESTABLISHED
   - Controller + Subpackage pattern (proven in color.py, experiment.py)
   - configure() delegation pattern
   - Numbered subsections pattern
   - When to use modular vs flat structure

2. **02-refactoring-workflow.md** ⏳ OUTLINE (will refine)
   - 5-phase systematic process
   - Basic structure defined
   - Will add details during param.py refactoring

3. **03-quality-gates.md** ✅ ESTABLISHED
   - Extends REFACTOR_GUIDE checklist
   - Adds pattern compliance checks
   - Testing requirements

4. **04-decision-records/** 📝 ONGOING
   - ADRs documenting major architectural choices
   - Why we chose specific patterns
   - Consequences and trade-offs

---

## 🎯 How to Use This Playbook

### For Refactoring a New Module

1. **Read prerequisites**
   - REFACTOR_GUIDE.md (base standards)
   - This README (overview)
   - 01-architecture-patterns.md (proven patterns)

2. **Analyze the module**
   - How many lines? (< 400 = simple, > 400 = modular)
   - Natural sections? (what are the concerns?)
   - Dependencies? (what does it import/use?)

3. **Follow the workflow**
   - See 02-refactoring-workflow.md
   - Adapt to your specific module
   - Document lessons learned

4. **Check quality gates**
   - Use 03-quality-gates.md checklist
   - All gates must pass before moving on

5. **Update playbook**
   - Add patterns you discover
   - Refine workflow based on experience
   - Document decisions in 04-decision-records/

---

## ✅ What's Established (Proven Patterns)

These patterns are **confirmed working** in color.py and experiment.py:

### Controller + Subpackage Architecture
- **When**: Module > 400 lines OR natural separation of concerns
- **Structure**: Main file (~200-300 lines) + _subpackage/ (4-5 focused modules)
- **Proven**: color.py (350→274 + _color/) and experiment.py (500→230 + _experiment/)

### configure() Delegation
- **Pattern**: Single function call passes all user inputs to subpackage
- **Benefits**: Clean interface, coordinated initialization
- **Proven**: Both color and experiment use this consistently

### Cell Structure
- **From REFACTOR_GUIDE**: Cells 00, 01, 02-03, 04, 05
- **Extension**: Numbered subsections (02.1, 02.2) for long CELL 02
- **Proven**: Both refactored modules use numbered subsections

---

## ⏳ What's To Be Determined

These will be refined during param.py and path.py refactoring:

### Module-Specific Split Strategies
- **param.py**: 714 lines - how to organize? (by file type? concept?)
- **path.py**: 692 lines - how to split? (folders vs files vs helpers?)
- **Decision**: Will be made during analysis phase

### Testing Strategy Details
- **What**: How to validate refactored modules match originals?
- **How**: Import tests? Behavior tests? Integration tests?
- **Decision**: Will develop during first refactoring

### Edge Cases
- **Circular imports**: How to handle? (haven't encountered yet)
- **Performance**: Any impact from modular structure? (seems fine)
- **Backward compatibility**: How to ensure? (use same bundle keys)

---

## 📊 Current Progress

### Completed ✅
- [x] Audited REFACTOR_GUIDE.md
- [x] Analyzed refactored modules (color.py, experiment.py)
- [x] Extracted proven patterns
- [x] Created playbook v1.0 structure

### In Progress ⏳
- [ ] param.py refactoring (next!)
- [ ] Refine workflow based on experience
- [ ] Add testing strategy details

### Future
- [ ] path.py refactoring
- [ ] Playbook v2.0 (expanded with learnings)
- [ ] Pattern template library

---

## 🔄 Playbook Evolution

**Version History**:
- **v1.0** (2025-10-22): Initial version with established patterns
- **v1.1** (TBD): After param.py refactoring (add learnings)
- **v2.0** (TBD): After all Config modules refactored (comprehensive)

**Update Policy**:
- Add patterns as we discover them
- Refine workflow based on real experience
- Document all decisions in ADRs
- Keep CHANGELOG in this README

---

## 📚 Quick Reference

**Key Files**:
- Base standards: `../../references/original/REFACTOR_GUIDE.md`
- Refactored examples: `../Config/color.py`, `../Config/experiment.py`
- Original code: `../../references/original/Config/`
- Planning discussions: `../../plans/config-refactor/`

**Key Patterns**:
- Controller pattern: See 01-architecture-patterns.md
- Quality gates: See 03-quality-gates.md
- Decisions: See 04-decision-records/

---

**Status**: Playbook v1.0 established - ready to refactor param.py!

**Next**: User will explain full context, then we analyze param.py

---

**Last Updated**: 2025-10-22 | **Version**: 1.0

