# path.py Refactoring Validation Checklist

**Purpose**: Define quality gates to ensure refactored path.py meets all requirements  
**Usage**: Run before committing; all gates must pass

---

## Quality Gate 1: Structure Compliance

**Requirement**: Follows controller + subpackage pattern from REFACTOR_GUIDE.md

### Checklist
- [ ] Directory `codes/Config/_path/` exists
- [ ] 8 worker files exist (roots, folders, filename_policy, name_builders, path_builders, discovery, transforms, report)
- [ ] 1 coordinator exists (`_path/__init__.py`)
- [ ] 1 controller exists (`codes/Config/path.py`)
- [ ] All files use `#%%` cell markers
- [ ] All files have `from __future__ import annotations`
- [ ] All workers have `configure()` function

### Validation Script
```python
import sys
sys.path.insert(0, "codes")
from pathlib import Path

workers = [
    "roots", "folders", "filename_policy", "name_builders",
    "path_builders", "discovery", "transforms", "report"
]

for worker in workers:
    module = __import__(f"Config._path.{worker}", fromlist=[worker])
    assert hasattr(module, "configure"), f"{worker} missing configure()"
    print(f"✓ {worker}.py has configure()")

print("✅ GATE 1 PASSED: Structure Compliance")
```

---

## Quality Gate 2: Export Completeness

**Requirement**: All original exports preserved (backward compatibility)

### Expected Exports (67 total)

| Category | Count | Items |
|----------|-------|-------|
| **Folders** | 13 | pExperimentalFolder, pCodes, pTracked, pScored, pDenoised, pResistant, pSLEAP, pPose, pClassified, pFigures, pStatistics, pLogs, pTemp, pArchive |
| **Suffixes** | 8 | SUFFIX_TRACKED, SUFFIX_SCORED, SUFFIX_DENOISED, SUFFIX_RESISTANT, SUFFIX_SLEAP, SUFFIX_POSE, SUFFIX_CLASSIFIED, SUFFIX_STATS |
| **Suffix Registry** | 1 | KNOWN_SUFFIXES |
| **Name Builders** | 10 | tracked_name, scored_name, denoised_name, resistant_name, sleap_name, pose_name, classified_name, stats_name, figure_name, log_name |
| **Path Builders** | 10 | tracked_path, scored_path, denoised_path, resistant_path, sleap_path, pose_path, classified_path, stats_path, figure_path, log_path |
| **Discovery** | 10 | g_tracked, g_scored, g_denoised, g_resistant, g_sleap, g_pose, g_classified, g_all_experiments, g_latest_log, g_figures_for_fly |
| **Transforms** | 7 | parse_base_fly, swap_suffix, siblings, normalize_path, get_relative_path, path_exists_safe, derive_output_from_input |
| **Reports** | 4 | render_path_report, sanity_check_all_paths, missing_folders, build_experiment_manifest |
| **Environment** | 4 | is_colab, is_jupyter, is_template_mode, detect_experiment_root |

**Total**: 67 exports

### Checklist
- [ ] PATH bundle has exactly 67 exports
- [ ] All folder constants present
- [ ] All suffix constants present
- [ ] All name builders present
- [ ] All path builders present
- [ ] All discovery functions present
- [ ] All transforms present
- [ ] All reports present
- [ ] All environment functions present

### Validation Script
```python
from Config.path import PATH

expected = [
    # Folders (13)
    "pExperimentalFolder", "pCodes", "pTracked", "pScored", "pDenoised",
    "pResistant", "pSLEAP", "pPose", "pClassified", "pFigures",
    "pStatistics", "pLogs", "pTemp", "pArchive",
    
    # Suffixes (9)
    "SUFFIX_TRACKED", "SUFFIX_SCORED", "SUFFIX_DENOISED", "SUFFIX_RESISTANT",
    "SUFFIX_SLEAP", "SUFFIX_POSE", "SUFFIX_CLASSIFIED", "SUFFIX_STATS",
    "KNOWN_SUFFIXES",
    
    # Name builders (10)
    "tracked_name", "scored_name", "denoised_name", "resistant_name",
    "sleap_name", "pose_name", "classified_name", "stats_name",
    "figure_name", "log_name",
    
    # Path builders (10)
    "tracked_path", "scored_path", "denoised_path", "resistant_path",
    "sleap_path", "pose_path", "classified_path", "stats_path",
    "figure_path", "log_path",
    
    # Discovery (10)
    "g_tracked", "g_scored", "g_denoised", "g_resistant",
    "g_sleap", "g_pose", "g_classified", "g_all_experiments",
    "g_latest_log", "g_figures_for_fly",
    
    # Transforms (7)
    "parse_base_fly", "swap_suffix", "siblings", "normalize_path",
    "get_relative_path", "path_exists_safe", "derive_output_from_input",
    
    # Reports (4)
    "render_path_report", "sanity_check_all_paths", "missing_folders",
    "build_experiment_manifest",
    
    # Environment (4)
    "is_colab", "is_jupyter", "is_template_mode", "detect_experiment_root",
]

missing = [key for key in expected if key not in PATH]
extra = [key for key in PATH if key not in expected]

assert len(missing) == 0, f"Missing exports: {missing}"
assert len(extra) == 0, f"Extra exports: {extra}"
assert len(PATH) == 67, f"Expected 67 exports, got {len(PATH)}"

print(f"✓ All 67 exports present")
print("✅ GATE 2 PASSED: Export Completeness")
```

---

## Quality Gate 3: Type Safety

**Requirement**: All exports have correct types

### Checklist
- [ ] Folder constants are `Path` objects
- [ ] Suffix constants are `str` objects
- [ ] KNOWN_SUFFIXES is a `list`
- [ ] Name builders are callable
- [ ] Path builders are callable
- [ ] Discovery functions are callable
- [ ] Transform functions are callable
- [ ] Report functions are callable
- [ ] Environment functions are callable

### Validation Script
```python
from Config.path import PATH
from pathlib import Path as PathType

# Check folders are Path objects
folders = ["pExperimentalFolder", "pCodes", "pTracked", "pScored",
           "pDenoised", "pResistant", "pSLEAP", "pPose", "pClassified",
           "pFigures", "pStatistics", "pLogs", "pTemp", "pArchive"]
for folder in folders:
    assert isinstance(PATH[folder], PathType), f"{folder} is not Path"

print("✓ All 13 folders are Path objects")

# Check suffixes are strings
suffixes = ["SUFFIX_TRACKED", "SUFFIX_SCORED", "SUFFIX_DENOISED",
            "SUFFIX_RESISTANT", "SUFFIX_SLEAP", "SUFFIX_POSE",
            "SUFFIX_CLASSIFIED", "SUFFIX_STATS"]
for suffix in suffixes:
    assert isinstance(PATH[suffix], str), f"{suffix} is not str"

print("✓ All 8 suffixes are strings")

# Check KNOWN_SUFFIXES is list
assert isinstance(PATH["KNOWN_SUFFIXES"], list)
assert len(PATH["KNOWN_SUFFIXES"]) == 8
print("✓ KNOWN_SUFFIXES is list with 8 items")

# Check all functions are callable
functions = [
    # Name builders
    "tracked_name", "scored_name", "denoised_name", "resistant_name",
    "sleap_name", "pose_name", "classified_name", "stats_name",
    "figure_name", "log_name",
    # Path builders
    "tracked_path", "scored_path", "denoised_path", "resistant_path",
    "sleap_path", "pose_path", "classified_path", "stats_path",
    "figure_path", "log_path",
    # Discovery
    "g_tracked", "g_scored", "g_denoised", "g_resistant",
    "g_sleap", "g_pose", "g_classified", "g_all_experiments",
    "g_latest_log", "g_figures_for_fly",
    # Transforms
    "parse_base_fly", "swap_suffix", "siblings", "normalize_path",
    "get_relative_path", "path_exists_safe", "derive_output_from_input",
    # Reports
    "render_path_report", "sanity_check_all_paths", "missing_folders",
    "build_experiment_manifest",
    # Environment
    "is_colab", "is_jupyter", "is_template_mode", "detect_experiment_root",
]

for func in functions:
    assert callable(PATH[func]), f"{func} is not callable"

print(f"✓ All {len(functions)} functions are callable")
print("✅ GATE 3 PASSED: Type Safety")
```

---

## Quality Gate 4: Immutability

**Requirement**: PATH bundle is read-only (MappingProxyType)

### Checklist
- [ ] PATH is `types.MappingProxyType`
- [ ] PATH cannot be modified

### Validation Script
```python
import types
from Config.path import PATH

assert isinstance(PATH, types.MappingProxyType), "PATH is not immutable"

# Try to modify (should fail)
try:
    PATH["new_key"] = "value"
    assert False, "PATH was modified (should be immutable)"
except TypeError:
    print("✓ PATH is immutable (cannot add keys)")

try:
    PATH["pTracked"] = "/new/path"
    assert False, "PATH was modified (should be immutable)"
except TypeError:
    print("✓ PATH is immutable (cannot change values)")

print("✅ GATE 4 PASSED: Immutability")
```

---

## Quality Gate 5: Backward Compatibility

**Requirement**: All original import patterns still work

### Checklist
- [ ] Can import individual folder constants
- [ ] Can import individual suffix constants
- [ ] Can import individual functions
- [ ] Can import PATH bundle
- [ ] Can import from `Config.path`
- [ ] Can import from `Config`

### Validation Script
```python
# Test 1: Individual folder imports
from Config.path import pTracked, pScored, pDenoised
assert pTracked.name == "tracked"
print("✓ Can import individual folders")

# Test 2: Individual suffix imports
from Config.path import SUFFIX_TRACKED, SUFFIX_DENOISED
assert SUFFIX_TRACKED == "_tracked"
print("✓ Can import individual suffixes")

# Test 3: Individual function imports
from Config.path import tracked_name, denoised_path, g_tracked
assert callable(tracked_name)
assert callable(denoised_path)
assert callable(g_tracked)
print("✓ Can import individual functions")

# Test 4: Bundle import from path
from Config.path import PATH
assert len(PATH) == 67
print("✓ Can import PATH bundle from Config.path")

# Test 5: Bundle import from Config
from Config import PATH as PATH2
assert len(PATH2) == 67
print("✓ Can import PATH bundle from Config")

# Test 6: Transform functions work
from Config.path import parse_base_fly, swap_suffix
base = parse_base_fly("fly1_tracked.csv")
assert base == "fly1"
print("✓ Transform functions work correctly")

print("✅ GATE 5 PASSED: Backward Compatibility")
```

---

## Quality Gate 6: Environment Detection

**Requirement**: Environment detection works correctly

### Checklist
- [ ] `is_colab()` runs without error
- [ ] `is_jupyter()` runs without error
- [ ] `is_template_mode()` runs without error
- [ ] `detect_experiment_root()` returns Path
- [ ] Root path is reasonable

### Validation Script
```python
from Config.path import PATH, is_colab, is_jupyter, detect_experiment_root
from pathlib import Path as PathType

# Test environment detection functions
colab = PATH["is_colab"]()
jupyter = PATH["is_jupyter"]()
template = PATH["is_template_mode"]()

print(f"✓ is_colab() = {colab}")
print(f"✓ is_jupyter() = {jupyter}")
print(f"✓ is_template_mode() = {template}")

# Test root detection
root = detect_experiment_root()
assert isinstance(root, PathType)
print(f"✓ detect_experiment_root() = {root}")

# Test experiment root is set
assert isinstance(PATH["pExperimentalFolder"], PathType)
print(f"✓ pExperimentalFolder = {PATH['pExperimentalFolder']}")

print("✅ GATE 6 PASSED: Environment Detection")
```

---

## Quality Gate 7: Function Behavior

**Requirement**: All functions produce correct outputs

### Checklist
- [ ] Name builders return correct format
- [ ] Path builders combine folder + name
- [ ] parse_base_fly extracts base correctly
- [ ] swap_suffix changes suffix correctly
- [ ] Discovery functions are callable (actual behavior tested in integration)

### Validation Script
```python
from Config.path import PATH
from pathlib import Path as PathType

# Test name builders
tracked = PATH["tracked_name"]("fly1")
assert tracked == "fly1_tracked.csv", f"Expected 'fly1_tracked.csv', got '{tracked}'"
print("✓ tracked_name('fly1') = fly1_tracked.csv")

denoised = PATH["denoised_name"]("fly1")
assert denoised == "fly1_denoised.csv"
print("✓ denoised_name('fly1') = fly1_denoised.csv")

resistant = PATH["resistant_name"]("fly1")
assert resistant == "fly1_resistant.csv"
print("✓ resistant_name('fly1') = fly1_resistant.csv")

# Test path builders (return Path objects)
tracked_p = PATH["tracked_path"]("fly1")
assert isinstance(tracked_p, PathType)
assert tracked_p.name == "fly1_tracked.csv"
assert "tracked" in str(tracked_p)
print(f"✓ tracked_path('fly1') = {tracked_p}")

denoised_p = PATH["denoised_path"]("fly1")
assert isinstance(denoised_p, PathType)
assert denoised_p.name == "fly1_denoised.csv"
print(f"✓ denoised_path('fly1') = {denoised_p}")

# Test parse_base_fly
base1 = PATH["parse_base_fly"]("fly1_tracked.csv")
assert base1 == "fly1"
print("✓ parse_base_fly('fly1_tracked.csv') = fly1")

base2 = PATH["parse_base_fly"]("experiment_2_denoised.csv")
assert base2 == "experiment_2"
print("✓ parse_base_fly('experiment_2_denoised.csv') = experiment_2")

# Test swap_suffix
new_path = PATH["swap_suffix"](PathType("/data/fly1_tracked.csv"), "_scored")
assert new_path.name == "fly1_scored.csv"
assert new_path.parent == PathType("/data")
print("✓ swap_suffix preserves directory and changes suffix")

# Test render_path_report
report = PATH["render_path_report"]()
assert "PATH CONFIGURATION REPORT" in report
assert "Experiment Root" in report
print("✓ render_path_report produces output")

print("✅ GATE 7 PASSED: Function Behavior")
```

---

## Quality Gate 8: Documentation

**Requirement**: All code is well-documented

### Checklist
- [ ] All workers have module docstrings
- [ ] All functions have docstrings
- [ ] Controller has comprehensive module docstring
- [ ] CELL 02 in path.py has verbose explanation
- [ ] __all__ exports are correct

### Validation Script
```python
import inspect
from Config import path as path_module
from Config._path import (
    roots, folders, filename_policy, name_builders,
    path_builders, discovery, transforms, report
)

workers = [roots, folders, filename_policy, name_builders,
           path_builders, discovery, transforms, report, path_module]

for worker in workers:
    assert worker.__doc__ is not None, f"{worker.__name__} missing module docstring"
    print(f"✓ {worker.__name__} has module docstring")

# Check main controller docstring is verbose
controller_doc = path_module.__doc__
assert len(controller_doc) > 200, "Controller docstring too short"
print("✓ path.py controller has comprehensive docstring")

# Check CELL 02 comment (intentional empty cell)
with open("codes/Config/path.py", "r") as f:
    content = f.read()
    assert "CELL 02" in content
    assert "intentionally empty" in content.lower()
print("✓ CELL 02 has verbose explanation")

# Check __all__ exists
assert hasattr(path_module, "__all__")
assert len(path_module.__all__) >= 67
print(f"✓ __all__ has {len(path_module.__all__)} exports")

print("✅ GATE 8 PASSED: Documentation")
```

---

## Final Integration Test

**Purpose**: Test complete workflow end-to-end

### Test Script
```python
# _test_path_complete.py
import sys
sys.path.insert(0, "codes")
from pathlib import Path

print("=" * 50)
print("PATH.PY COMPLETE INTEGRATION TEST")
print("=" * 50)

# Test 1: Default configuration (auto-detect)
from Config.path import PATH
print(f"\n✓ Test 1: Auto-detect mode")
print(f"  Root: {PATH['pExperimentalFolder']}")
print(f"  Tracked folder: {PATH['pTracked']}")

# Test 2: Custom root override
from Config.path import configure
custom_root = Path("/custom/experiment")
PATH2 = configure(custom_root)
assert PATH2["pExperimentalFolder"] == custom_root
assert PATH2["pTracked"] == custom_root / "tracked"
print(f"\n✓ Test 2: Custom root override")
print(f"  Custom root: {PATH2['pExperimentalFolder']}")

# Test 3: Backward compatibility (module-level imports)
from Config.path import (
    pTracked, pDenoised, pResistant,
    SUFFIX_TRACKED, SUFFIX_DENOISED,
    tracked_name, denoised_name, resistant_name,
    tracked_path, denoised_path, resistant_path,
    g_tracked, g_denoised, g_resistant,
    parse_base_fly, swap_suffix
)
print(f"\n✓ Test 3: All backward-compatible imports work")

# Test 4: Name builders
assert tracked_name("fly1") == "fly1_tracked.csv"
assert denoised_name("fly1") == "fly1_denoised.csv"
assert resistant_name("fly1") == "fly1_resistant.csv"
print(f"\n✓ Test 4: Name builders work correctly")

# Test 5: Path builders
tracked_p = tracked_path("fly1")
assert tracked_p.name == "fly1_tracked.csv"
assert "tracked" in str(tracked_p.parent)
print(f"\n✓ Test 5: Path builders work correctly")
print(f"  tracked_path('fly1') = {tracked_p}")

# Test 6: Transform functions
base = parse_base_fly("experiment_2_denoised.csv")
assert base == "experiment_2"
new_p = swap_suffix(Path("/data/fly1_tracked.csv"), "_scored")
assert new_p.name == "fly1_scored.csv"
print(f"\n✓ Test 6: Transform functions work correctly")

# Test 7: Environment detection
from Config.path import is_colab, is_jupyter, detect_experiment_root
colab = is_colab()
jupyter = is_jupyter()
root = detect_experiment_root()
print(f"\n✓ Test 7: Environment detection works")
print(f"  is_colab: {colab}, is_jupyter: {jupyter}")

# Test 8: Report generation
from Config.path import render_path_report
report = render_path_report()
assert "PATH CONFIGURATION REPORT" in report
print(f"\n✓ Test 8: Report generation works")

# Test 9: Config package integration
from Config import PATH as PATH_FROM_CONFIG
assert len(PATH_FROM_CONFIG) == 67
print(f"\n✓ Test 9: Config package exports PATH")

# Test 10: Immutability
import types
assert isinstance(PATH, types.MappingProxyType)
print(f"\n✓ Test 10: PATH is immutable")

print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED")
print("=" * 50)
```

---

## Pre-Commit Checklist

Before running `git commit`:

- [ ] All 8 quality gates passed
- [ ] Integration test passed
- [ ] No linter errors in any file
- [ ] All files have docstrings
- [ ] Git status shows only intended changes
- [ ] pyproject.toml updated (if new dependencies)

---

## Post-Commit Validation

After merging to main:

- [ ] Checkout main branch
- [ ] Import `from Config import PATH`
- [ ] Verify PATH has 67 exports
- [ ] Run quick smoke test
- [ ] Delete feature branch

---

## Rollback Plan

If validation fails:

1. **Do NOT commit**
2. Identify failing gate
3. Fix issue in specific worker
4. Re-run all gates
5. Only commit when all pass

---

**Usage**: Copy validation scripts into `_test_path_gates.py` and run:
```bash
python _test_path_gates.py
```

If all gates pass, proceed with commit. Otherwise, fix issues and re-validate.

---

**Status**: Validation criteria defined ✅  
**Next**: Execute implementation plan

