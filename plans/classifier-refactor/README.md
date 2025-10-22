# BehaviorClassifier Refactoring Plan

**Status**: Planning Phase  
**Start Date**: 2025-10-22  
**Methodology**: Controller + Subpackage Pattern (proven from Config refactoring)

---

## Overview

Refactor BehaviorClassifier package from monolithic modules to modular, testable structure.

**Scope**: ~5,870 lines across 7 files
- `_classifier.py` (1,370 lines) - Classification algorithms
- `_qc_error_flag.py` (1,372 lines) - Quality control logic
- `_main.py` (1,254 lines) - Main orchestration
- `_utils.py` (1,001 lines) - Shared utilities
- `_colab.py` (649 lines) - Colab adapter
- `behaviorclassifier_run.py` (157 lines) - Runner script
- `__init__.py` (67 lines) - Lazy exports

**Estimated Effort**: 15-20 hours (vs 3 hours for path.py, 4x code size + algorithm complexity)

---

## Why This Refactoring?

### Current Issues
1. **Large Monoliths**: Files exceed 1,000 lines (hard to navigate)
2. **Mixed Concerns**: Algorithms, I/O, and orchestration tangled
3. **Testing Difficulty**: Hard to test individual components
4. **Maintenance Burden**: Changes ripple across large files

### Target Benefits
1. **Modularity**: ~200 line focused modules
2. **Testability**: Independent unit tests per worker
3. **Consistency**: Same pattern as Config package
4. **Maintainability**: Clear separation of concerns
5. **Performance**: No regression (validated via benchmarks)

---

## Methodology (Proven from Config)

### Phase 1: Analysis (2-3 hours)
**Goal**: Understand current structure and identify natural boundaries

**Deliverables**:
- `00-analysis/structure.md` - File breakdown and line counts
- `00-analysis/dependencies.md` - Import graph and coupling
- `00-analysis/complexity-hotspots.md` - Where to focus effort

**Key Questions**:
- What are the natural module boundaries?
- Which parts are pure logic vs I/O?
- What dependencies exist between modules?
- Where are the performance-critical sections?

### Phase 2: Decisions (1-2 hours)
**Goal**: Make architectural decisions with clear rationale

**Deliverables**:
- `01-decisions/ADR-015-to-020.md` - 6+ architectural decisions

**Key ADRs Needed**:
- ADR-015: Algorithm module structure
- ADR-016: QC module organization
- ADR-017: Orchestration pattern
- ADR-018: Utility breakdown strategy
- ADR-019: Testing strategy (algorithms need validation)
- ADR-020: Performance validation approach

### Phase 3: Module Planning (3-4 hours)
**Goal**: Create detailed implementation plans for each module

**Deliverables**:
- `02-classifier/` - _classifier.py refactor plan
- `03-qc/` - _qc_error_flag.py refactor plan
- `04-utils/` - _utils.py refactor plan
- `05-main/` - _main.py refactor plan
- `06-colab/` - _colab.py refactor plan

Each module plan includes:
- Analysis (structure breakdown)
- Decisions (module-specific ADRs)
- Implementation plan (step-by-step with code examples)
- Quality gates (validation checklist)

### Phase 4: Execution (12-15 hours)
**Goal**: Implement refactoring systematically

**Strategy**: One module at a time, fully validated before moving to next

**Order** (by priority/dependency):
1. `_utils.py` → `utils.py` + `_utils/` (foundation, others depend on it)
2. `_classifier.py` → `classifier.py` + `_classifier/` (core algorithms)
3. `_qc_error_flag.py` → `qc.py` + `_qc/` (quality control)
4. `_main.py` → refactor or keep (orchestration)
5. `_colab.py` → refactor or keep (already focused)

### Phase 5: Validation (2-3 hours)
**Goal**: Ensure correctness and no regressions

**Validation**:
- Algorithm correctness (outputs match original)
- Performance benchmarks (no regression)
- Integration tests (full pipeline works)
- Backward compatibility (existing notebooks work)

---

## Success Criteria

### Code Quality
- [ ] Average module size: ~200 lines
- [ ] All workers independently testable
- [ ] Zero linter errors
- [ ] Comprehensive docstrings

### Functional Correctness
- [ ] All algorithm outputs match original (bit-perfect)
- [ ] All quality gates passed
- [ ] No performance regression (within 5%)
- [ ] Backward compatibility (all imports work)

### Process Quality
- [ ] All ADRs documented with rationale
- [ ] Quality gates defined before execution
- [ ] Atomic commits (one per module)
- [ ] Handoff documentation updated

---

## Directory Structure

```
plans/classifier-refactor/
├── README.md                    ← This file
├── 00-analysis/                 ← Phase 1: Understanding
│   ├── structure.md
│   ├── dependencies.md
│   └── complexity-hotspots.md
├── 01-decisions/                ← Phase 2: Architecture
│   ├── README.md
│   └── ADR-015-to-020.md
├── 02-classifier/               ← Phase 3: _classifier.py plan
│   ├── analysis.md
│   ├── decisions.md
│   ├── implementation-plan.md
│   └── quality-gates.md
├── 03-qc/                       ← _qc_error_flag.py plan
│   └── ...
├── 04-utils/                    ← _utils.py plan
│   └── ...
├── 05-main/                     ← _main.py plan
│   └── ...
├── 06-colab/                    ← _colab.py plan
│   └── ...
└── 07-integration/              ← Phase 5: Testing
    └── validation-plan.md
```

---

## Lessons from Config Refactoring

### What Worked
✅ **Comprehensive Planning**: 1.5h planning → 2.5h execution (beat 6.5h estimate!)  
✅ **Quality Gates**: Caught issues before commit  
✅ **Pattern Consistency**: Same structure across all modules  
✅ **Incremental Progress**: One module at a time  
✅ **ADR Discipline**: No second-guessing decisions  

### Adaptations for BehaviorClassifier
🔄 **More Complex**: Algorithms need correctness validation, not just structure  
🔄 **Performance Critical**: Must benchmark against original  
🔄 **Larger Scope**: 4x code size requires proportionally more time  
🔄 **Algorithm Focus**: Pure logic needs careful extraction  

---

## Timeline Estimate

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| **Analysis** | 2-3 hours | Structure, dependencies, hotspots |
| **Decisions** | 1-2 hours | 6+ ADRs |
| **Module Planning** | 3-4 hours | 5 detailed plans |
| **Execution** | 12-15 hours | Refactored modules |
| **Validation** | 2-3 hours | Tests, benchmarks |
| **Total** | **20-27 hours** | Complete refactoring |

**Comparison**:
- param.py: 714 lines, 4 hours (Session 1)
- path.py: 692 lines, 3 hours (Session 3)
- BehaviorClassifier: 5,870 lines, 20-27 hours (4x size, higher complexity)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Algorithm regression | Medium | High | Bit-perfect output validation |
| Performance degradation | Low | High | Benchmark suite before/after |
| Breaking changes | Low | Medium | Strict backward compatibility |
| Scope creep | Medium | Medium | Stick to refactoring only |
| Time overrun | Medium | Low | Incremental progress, can pause |

---

## Resources

### Pattern References
- `codes/Config/param.py` + `_param/` - Pure data module example
- `codes/Config/path.py` + `_path/` - Functions + paths example
- `_tools/playbook/01-architecture-patterns.md` - Pattern documentation

### Planning Templates
- `plans/config-refactor/03-params/` - param.py planning example
- `plans/config-refactor/04-path/` - path.py planning example (1,200 lines!)

### Methodology
- `_tools/playbook/02-refactoring-workflow.md` - Step-by-step process
- `_tools/playbook/03-quality-gates.md` - Validation checklist

---

## Current Status

**Phase**: Initialization  
**Next Action**: Begin Phase 1 (Analysis)  
**Blockers**: None

---

## Getting Started

### Immediate Next Steps

1. **Create analysis documents** (Phase 1)
   ```bash
   mkdir -p plans/classifier-refactor/00-analysis
   # Create structure.md, dependencies.md, complexity-hotspots.md
   ```

2. **Read original modules**
   ```bash
   # Understand what exists
   cat references/original/BehaviorClassifier/_classifier.py
   cat references/original/BehaviorClassifier/_qc_error_flag.py
   cat references/original/BehaviorClassifier/_utils.py
   ```

3. **Map dependencies**
   ```python
   # Understand import graph
   # What depends on what?
   # Which modules are foundational?
   ```

4. **Identify natural boundaries**
   ```
   # Where can we split?
   # What are the concerns?
   # Which parts are coupled?
   ```

---

**Ready to begin!** 🚀

Start with: `plans/classifier-refactor/00-analysis/structure.md`

