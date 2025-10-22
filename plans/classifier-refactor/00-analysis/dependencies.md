# BehaviorClassifier Dependency Analysis

**Date**: 2025-10-22  
**Purpose**: Map import relationships and identify coupling

---

## Import Graph

```
External Dependencies
    ↓
Config Package (PATH, PARAM, EXPERIMENT)
    ↓
_utils.py (foundation)
    ↓
    ├─→ _classifier.py (algorithms)
    │       ↓
    └─→ _qc_error_flag.py (QC logic)
            ↓
        _main.py (orchestration)
            ↓
        External (notebooks, scripts)

_colab.py (standalone, Config.PATH only)
```

---

## Module Dependencies (Detailed)

### `__init__.py`
**Imports**:
- None (lazy loading)

**Exports**:
- BC_COLAB (from _colab)
- BC_MAIN (from _main)
- BC_QC (from _qc_error_flag)
- BC_UTILS (from _utils)
- BC_CLASSIFIER (from _classifier)

**Coupling**: Low (lazy loader pattern)

---

### `_utils.py`
**Imports**:
- Config.EXPERIMENT
- numpy, pandas
- typing, types

**Used By**:
- _classifier.py ✅
- _qc_error_flag.py ✅
- _main.py ✅

**Exports**: BC_UTILS (MappingProxyType)

**Coupling**: **Foundation** (everything depends on it)

**Refactoring Impact**: HIGH - Must refactor first, changes affect all modules

---

### `_classifier.py`
**Imports**:
- Config.EXPERIMENT
- BehaviorClassifier.BC_UTILS (⚠️ circular if not careful)
- numpy, pandas
- numba (optional)

**Used By**:
- _main.py ✅

**Exports**: BC_CLASSIFIER (MappingProxyType)

**Coupling**: Medium (depends on _utils, used by _main)

**Refactoring Impact**: Medium - Refactor after _utils, before _main

---

### `_qc_error_flag.py`
**Imports**:
- Config.PATH
- Config.PARAM
- pandas

**Used By**:
- _main.py ✅

**Exports**: BC_QC (MappingProxyType)

**Coupling**: Low-Medium (independent of _classifier, used by _main)

**Refactoring Impact**: Medium - Can refactor parallel to _classifier

---

### `_main.py`
**Imports**:
- Config.PATH
- Config.PARAM
- BehaviorClassifier.BC_UTILS
- BehaviorClassifier.BC_CLASSIFIER
- BehaviorClassifier.BC_QC
- pandas, numpy

**Used By**:
- External scripts ✅
- Notebooks ✅

**Exports**: BC_MAIN (MappingProxyType)

**Coupling**: HIGH (depends on all other modules)

**Refactoring Impact**: HIGH - Refactor last, after all dependencies

---

### `_colab.py`
**Imports**:
- Config.PATH
- pandas
- pathlib

**Used By**:
- Colab notebooks only ✅

**Exports**: BC_COLAB (MappingProxyType)

**Coupling**: Low (standalone, Config.PATH only)

**Refactoring Impact**: Low - Can refactor anytime (or skip)

---

### `behaviorclassifier_run.py`
**Imports**:
- BehaviorClassifier.BC_MAIN
- argparse, pathlib

**Used By**:
- Command-line invocation

**Exports**: None (script)

**Coupling**: Low (thin wrapper around BC_MAIN)

**Refactoring Impact**: Very low - Update imports after _main refactor

---

## Dependency Levels

### Level 0: External
- Config.PATH
- Config.PARAM
- Config.EXPERIMENT
- numpy, pandas

### Level 1: Foundation
- `_utils.py` → BC_UTILS

### Level 2: Core Logic
- `_classifier.py` → BC_CLASSIFIER (depends on BC_UTILS)
- `_qc_error_flag.py` → BC_QC (independent)

### Level 3: Orchestration
- `_main.py` → BC_MAIN (depends on BC_UTILS, BC_CLASSIFIER, BC_QC)

### Level 4: Adapters
- `_colab.py` → BC_COLAB (depends on Config.PATH only)
- `behaviorclassifier_run.py` (depends on BC_MAIN)

---

## Circular Dependency Risks

### Current Design
✅ No circular dependencies (good!)

**Why safe**:
- _utils exports BC_UTILS (dict)
- _classifier imports from BehaviorClassifier, gets BC_UTILS
- Lazy loading in __init__.py prevents import cycles

### Refactoring Risks
⚠️ **Watch out for**:
- If workers in _utils/ need to import from _classifier/
- If _classifier/ workers need _utils/ workers (not just public surface)

**Mitigation**:
- Keep clear hierarchy: _utils → _classifier → _qc → _main
- Workers only import from parent public surfaces (BC_UTILS, BC_CLASSIFIER, etc.)
- Never import between subpackages at worker level

---

## Refactoring Order (Based on Dependencies)

1. **_utils.py** → utils.py + _utils/ (foundation)
2. **_classifier.py** → classifier.py + _classifier/ (uses BC_UTILS)
3. **_qc_error_flag.py** → qc.py + _qc/ (parallel to _classifier)
4. **_main.py** → main.py + _main/ (uses BC_UTILS, BC_CLASSIFIER, BC_QC)
5. **_colab.py** → colab.py + _colab/ (optional, standalone)
6. **behaviorclassifier_run.py** → update imports (minimal change)
7. **__init__.py** → update import paths (minimal change)

---

## Import Impact Matrix

| Module | _utils | _classifier | _qc | _main | _colab |
|--------|--------|-------------|-----|-------|--------|
| **_utils** | - | ✅ Used | - | ✅ Used | - |
| **_classifier** | ⚠️ Depends | - | - | ✅ Used | - |
| **_qc** | - | - | - | ✅ Used | - |
| **_main** | ⚠️ Depends | ⚠️ Depends | ⚠️ Depends | - | - |
| **_colab** | - | - | - | - | - |

**Legend**:
- ✅ Used: Module is imported/used by this row
- ⚠️ Depends: This module depends on column module
- -: No relationship

---

## Critical Path

```
Config.EXPERIMENT
    ↓
_utils.py (60+ utility functions)
    ↓
    ├─→ _classifier.py (classification algorithms)
    │       ↓
    └─────→ _main.py (pipeline orchestration)
                ↓
            External usage
```

**Bottleneck**: _utils.py must be refactored first

---

## Analysis Status

- [x] High-level import graph
- [x] Per-module dependency analysis
- [x] Dependency levels identified
- [x] Circular dependency check
- [x] Refactoring order determined
- [ ] Detailed function-level dependencies
- [ ] Performance-critical import paths
- [ ] External dependency audit

**Next**: Create `complexity-hotspots.md`

