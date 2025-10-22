# Architectural Decisions for path.py Refactoring

**Date**: October 22, 2025  
**Context**: Refactoring path.py from monolithic (692 lines) to modular controller + subpackage pattern  
**Reference**: `analysis.md` for detailed breakdown

---

## Decision Summary

| # | Decision | Status | Impact |
|---|----------|--------|--------|
| ADR-005 | Experiment root configuration | ✅ Decided | High |
| ADR-006 | Configure() delegation pattern | ✅ Decided | High |
| ADR-007 | Discovery function testing | ✅ Decided | Medium |
| ADR-008 | Mixed PATH mode timing | ✅ Decided | Low |
| ADR-009 | Environment detection strategy | ✅ Decided | Medium |
| ADR-010 | Backward compatibility guarantee | ✅ Decided | High |

---

## ADR-005: Experiment Root Configuration

### Problem
`pExperimentalFolder` is configurable at runtime. How should users provide this value?

### Options Considered

**Option A: Argument to configure(root: Path)**
```python
from Config.path import configure, PATH
configure(root=Path("/path/to/experiments"))
print(PATH.pExperimentalFolder)
```
- ✅ Explicit control
- ✅ Clear API
- ❌ Breaking change (adds required step)
- ❌ Inconsistent with color/experiment/param (no-arg configure)

**Option B: Global with setter**
```python
from Config import path
path.set_experiment_root(Path("/path/to/experiments"))
from Config.path import PATH
```
- ✅ Flexible
- ❌ Two-step process
- ❌ Mutation feels wrong
- ❌ Easy to forget

**Option C: Environment variable + optional override**
```python
# Default behavior (auto-detect)
from Config.path import PATH
print(PATH.pExperimentalFolder)  # Auto-detected

# Override if needed
from Config import path
path.configure(root=Path("/custom/path"))
from Config.path import PATH  # Re-import
```
- ✅ Works out-of-box (auto-detect)
- ✅ Optional override for advanced users
- ✅ Consistent with other modules (no-arg configure)
- ❌ Slightly more complex

### Decision: **Option C** (Environment variable + optional override)

### Rationale
1. **User Experience**: Most users want auto-detection (Colab, Jupyter, local)
2. **Consistency**: Matches `color.py` and `experiment.py` (no-arg configure)
3. **Flexibility**: Power users can override when needed
4. **Backward Compatible**: Existing code works without changes

### Implementation
```python
# _path/__init__.py
def configure(root: Optional[Path] = None) -> dict:
    """
    Configure path registry.
    
    Args:
        root: Optional experiment root. If None, auto-detect from environment.
    
    Returns:
        Dictionary with all path components.
    """
    from . import roots, folders, ...
    
    # Get experiment root (auto-detect or override)
    experiment_root = root if root is not None else roots.detect_experiment_root()
    
    # Pass root to folder builder
    folder_registry = folders.configure(experiment_root)
    
    # ... rest of configuration
```

---

## ADR-006: Configure() Delegation Pattern

### Problem
Should we use the `configure()` pattern for all workers, even though path.py has functions?

### Options Considered

**Option A: configure() for all workers** (like param.py)
```python
# _path/name_builders.py
def configure() -> dict[str, callable]:
    return {
        "tracked_name": tracked_name,
        "scored_name": scored_name,
        # ... all 10 name builders
    }
```
- ✅ Consistent with param.py
- ✅ Clear structure
- ❌ Unnecessary wrapping (functions are already defined)

**Option B: Direct imports** (no configure)
```python
# _path/__init__.py
from . import name_builders
from . import path_builders
PATH = {
    "tracked_name": name_builders.tracked_name,
    "scored_name": name_builders.scored_name,
    # ...
}
```
- ✅ Simpler
- ✅ No wrapping
- ❌ Inconsistent with param.py pattern

**Option C: Hybrid** (configure for data, direct for functions)
```python
# _path/folders.py (data worker)
def configure(root: Path) -> dict[str, Path]:
    return {...}

# _path/name_builders.py (function worker)
# Just expose functions directly, no configure()
```
- ✅ Pragmatic
- ✅ No unnecessary wrapping
- ❌ Inconsistent pattern within path.py

### Decision: **Option A** (configure() for all workers)

### Rationale
1. **Consistency**: All Config modules use the same pattern
2. **Testability**: Worker `configure()` is a single point to test
3. **Future-Proofing**: If we need to add configuration later, API doesn't change
4. **Minimal Cost**: Wrapping is trivial, pays for itself in consistency

### Implementation
```python
# _path/name_builders.py
def configure() -> dict[str, callable]:
    """Return all name builder functions."""
    return {
        "tracked_name": tracked_name,
        "scored_name": scored_name,
        "denoised_name": denoised_name,
        "resistant_name": resistant_name,
        # ... 6 more
    }

# _path/__init__.py
name_builders = name_builders.configure()
PATH = types.MappingProxyType({
    **folders,
    **name_builders,  # Unpack all name builders
    **path_builders,  # Unpack all path builders
    # ...
})
```

---

## ADR-007: Discovery Function Testing

### Problem
How to test discovery functions (`g_tracked()`, etc.) that depend on file system?

### Options Considered

**Option A: Mock file system**
```python
from unittest.mock import patch, MagicMock

@patch('pathlib.Path.glob')
def test_g_tracked(mock_glob):
    mock_glob.return_value = [Path("fly1_tracked.csv")]
    result = g_tracked()
    assert len(result) == 1
```
- ✅ No real files needed
- ✅ Fast
- ❌ Doesn't test actual glob patterns
- ❌ Fragile (breaks on implementation details)

**Option B: Test fixtures in data/test/**
```python
# Setup: Create test files
test_root = Path("data/test/experiment1")
(test_root / "tracked" / "fly1_tracked.csv").touch()

# Test
result = g_tracked()
assert "fly1_tracked.csv" in [p.name for p in result]
```
- ✅ Tests real behavior
- ✅ Validates glob patterns
- ❌ Requires test data setup
- ❌ Slower

**Option C: Skip unit tests, only integration tests**
```python
# No unit tests for discovery.py
# Only test in full integration tests
```
- ✅ Simple
- ❌ No isolated testing
- ❌ Harder to debug

### Decision: **Option A** (Mock file system) + **Option B** (Integration tests)

### Rationale
1. **Fast Feedback**: Mocked unit tests catch obvious errors
2. **Real Validation**: Integration tests with fixtures catch subtle bugs
3. **Pragmatic**: Use the right tool for each test level
4. **Defer Setup**: Can implement unit tests now, integration tests later

### Implementation
```python
# Unit test (fast, mocked)
def test_g_tracked_calls_glob():
    with patch('pathlib.Path.glob') as mock:
        mock.return_value = [Path("fly1_tracked.csv")]
        result = g_tracked()
        mock.assert_called_once_with("*_tracked.csv")

# Integration test (slower, real files) - DEFER TO PHASE 5
def test_g_tracked_finds_real_files():
    # Requires test fixture setup
    pass
```

---

## ADR-008: Mixed PATH Mode Timing

### Problem
Should we implement Mixed PATH mode (separate input/output roots) now or later?

### Context
From `CONTEXT_NOTES.md`:
> "Mixed PATH mode... input files read from Google Drive, output files written to /content, background process syncs results back to Drive."

### Options Considered

**Option A: Implement now**
- ✅ Complete feature
- ❌ Adds complexity
- ❌ Not currently used
- ❌ Slows down refactoring

**Option B: Defer to Phase 5** (after basic refactoring)
- ✅ Focus on core refactoring first
- ✅ Can test basic functionality sooner
- ✅ Add complexity only when needed
- ❌ May require API changes later

**Option C: Architecture now, implement later**
- ✅ Future-proof API
- ❌ YAGNI (You Ain't Gonna Need It)
- ❌ Premature optimization

### Decision: **Option B** (Defer to Phase 5)

### Rationale
1. **Prioritization**: Core refactoring is more important
2. **Testing**: Need to validate basic functionality first
3. **Risk**: Mixed PATH mode adds significant complexity
4. **Flexibility**: Can add later without breaking changes (just add new functions)

### Implementation
```python
# Phase 4 (this refactoring): Basic path registry only
PATH = {
    "pExperimentalFolder": Path("/path/to/root"),
    "pTracked": Path("/path/to/root/tracked"),
    # ...
}

# Phase 5 (future): Add Mixed PATH mode if needed
PATH_INPUT = {...}   # Google Drive paths
PATH_OUTPUT = {...}  # Local /content paths
```

---

## ADR-009: Environment Detection Strategy

### Problem
How should we detect the runtime environment (Colab, Jupyter, local)?

### Options Considered

**Option A: Check for known modules**
```python
def is_colab() -> bool:
    try:
        import google.colab
        return True
    except ImportError:
        return False
```
- ✅ Simple
- ✅ Reliable
- ❌ Import side effects

**Option B: Check for environment variables**
```python
def is_colab() -> bool:
    return "COLAB_GPU" in os.environ
```
- ✅ No imports
- ❌ Less reliable (env vars can be spoofed)

**Option C: Check for IPython kernel**
```python
def is_jupyter() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        return shell == "ZMQInteractiveShell"
    except NameError:
        return False
```
- ✅ Standard approach
- ❌ Complex

### Decision: **Option A** (Check for known modules) + **Option C** (IPython kernel)

### Rationale
1. **Reliability**: Module presence is definitive
2. **Standard Practice**: Widely used in the community
3. **Original Code**: Already uses this pattern
4. **Low Risk**: These are well-established patterns

### Implementation
```python
# _path/roots.py
def is_colab() -> bool:
    """Detect if running in Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def is_jupyter() -> bool:
    """Detect if running in Jupyter notebook."""
    try:
        shell = get_ipython().__class__.__name__
        return shell == "ZMQInteractiveShell"
    except NameError:
        return False

def detect_experiment_root() -> Path:
    """Auto-detect experiment root based on environment."""
    if is_colab():
        return Path("/content/drive/MyDrive/Experiments")
    elif is_jupyter():
        return Path.cwd() / "Experiments"
    else:
        return Path.cwd() / "Experiments"
```

---

## ADR-010: Backward Compatibility Guarantee

### Problem
Must existing code continue to work after refactoring?

### Options Considered

**Option A: Strict backward compatibility**
```python
# Before (original)
from Config.path import pTracked, tracked_name, g_tracked

# After (refactored) - MUST STILL WORK
from Config.path import pTracked, tracked_name, g_tracked
```
- ✅ Zero user migration
- ✅ Safe refactoring
- ❌ Constrains API design

**Option B: Allow breaking changes**
```python
# After (refactored) - NEW API
from Config.path import PATH
PATH["pTracked"]
PATH["tracked_name"]("fly1")
```
- ✅ Cleaner API
- ❌ Breaks existing code
- ❌ High risk

**Option C: Hybrid (new API + deprecated old API)**
```python
# New API (preferred)
from Config.path import PATH

# Old API (deprecated, still works)
from Config.path import pTracked  # Works but shows deprecation warning
```
- ✅ Smooth migration path
- ❌ More maintenance

### Decision: **Option A** (Strict backward compatibility)

### Rationale
1. **Safety**: Refactoring should not break existing code
2. **User Trust**: Users expect imports to remain stable
3. **Simplicity**: No deprecation warnings to manage
4. **REFACTOR_GUIDE.md**: Emphasizes backward compatibility

### Implementation
```python
# codes/Config/path.py (controller)
from ._path import configure

PATH = configure()

# Backward compatibility: Export all as module-level attributes
pExperimentalFolder = PATH["pExperimentalFolder"]
pTracked = PATH["pTracked"]
pScored = PATH["pScored"]
# ... all 23 folder constants

tracked_name = PATH["tracked_name"]
scored_name = PATH["scored_name"]
# ... all 45 functions

__all__ = ["PATH", "pExperimentalFolder", "pTracked", ...]  # Explicit exports
```

---

## Decision Matrix

| Decision | Priority | Risk | Effort | Status |
|----------|----------|------|--------|--------|
| ADR-005 (Root config) | High | Low | Medium | ✅ |
| ADR-006 (Configure pattern) | High | Low | Low | ✅ |
| ADR-007 (Testing strategy) | Medium | Low | Medium | ✅ |
| ADR-008 (Mixed PATH timing) | Low | Low | Low | ✅ |
| ADR-009 (Environment detection) | Medium | Low | Low | ✅ |
| ADR-010 (Backward compat) | High | High | Medium | ✅ |

---

## Implications for Implementation

### 1. **Worker Dependencies**
```python
# _path/__init__.py
def configure(root: Optional[Path] = None) -> dict:
    experiment_root = root if root else roots.detect_experiment_root()
    
    folders = folders_worker.configure(experiment_root)
    suffixes = suffixes_worker.configure()
    name_builders = names_worker.configure()
    path_builders = paths_worker.configure(folders)
    discovery_fns = discovery_worker.configure(folders)
    transforms = transforms_worker.configure()
    report = report_worker.configure(folders)
    
    return {**folders, **suffixes, **name_builders, ...}
```

### 2. **Testing Order**
1. roots.py (no dependencies)
2. folders.py (depends on roots)
3. filename_policy.py (no dependencies)
4. name_builders.py (depends on filename_policy)
5. path_builders.py (depends on folders + name_builders)
6. discovery.py (depends on folders)
7. transforms.py (depends on filename_policy)
8. report.py (depends on folders)

### 3. **Export Strategy**
```python
# path.py (controller)
PATH = configure()  # Dict with all ~70 exports

# Backward compat: explode dict to module-level
globals().update(PATH)
__all__ = list(PATH.keys()) + ["PATH"]
```

---

## Open Questions

1. **Q: Should `configure()` be idempotent (safe to call multiple times)?**
   - A: Yes, but subsequent calls with different roots should raise an error (once configured, immutable).

2. **Q: Should environment detection be cached?**
   - A: Yes, detect once at module load time.

3. **Q: Should we validate folder existence at configure time?**
   - A: No, defer to runtime (discovery functions handle missing folders gracefully).

---

## Validation Criteria

Each decision will be validated by:

1. ✅ All quality gates pass
2. ✅ Existing imports still work
3. ✅ `PATH` bundle is immutable (MappingProxyType)
4. ✅ Environment detection works in Colab, Jupyter, local
5. ✅ Optional root override works correctly

---

**Status**: All decisions made ✅  
**Next**: Create implementation plan

