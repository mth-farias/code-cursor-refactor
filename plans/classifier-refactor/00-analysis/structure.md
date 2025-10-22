# BehaviorClassifier Structure Analysis

**Date**: 2025-10-22  
**Purpose**: Understand current code organization and identify refactoring boundaries

---

## File Overview

| File | Lines | Complexity | Priority | Notes |
|------|-------|------------|----------|-------|
| `_classifier.py` | 1,370 | High | P1 | Core algorithms, NumPy-heavy |
| `_qc_error_flag.py` | 1,372 | High | P2 | Quality control logic |
| `_main.py` | 1,254 | High | P3 | Orchestration |
| `_utils.py` | 1,001 | Medium | P0 | Foundation (others depend on it) |
| `_colab.py` | 649 | Medium | P4 | Colab adapter |
| `behaviorclassifier_run.py` | 157 | Low | P5 | Runner script |
| `__init__.py` | 67 | Low | - | Lazy exports (keep as-is) |
| **Total** | **5,870** | - | - | 4x larger than Config |

---

## Module Breakdown

### 1. `_utils.py` (1,001 lines)

**Purpose**: Shared utilities used by all other modules

**Sections** (to be analyzed):
- [ ] Constants and configuration
- [ ] Label management utilities
- [ ] Onset detection functions
- [ ] Data validation helpers
- [ ] Common transformations

**Refactoring Strategy**: TBD after deep analysis

**Dependencies**: 
- Imports: Config.EXPERIMENT, numpy, pandas
- Used by: _classifier, _qc_error_flag, _main

---

### 2. `_classifier.py` (1,370 lines)

**Purpose**: Core behavior classification algorithms

**Sections** (to be analyzed):
- [ ] Constants and thresholds (CELL 02)
- [ ] Classification kernels
- [ ] Denoising algorithms
- [ ] Layer1/Layer2 processing
- [ ] Resistant behavior detection
- [ ] Speed-based classification

**Refactoring Strategy**: TBD after deep analysis

**Dependencies**:
- Imports: Config.EXPERIMENT, BC_UTILS, numpy, pandas, numba (optional)
- Used by: _main

**Performance Critical**: ⚠️ YES (NumPy operations, optional JIT)

---

### 3. `_qc_error_flag.py` (1,372 lines)

**Purpose**: Quality control, error detection, and flagging logic

**Sections** (to be analyzed):
- [ ] Error detection rules
- [ ] Flag detection rules
- [ ] QC thresholds
- [ ] Report generation
- [ ] File I/O for QC outputs

**Refactoring Strategy**: TBD after deep analysis

**Dependencies**:
- Imports: Config.PATH, Config.PARAM, pandas
- Used by: _main

**I/O Heavy**: ⚠️ YES (CSV writes, folder creation)

---

### 4. `_main.py` (1,254 lines)

**Purpose**: Orchestrate full behavior classification pipeline

**Sections** (to be analyzed):
- [ ] Pipeline orchestration
- [ ] File discovery and loading
- [ ] Progress reporting
- [ ] Error handling
- [ ] Output generation

**Refactoring Strategy**: TBD after deep analysis

**Dependencies**:
- Imports: All other modules (_utils, _classifier, _qc_error_flag)
- Used by: External scripts, notebooks

**Orchestration**: ⚠️ Complex coordination logic

---

### 5. `_colab.py` (649 lines)

**Purpose**: Google Colab adapter for Mixed PATH mode

**Sections** (to be analyzed):
- [ ] Drive mounting
- [ ] PATH flipping
- [ ] Batch sync
- [ ] Runtime configuration

**Refactoring Strategy**: TBD (may keep as-is if already focused)

**Dependencies**:
- Imports: Config.PATH
- Used by: Colab notebooks only

---

### 6. `behaviorclassifier_run.py` (157 lines)

**Purpose**: Command-line runner script

**Sections** (to be analyzed):
- [ ] CLI argument parsing
- [ ] Runner invocation

**Refactoring Strategy**: Likely keep as-is (already small and focused)

---

### 7. `__init__.py` (67 lines)

**Purpose**: Package interface with lazy exports

**Current Structure**:
```python
# Lazy exports via __getattr__ (PEP 562)
BC_COLAB  → _colab.BC_COLAB
BC_MAIN   → _main.BC_MAIN
BC_QC     → _qc_error_flag.BC_QC
BC_UTILS  → _utils.BC_UTILS
BC_CLASSIFIER → _classifier.BC_CLASSIFIER
```

**Refactoring Strategy**: Keep lazy exports, update import paths after refactoring

---

## Initial Observations

### Strengths
✅ Already has modular separation (5 main modules)  
✅ Lazy loading in __init__.py (good pattern)  
✅ CELL-based organization (consistent with Config)  
✅ Public surfaces are MappingProxyType (immutable)

### Issues
⚠️ Large files (1,000+ lines) hard to navigate  
⚠️ Mixed concerns within files (algorithms + I/O + orchestration)  
⚠️ Difficult to test individual components  
⚠️ Some coupling between modules

---

## Natural Boundaries (Preliminary)

### By Concern Type

**Pure Logic** (easy to test):
- Classification algorithms (_classifier.py)
- Utility functions (_utils.py)
- Onset detection
- Label management

**I/O Operations** (needs mocking):
- CSV reading/writing (_qc_error_flag.py, _main.py)
- File discovery (_main.py)
- Folder creation (_qc_error_flag.py)

**Orchestration** (integration focus):
- Pipeline coordination (_main.py)
- Error handling
- Progress reporting

**External Adapters** (keep focused):
- Colab integration (_colab.py)
- CLI runner (behaviorclassifier_run.py)

---

## Proposed Refactoring Priority

### Priority 0: Foundation
**Module**: `_utils.py`  
**Why**: Other modules depend on it  
**Effort**: 3-4 hours  
**Risk**: Medium (used everywhere)

### Priority 1: Core Algorithms
**Module**: `_classifier.py`  
**Why**: Core value, performance-critical  
**Effort**: 4-5 hours  
**Risk**: High (correctness + performance)

### Priority 2: Quality Control
**Module**: `_qc_error_flag.py`  
**Why**: Large, I/O-heavy, independent  
**Effort**: 3-4 hours  
**Risk**: Medium (I/O needs testing)

### Priority 3: Orchestration
**Module**: `_main.py`  
**Why**: Coordinates everything  
**Effort**: 3-4 hours  
**Risk**: High (touches all modules)

### Priority 4: Colab Adapter
**Module**: `_colab.py`  
**Why**: Already focused, optional  
**Effort**: 1-2 hours  
**Risk**: Low (isolated)

### Priority 5: Runner
**Module**: `behaviorclassifier_run.py`  
**Why**: Already small  
**Effort**: Skip or 1 hour  
**Risk**: Very low

---

## Next Steps

1. **Deep dive into `_utils.py`**
   - Map all functions
   - Identify groupings
   - Find dependencies
   - Estimate worker count (5-6 workers?)

2. **Analyze `_classifier.py`**
   - Map algorithm sections
   - Identify performance-critical parts
   - Find natural splits
   - Estimate worker count (6-8 workers?)

3. **Review `_qc_error_flag.py`**
   - Separate logic from I/O
   - Identify validation rules
   - Map report generation
   - Estimate worker count (5-7 workers?)

4. **Study `_main.py`**
   - Understand orchestration flow
   - Identify pipeline stages
   - Map error handling
   - Decide: refactor or keep?

5. **Evaluate `_colab.py`**
   - Check if already well-organized
   - Decide: refactor or keep?

---

## Analysis Status

- [x] High-level file overview
- [x] Line count per file
- [x] Initial priority assessment
- [ ] Deep analysis of _utils.py
- [ ] Deep analysis of _classifier.py
- [ ] Deep analysis of _qc_error_flag.py
- [ ] Deep analysis of _main.py
- [ ] Deep analysis of _colab.py
- [ ] Dependency graph
- [ ] Complexity hotspots

**Next**: Create `dependencies.md` and `complexity-hotspots.md`

