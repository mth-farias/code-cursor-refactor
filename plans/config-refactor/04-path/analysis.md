# path.py Structure Analysis

**Source**: `references/original/Config/path.py` (692 lines)  
**Analyzed**: October 22, 2025  
**Purpose**: Understand the monolithic structure before refactoring

---

## Overview Statistics

| Metric | Count | Notes |
|--------|-------|-------|
| **Total Lines** | 692 | Monolithic file |
| **Constants** | ~25 | Paths + suffixes |
| **Functions** | ~50 | Builders + discovery + helpers |
| **Imports** | 4 | os, pathlib, typing, pandas |
| **Dependencies** | 0 | No internal Config dependencies |
| **Exports** | All | Currently implicit (all module-level) |

---

## Section Breakdown

### 1. **Imports** (Lines 1-4)
```python
import os
from pathlib import Path
from typing import Optional
import pandas as pd
```
**Analysis**: Minimal, clean imports. No surprises.

---

### 2. **Experiment Root** (Lines 6-15, ~10 lines)
```python
pExperimentalFolder: Path
# Environment detection logic (Colab, Jupyter, local)
# Configurable via user input
```

**Key Variables**:
- `pExperimentalFolder`: The root path for all experiments (configurable)

**Responsibilities**:
- Detect runtime environment (Colab vs local)
- Allow user configuration
- Serve as anchor for all other paths

**Worker**: `roots.py`

---

### 3. **Core Infrastructure Folders** (Lines 17-40, ~24 lines)

**Constants** (13 folder paths):
```python
pCodes           # Code directory
pTracked         # Tracked CSV files
pScored          # Scored CSV files
pDenoised        # Denoised outputs (NEW for refactor)
pResistant       # Resistant behavior outputs (NEW for refactor)
pSLEAP           # SLEAP tracking files
pPose            # Pose estimation files
pFigures         # Generated figures
pStatistics      # Statistical outputs
pClassified      # Final classified behaviors
pLogs            # Log files
pTemp            # Temporary files
pArchive         # Archived experiments
```

**Pattern**: All relative to `pExperimentalFolder`

**Worker**: `folders.py`

---

### 4. **Filename Suffixes** (Lines 42-55, ~14 lines)

**Constants** (8 suffixes):
```python
SUFFIX_TRACKED = "_tracked"
SUFFIX_SCORED = "_scored"
SUFFIX_DENOISED = "_denoised"         # NEW for refactor
SUFFIX_RESISTANT = "_resistant"       # NEW for refactor
SUFFIX_SLEAP = "_sleap"
SUFFIX_POSE = "_pose"
SUFFIX_CLASSIFIED = "_classified"
SUFFIX_STATS = "_stats"
```

**Registry**:
```python
KNOWN_SUFFIXES = [SUFFIX_TRACKED, SUFFIX_SCORED, ...]
```

**Worker**: `filename_policy.py`

---

### 5. **Name Builders** (Lines 57-150, ~94 lines)

**Functions** (10 name builders):
```python
def tracked_name(base_fly: str) -> str
def scored_name(base_fly: str) -> str
def denoised_name(base_fly: str) -> str       # NEW for refactor
def resistant_name(base_fly: str) -> str      # NEW for refactor
def sleap_name(base_fly: str) -> str
def pose_name(base_fly: str) -> str
def classified_name(base_fly: str) -> str
def stats_name(base_fly: str) -> str
def figure_name(base_fly: str, plot_type: str) -> str
def log_name(timestamp: str) -> str
```

**Pattern**: All return `f"{base_fly}{SUFFIX}.csv"` (except figure/log)

**Worker**: `name_builders.py`

---

### 6. **Path Builders** (Lines 152-280, ~129 lines)

**Functions** (10 path builders):
```python
def tracked_path(base_fly: str) -> Path
def scored_path(base_fly: str) -> Path
def denoised_path(base_fly: str) -> Path      # NEW for refactor
def resistant_path(base_fly: str) -> Path     # NEW for refactor
def sleap_path(base_fly: str) -> Path
def pose_path(base_fly: str) -> Path
def classified_path(base_fly: str) -> Path
def stats_path(base_fly: str) -> Path
def figure_path(base_fly: str, plot_type: str) -> Path
def log_path(timestamp: str) -> Path
```

**Pattern**: All return `folder / name_builder(base_fly)`

**Worker**: `path_builders.py`

---

### 7. **Discovery Functions** (Lines 282-420, ~139 lines)

**Functions** (10 glob functions):
```python
def g_tracked() -> list[Path]                  # Find all *_tracked.csv
def g_scored() -> list[Path]                   # Find all *_scored.csv
def g_denoised() -> list[Path]                 # NEW for refactor
def g_resistant() -> list[Path]                # NEW for refactor
def g_sleap() -> list[Path]
def g_pose() -> list[Path]
def g_classified() -> list[Path]
def g_all_experiments() -> list[str]           # Find all base_fly names
def g_latest_log() -> Optional[Path]           # Find most recent log
def g_figures_for_fly(base_fly: str) -> list[Path]
```

**Pattern**: All use `Path.glob()` on appropriate folder

**Worker**: `discovery.py`

---

### 8. **Helper Functions** (Lines 422-550, ~129 lines)

**Functions** (15 helpers):
```python
def parse_base_fly(filename: str) -> str                # Extract base_fly from filename
def swap_suffix(path: Path, new_suffix: str) -> Path   # Change file suffix
def siblings(path: Path) -> list[Path]                  # Find related files
def ensure_folder(folder: Path) -> None                 # Create folder if missing
def is_colab() -> bool                                  # Detect Colab environment
def is_jupyter() -> bool                                # Detect Jupyter environment
def is_template_mode() -> bool                          # Detect template mode (NEW)
def validate_structure() -> dict                        # Check folder existence
def missing_folders() -> list[str]                      # Report missing folders
def get_relative_path(path: Path) -> Path               # Make path relative to root
def normalize_path(path: Path) -> Path                  # Normalize OS-specific paths
def path_exists_safe(path: Path) -> bool                # Safe path checking
def read_csv_safe(path: Path) -> Optional[pd.DataFrame] # Safe CSV reading
def derive_output_from_input(input_path: Path, output_suffix: str) -> Path
def build_experiment_manifest() -> dict                 # List all files by type
```

**Pattern**: Mixed utilities (parsing, validation, I/O)

**Worker**: `transforms.py` (first 7), `report.py` (last 8)

---

### 9. **Diagnostic Functions** (Lines 552-692, ~141 lines)

**Functions** (8 diagnostics):
```python
def sanity_check_all_paths() -> dict           # Validate all path constants
def report_environment() -> str                # Show detected environment
def list_all_files() -> dict                   # Inventory all experiment files
def check_orphaned_files() -> list[Path]       # Find files without base_fly
def check_incomplete_pipelines() -> list[str]  # Find incomplete processing
def export_path_config() -> dict               # Serialize path registry
def import_path_config(config: dict) -> None   # Deserialize path registry
def render_path_report() -> str                # Full diagnostic report
```

**Pattern**: All for debugging and validation

**Worker**: `report.py`

---

## Dependency Graph

```
roots.py (pExperimentalFolder)
    ↓
folders.py (all folder constants)
    ↓
filename_policy.py (suffixes) ----┐
    ↓                              ↓
name_builders.py              path_builders.py
    ↓                              ↓
discovery.py ← transforms.py ← report.py
```

**Key Insight**: Linear dependency chain! Workers can be implemented in order.

---

## Worker Allocation

| Worker | Lines | Functions | Constants | Complexity |
|--------|-------|-----------|-----------|------------|
| `roots.py` | ~15 | 0 | 1 | Low |
| `folders.py` | ~30 | 0 | 13 | Low |
| `filename_policy.py` | ~20 | 0 | 9 | Low |
| `name_builders.py` | ~100 | 10 | 0 | Low |
| `path_builders.py` | ~130 | 10 | 0 | Low |
| `discovery.py` | ~140 | 10 | 0 | Medium |
| `transforms.py` | ~70 | 7 | 0 | Medium |
| `report.py` | ~150 | 8 | 0 | Medium |
| **Total** | **~655** | **45** | **23** | |

---

## NEW Features for Refactor

Based on `BehaviorScoringRefactor_add_denoise.txt`:

1. **pDenoised**: New folder for denoised outputs
2. **pResistant**: New folder for resistant behavior outputs
3. **SUFFIX_DENOISED**: New suffix "_denoised"
4. **SUFFIX_RESISTANT**: New suffix "_resistant"
5. **denoised_name()**: New name builder
6. **resistant_name()**: New name builder
7. **denoised_path()**: New path builder
8. **resistant_path()**: New path builder
9. **g_denoised()**: New discovery function
10. **g_resistant()**: New discovery function

**Impact**: These fit naturally into existing structure (no architectural changes needed).

---

## Configurable Elements

Unlike param.py (pure data), path.py has **configurable elements**:

### 1. **Runtime Configuration**
- `pExperimentalFolder`: User can override default
- Environment detection: Auto-detect but allow override

### 2. **Template Mode** (NEW for refactor)
- `is_template_mode()`: Detect if running in GenerateExperiment.ipynb
- May skip environment detection when in template mode

### 3. **Mixed PATH Mode** (Future consideration)
- Input root (Google Drive)
- Output root (local /content)
- Currently NOT implemented, but architecture should support it

---

## Testing Strategy

### 1. **Data Workers** (roots, folders, filename_policy)
- Assert expected counts
- Validate data types
- Check no duplicates

### 2. **Function Workers** (name_builders, path_builders)
- Test with known inputs
- Validate output format
- Check suffix correctness

### 3. **Discovery Workers** (discovery)
- Mock file system OR use test fixtures
- Validate glob patterns
- Check return types

### 4. **Helper Workers** (transforms, report)
- Unit test each function
- Mock I/O where needed
- Validate error handling

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Environment detection breaks** | High | Test in Colab, Jupyter, local |
| **Path separators (OS)** | Medium | Use `pathlib.Path` everywhere |
| **Missing folders at runtime** | Low | Discovery functions handle gracefully |
| **Function signature changes** | High | **Must maintain backward compatibility** |
| **Template mode detection** | Low | Defer to Phase 5 (post-refactor) |

---

## Key Decisions to Make

1. **How to handle `pExperimentalFolder` configuration?**
   - Option A: Pass as argument to `configure(root: Path)`
   - Option B: Use global with setter `set_experiment_root(root: Path)`
   - Option C: Environment variable + override

2. **Should `configure()` be called explicitly or implicitly?**
   - Option A: Explicit (user must call before using)
   - Option B: Implicit (auto-detect on first import)

3. **How to test discovery functions?**
   - Option A: Mock file system
   - Option B: Use real test fixtures in `data/test/`
   - Option C: Skip in unit tests, only integration tests

4. **Should we add Mixed PATH mode now or later?**
   - Option A: Now (more complex)
   - Option B: Later (defer to Phase 5)

---

## Conclusion

**Complexity**: Medium (more than param.py due to functions + configuration)

**Confidence**: High (clear structure, linear dependencies)

**Timeline**: 6.5 hours (1.5 planning + 4 implementation + 1 validation)

**Next Step**: Create `decisions.md` to address the 4 key decisions above.

---

**Status**: Analysis complete ✅  
**Next**: Document architectural decisions

