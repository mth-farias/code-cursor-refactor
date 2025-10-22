# path.py Implementation Plan

**Target**: Refactor `references/original/Config/path.py` → `codes/Config/path.py` + `codes/Config/_path/`  
**Pattern**: Controller + subpackage (following param.py success)  
**Status**: Ready for execution

---

## Executive Summary

**Scope**: Transform 692-line monolithic file into 8 modular workers + 1 controller

**Timeline**: 6.5 hours
- Planning: 1.5h ✅ (Complete)
- Implementation: 4h (Next)
- Validation: 1h

**Risk**: Medium (functions + configuration vs pure data)

**Confidence**: High (clear decisions, proven pattern)

---

## Phase 1: Setup (15 minutes)

### 1.1 Create Feature Branch
```bash
git checkout main
git pull origin main
git checkout -b refactor/path-py
```

### 1.2 Create Subpackage Structure
```bash
mkdir codes/Config/_path
touch codes/Config/_path/__init__.py
touch codes/Config/_path/roots.py
touch codes/Config/_path/folders.py
touch codes/Config/_path/filename_policy.py
touch codes/Config/_path/name_builders.py
touch codes/Config/_path/path_builders.py
touch codes/Config/_path/discovery.py
touch codes/Config/_path/transforms.py
touch codes/Config/_path/report.py
```

### 1.3 Validation
- [ ] Directory `codes/Config/_path/` exists
- [ ] 9 Python files created (8 workers + __init__)
- [ ] Git status shows new files

---

## Phase 2: Implement Workers (3 hours)

**Strategy**: Implement in dependency order, test each independently.

---

### 2.1 Worker: `roots.py` (20 minutes)

**Purpose**: Environment detection + experiment root configuration

**Dependencies**: None

**Exports**: 
- `is_colab()` → bool
- `is_jupyter()` → bool  
- `is_template_mode()` → bool (stub for now)
- `detect_experiment_root()` → Path
- `configure()` → dict with above functions

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Experiment Root Configuration
==============================
Environment detection and experiment folder root resolution.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

#%% CELL 02: Environment Detection

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

def is_template_mode() -> bool:
    """
    Detect if running in GenerateExperiment.ipynb template mode.
    
    Note: Currently stubbed. Implementation deferred to Phase 5.
    """
    return False  # TODO: Implement in Phase 5

#%% CELL 03: Root Detection

def detect_experiment_root() -> Path:
    """
    Auto-detect experiment root based on runtime environment.
    
    Returns:
        Path to experiment folder root.
    """
    if is_colab():
        return Path("/content/drive/MyDrive/Experiments")
    elif is_jupyter():
        return Path.cwd() / "Experiments"
    else:
        # Local Python script or unknown environment
        return Path.cwd() / "Experiments"

#%% CELL 04: Worker API

def configure() -> dict[str, callable | Path]:
    """
    Return environment detection utilities.
    
    Returns:
        Dictionary with detection functions and default root.
    """
    return {
        "is_colab": is_colab,
        "is_jupyter": is_jupyter,
        "is_template_mode": is_template_mode,
        "detect_experiment_root": detect_experiment_root,
    }
```

**Test**:
```python
# Test independently
import sys
sys.path.insert(0, "codes")
from Config._path import roots

result = roots.configure()
print(f"✓ Exported {len(result)} items")
print(f"✓ is_colab: {result['is_colab']()}")
print(f"✓ Default root: {roots.detect_experiment_root()}")
```

**Quality Gate**:
- [ ] 4 functions exported
- [ ] Environment detection works
- [ ] No import errors

---

### 2.2 Worker: `folders.py` (30 minutes)

**Purpose**: All folder path constants

**Dependencies**: None (receives root as argument)

**Exports**: 13 folder paths

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Folder Path Constants
=====================
All experiment subfolder paths relative to experiment root.
"""
from __future__ import annotations

from pathlib import Path

#%% CELL 02: Folder Definitions

def _build_folders(root: Path) -> dict[str, Path]:
    """
    Build all folder paths relative to experiment root.
    
    Args:
        root: Experiment root folder.
    
    Returns:
        Dictionary of 13 folder paths.
    """
    return {
        # Core infrastructure
        "pExperimentalFolder": root,
        "pCodes": root / "codes",
        
        # Data processing pipeline
        "pTracked": root / "tracked",
        "pScored": root / "scored",
        "pDenoised": root / "denoised",      # NEW for refactor
        "pResistant": root / "resistant",    # NEW for refactor
        "pSLEAP": root / "sleap",
        "pPose": root / "pose",
        "pClassified": root / "classified",
        
        # Outputs
        "pFigures": root / "figures",
        "pStatistics": root / "statistics",
        
        # System
        "pLogs": root / "logs",
        "pTemp": root / "temp",
        "pArchive": root / "archive",
    }

#%% CELL 03: Worker API

def configure(root: Path) -> dict[str, Path]:
    """
    Return all folder path constants.
    
    Args:
        root: Experiment root folder.
    
    Returns:
        Dictionary of 13 folder paths.
    """
    folders = _build_folders(root)
    assert len(folders) == 13, f"Expected 13 folders, got {len(folders)}"
    return folders
```

**Test**:
```python
from pathlib import Path
from Config._path import folders

test_root = Path("/test/experiments")
result = folders.configure(test_root)
print(f"✓ Exported {len(result)} folders")
print(f"✓ pTracked: {result['pTracked']}")
print(f"✓ pDenoised: {result['pDenoised']}")  # NEW folder
assert result["pExperimentalFolder"] == test_root
```

**Quality Gate**:
- [ ] 13 folders exported
- [ ] All paths are `Path` objects
- [ ] Includes new folders (pDenoised, pResistant)

---

### 2.3 Worker: `filename_policy.py` (20 minutes)

**Purpose**: Filename suffix constants and registry

**Dependencies**: None

**Exports**: 8 suffixes + KNOWN_SUFFIXES list

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Filename Policy
===============
Standardized filename suffixes and suffix registry.
"""
from __future__ import annotations

#%% CELL 02: Suffix Constants

_SUFFIXES = {
    "SUFFIX_TRACKED": "_tracked",
    "SUFFIX_SCORED": "_scored",
    "SUFFIX_DENOISED": "_denoised",      # NEW for refactor
    "SUFFIX_RESISTANT": "_resistant",    # NEW for refactor
    "SUFFIX_SLEAP": "_sleap",
    "SUFFIX_POSE": "_pose",
    "SUFFIX_CLASSIFIED": "_classified",
    "SUFFIX_STATS": "_stats",
}

#%% CELL 03: Suffix Registry

_KNOWN_SUFFIXES = list(_SUFFIXES.values())

#%% CELL 04: Worker API

def configure() -> dict[str, str | list[str]]:
    """
    Return filename suffix policy.
    
    Returns:
        Dictionary with 8 suffix constants + KNOWN_SUFFIXES list.
    """
    result = {**_SUFFIXES, "KNOWN_SUFFIXES": _KNOWN_SUFFIXES}
    assert len(_SUFFIXES) == 8, f"Expected 8 suffixes, got {len(_SUFFIXES)}"
    return result
```

**Test**:
```python
from Config._path import filename_policy

result = filename_policy.configure()
print(f"✓ Exported {len(result)} items")
print(f"✓ Suffixes: {result['KNOWN_SUFFIXES']}")
assert result["SUFFIX_DENOISED"] == "_denoised"
```

**Quality Gate**:
- [ ] 9 items exported (8 suffixes + 1 list)
- [ ] Includes new suffixes (_denoised, _resistant)
- [ ] KNOWN_SUFFIXES has 8 items

---

### 2.4 Worker: `name_builders.py` (45 minutes)

**Purpose**: Functions to construct filenames

**Dependencies**: `filename_policy` (for suffixes)

**Exports**: 10 name builder functions

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Name Builder Functions
======================
Construct standardized filenames for all file types.
"""
from __future__ import annotations

#%% CELL 02: Core Name Builders

def tracked_name(base_fly: str) -> str:
    """Return filename for tracked CSV."""
    return f"{base_fly}_tracked.csv"

def scored_name(base_fly: str) -> str:
    """Return filename for scored CSV."""
    return f"{base_fly}_scored.csv"

def denoised_name(base_fly: str) -> str:
    """Return filename for denoised CSV."""
    return f"{base_fly}_denoised.csv"

def resistant_name(base_fly: str) -> str:
    """Return filename for resistant behavior CSV."""
    return f"{base_fly}_resistant.csv"

def sleap_name(base_fly: str) -> str:
    """Return filename for SLEAP tracking file."""
    return f"{base_fly}_sleap.csv"

def pose_name(base_fly: str) -> str:
    """Return filename for pose estimation file."""
    return f"{base_fly}_pose.csv"

def classified_name(base_fly: str) -> str:
    """Return filename for classified behavior CSV."""
    return f"{base_fly}_classified.csv"

def stats_name(base_fly: str) -> str:
    """Return filename for statistics file."""
    return f"{base_fly}_stats.csv"

#%% CELL 03: Special Name Builders

def figure_name(base_fly: str, plot_type: str) -> str:
    """Return filename for figure."""
    return f"{base_fly}_{plot_type}.png"

def log_name(timestamp: str) -> str:
    """Return filename for log file."""
    return f"log_{timestamp}.txt"

#%% CELL 04: Worker API

def configure() -> dict[str, callable]:
    """
    Return all name builder functions.
    
    Returns:
        Dictionary of 10 name builder functions.
    """
    builders = {
        "tracked_name": tracked_name,
        "scored_name": scored_name,
        "denoised_name": denoised_name,
        "resistant_name": resistant_name,
        "sleap_name": sleap_name,
        "pose_name": pose_name,
        "classified_name": classified_name,
        "stats_name": stats_name,
        "figure_name": figure_name,
        "log_name": log_name,
    }
    assert len(builders) == 10, f"Expected 10 name builders, got {len(builders)}"
    return builders
```

**Test**:
```python
from Config._path import name_builders

result = name_builders.configure()
print(f"✓ Exported {len(result)} functions")
tracked = result["tracked_name"]("fly1")
print(f"✓ tracked_name('fly1'): {tracked}")
assert tracked == "fly1_tracked.csv"
```

**Quality Gate**:
- [ ] 10 functions exported
- [ ] All return strings
- [ ] Includes new builders (denoised_name, resistant_name)

---

### 2.5 Worker: `path_builders.py` (45 minutes)

**Purpose**: Functions to construct full paths

**Dependencies**: `folders`, `name_builders`

**Exports**: 10 path builder functions

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Path Builder Functions
======================
Construct full file paths for all file types.
"""
from __future__ import annotations

from pathlib import Path

#%% CELL 02: Implementation Note

# NOTE: This worker depends on folders and name_builders being available.
# The __init__.py coordinator will inject them via closures.

#%% CELL 03: Path Builder Factory

def _create_path_builders(folders: dict, names: dict) -> dict[str, callable]:
    """
    Create path builder functions with access to folders and names.
    
    Args:
        folders: Folder path registry.
        names: Name builder function registry.
    
    Returns:
        Dictionary of 10 path builder functions.
    """
    
    def tracked_path(base_fly: str) -> Path:
        """Return full path for tracked CSV."""
        return folders["pTracked"] / names["tracked_name"](base_fly)
    
    def scored_path(base_fly: str) -> Path:
        """Return full path for scored CSV."""
        return folders["pScored"] / names["scored_name"](base_fly)
    
    def denoised_path(base_fly: str) -> Path:
        """Return full path for denoised CSV."""
        return folders["pDenoised"] / names["denoised_name"](base_fly)
    
    def resistant_path(base_fly: str) -> Path:
        """Return full path for resistant CSV."""
        return folders["pResistant"] / names["resistant_name"](base_fly)
    
    def sleap_path(base_fly: str) -> Path:
        """Return full path for SLEAP file."""
        return folders["pSLEAP"] / names["sleap_name"](base_fly)
    
    def pose_path(base_fly: str) -> Path:
        """Return full path for pose file."""
        return folders["pPose"] / names["pose_name"](base_fly)
    
    def classified_path(base_fly: str) -> Path:
        """Return full path for classified CSV."""
        return folders["pClassified"] / names["classified_name"](base_fly)
    
    def stats_path(base_fly: str) -> Path:
        """Return full path for statistics file."""
        return folders["pStatistics"] / names["stats_name"](base_fly)
    
    def figure_path(base_fly: str, plot_type: str) -> Path:
        """Return full path for figure."""
        return folders["pFigures"] / names["figure_name"](base_fly, plot_type)
    
    def log_path(timestamp: str) -> Path:
        """Return full path for log file."""
        return folders["pLogs"] / names["log_name"](timestamp)
    
    return {
        "tracked_path": tracked_path,
        "scored_path": scored_path,
        "denoised_path": denoised_path,
        "resistant_path": resistant_path,
        "sleap_path": sleap_path,
        "pose_path": pose_path,
        "classified_path": classified_path,
        "stats_path": stats_path,
        "figure_path": figure_path,
        "log_path": log_path,
    }

#%% CELL 04: Worker API

def configure(folders: dict, names: dict) -> dict[str, callable]:
    """
    Return all path builder functions.
    
    Args:
        folders: Folder path registry from folders.py.
        names: Name builder registry from name_builders.py.
    
    Returns:
        Dictionary of 10 path builder functions.
    """
    builders = _create_path_builders(folders, names)
    assert len(builders) == 10, f"Expected 10 path builders, got {len(builders)}"
    return builders
```

**Test**:
```python
from pathlib import Path
from Config._path import folders, name_builders, path_builders

test_root = Path("/test")
folder_reg = folders.configure(test_root)
name_reg = name_builders.configure()
result = path_builders.configure(folder_reg, name_reg)

print(f"✓ Exported {len(result)} functions")
tracked = result["tracked_path"]("fly1")
print(f"✓ tracked_path('fly1'): {tracked}")
assert tracked == Path("/test/tracked/fly1_tracked.csv")
```

**Quality Gate**:
- [ ] 10 functions exported
- [ ] All return `Path` objects
- [ ] Paths combine folder + name correctly

---

### 2.6 Worker: `discovery.py` (45 minutes)

**Purpose**: Glob functions to find files

**Dependencies**: `folders`

**Exports**: 10 discovery functions

**Implementation**:
```python
#%% CELL 01: Module Header
"""
File Discovery Functions
========================
Glob-based functions to find experiment files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

#%% CELL 02: Discovery Function Factory

def _create_discovery_functions(folders: dict) -> dict[str, callable]:
    """
    Create discovery functions with access to folders.
    
    Args:
        folders: Folder path registry.
    
    Returns:
        Dictionary of 10 discovery functions.
    """
    
    def g_tracked() -> list[Path]:
        """Find all tracked CSV files."""
        return list(folders["pTracked"].glob("*_tracked.csv"))
    
    def g_scored() -> list[Path]:
        """Find all scored CSV files."""
        return list(folders["pScored"].glob("*_scored.csv"))
    
    def g_denoised() -> list[Path]:
        """Find all denoised CSV files."""
        return list(folders["pDenoised"].glob("*_denoised.csv"))
    
    def g_resistant() -> list[Path]:
        """Find all resistant behavior CSV files."""
        return list(folders["pResistant"].glob("*_resistant.csv"))
    
    def g_sleap() -> list[Path]:
        """Find all SLEAP tracking files."""
        return list(folders["pSLEAP"].glob("*_sleap.csv"))
    
    def g_pose() -> list[Path]:
        """Find all pose estimation files."""
        return list(folders["pPose"].glob("*_pose.csv"))
    
    def g_classified() -> list[Path]:
        """Find all classified behavior CSV files."""
        return list(folders["pClassified"].glob("*_classified.csv"))
    
    def g_all_experiments() -> list[str]:
        """
        Find all unique base_fly names across all tracked files.
        
        Returns:
            List of base_fly names (without suffixes).
        """
        tracked_files = g_tracked()
        base_names = [p.stem.replace("_tracked", "") for p in tracked_files]
        return sorted(set(base_names))
    
    def g_latest_log() -> Optional[Path]:
        """
        Find the most recent log file.
        
        Returns:
            Path to latest log, or None if no logs exist.
        """
        logs = list(folders["pLogs"].glob("log_*.txt"))
        return max(logs, key=lambda p: p.stat().st_mtime) if logs else None
    
    def g_figures_for_fly(base_fly: str) -> list[Path]:
        """
        Find all figures for a given experiment.
        
        Args:
            base_fly: Base experiment name.
        
        Returns:
            List of figure paths for this experiment.
        """
        return list(folders["pFigures"].glob(f"{base_fly}_*.png"))
    
    return {
        "g_tracked": g_tracked,
        "g_scored": g_scored,
        "g_denoised": g_denoised,
        "g_resistant": g_resistant,
        "g_sleap": g_sleap,
        "g_pose": g_pose,
        "g_classified": g_classified,
        "g_all_experiments": g_all_experiments,
        "g_latest_log": g_latest_log,
        "g_figures_for_fly": g_figures_for_fly,
    }

#%% CELL 03: Worker API

def configure(folders: dict) -> dict[str, callable]:
    """
    Return all discovery functions.
    
    Args:
        folders: Folder path registry from folders.py.
    
    Returns:
        Dictionary of 10 discovery functions.
    """
    discovery_fns = _create_discovery_functions(folders)
    assert len(discovery_fns) == 10, f"Expected 10 discovery functions, got {len(discovery_fns)}"
    return discovery_fns
```

**Test**:
```python
# Note: Discovery functions need real folders to work
# Test with mocking or integration tests later
from Config._path import folders, discovery

test_root = Path("/test")
folder_reg = folders.configure(test_root)
result = discovery.configure(folder_reg)

print(f"✓ Exported {len(result)} functions")
print(f"✓ g_tracked function: {result['g_tracked']}")
```

**Quality Gate**:
- [ ] 10 functions exported
- [ ] All are callable
- [ ] Includes new discovery (g_denoised, g_resistant)

---

### 2.7 Worker: `transforms.py` (30 minutes)

**Purpose**: Helper utilities for path manipulation

**Dependencies**: `filename_policy` (for KNOWN_SUFFIXES)

**Exports**: 7 transform functions

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Path Transform Utilities
========================
Helper functions for path parsing and manipulation.
"""
from __future__ import annotations

from pathlib import Path

#%% CELL 02: Transform Functions

def parse_base_fly(filename: str) -> str:
    """
    Extract base_fly name from filename (remove suffix).
    
    Args:
        filename: File name with suffix (e.g., "fly1_tracked.csv").
    
    Returns:
        Base fly name (e.g., "fly1").
    """
    # Known suffixes from filename_policy
    suffixes = ["_tracked", "_scored", "_denoised", "_resistant",
                "_sleap", "_pose", "_classified", "_stats"]
    
    stem = Path(filename).stem
    for suffix in suffixes:
        if stem.endswith(suffix):
            return stem[:-len(suffix)]
    return stem

def swap_suffix(path: Path, new_suffix: str) -> Path:
    """
    Change the suffix of a file path.
    
    Args:
        path: Original path (e.g., "fly1_tracked.csv").
        new_suffix: New suffix (e.g., "_scored").
    
    Returns:
        Path with new suffix (e.g., "fly1_scored.csv").
    """
    base_fly = parse_base_fly(path.name)
    return path.parent / f"{base_fly}{new_suffix}.csv"

def siblings(path: Path) -> list[Path]:
    """
    Find all related files (same base_fly, different suffixes).
    
    Args:
        path: Path to a file (e.g., "fly1_tracked.csv").
    
    Returns:
        List of all files with same base_fly.
    """
    base_fly = parse_base_fly(path.name)
    return list(path.parent.glob(f"{base_fly}_*.csv"))

def normalize_path(path: Path) -> Path:
    """Normalize path for OS compatibility."""
    return path.resolve()

def get_relative_path(path: Path, root: Path) -> Path:
    """Get path relative to root."""
    return path.relative_to(root)

def path_exists_safe(path: Path) -> bool:
    """Check if path exists, handling errors gracefully."""
    try:
        return path.exists()
    except (OSError, PermissionError):
        return False

def derive_output_from_input(input_path: Path, output_suffix: str) -> Path:
    """
    Derive output file path from input path by changing suffix.
    
    Args:
        input_path: Input file (e.g., "tracked/fly1_tracked.csv").
        output_suffix: Output suffix (e.g., "_scored").
    
    Returns:
        Output path (e.g., "scored/fly1_scored.csv").
    """
    return swap_suffix(input_path, output_suffix)

#%% CELL 03: Worker API

def configure() -> dict[str, callable]:
    """
    Return all transform utility functions.
    
    Returns:
        Dictionary of 7 transform functions.
    """
    transforms = {
        "parse_base_fly": parse_base_fly,
        "swap_suffix": swap_suffix,
        "siblings": siblings,
        "normalize_path": normalize_path,
        "get_relative_path": get_relative_path,
        "path_exists_safe": path_exists_safe,
        "derive_output_from_input": derive_output_from_input,
    }
    assert len(transforms) == 7, f"Expected 7 transform functions, got {len(transforms)}"
    return transforms
```

**Test**:
```python
from Config._path import transforms

result = transforms.configure()
print(f"✓ Exported {len(result)} functions")

base = result["parse_base_fly"]("fly1_tracked.csv")
print(f"✓ parse_base_fly('fly1_tracked.csv'): {base}")
assert base == "fly1"
```

**Quality Gate**:
- [ ] 7 functions exported
- [ ] parse_base_fly works correctly
- [ ] swap_suffix preserves directory

---

### 2.8 Worker: `report.py` (30 minutes)

**Purpose**: Diagnostic and reporting functions

**Dependencies**: `folders`

**Exports**: 1 report function (others stubbed for Phase 5)

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Diagnostic and Reporting Functions
===================================
Tools for validating path configuration and generating reports.
"""
from __future__ import annotations

from pathlib import Path

#%% CELL 02: Report Function Factory

def _create_report_functions(folders: dict) -> dict[str, callable]:
    """
    Create report functions with access to folders.
    
    Args:
        folders: Folder path registry.
    
    Returns:
        Dictionary with report functions.
    """
    
    def render_path_report() -> str:
        """
        Generate comprehensive path configuration report.
        
        Returns:
            Formatted report string.
        """
        lines = [
            "PATH CONFIGURATION REPORT",
            "=" * 40,
            f"\nExperiment Root: {folders['pExperimentalFolder']}",
            "\nFolders:",
        ]
        
        for key, path in sorted(folders.items()):
            if key != "pExperimentalFolder":
                exists = "✓" if path.exists() else "✗"
                lines.append(f"  {exists} {key}: {path}")
        
        return "\n".join(lines)
    
    # Stub other functions for Phase 5
    def sanity_check_all_paths() -> dict:
        """Validate all path constants. TODO: Implement in Phase 5."""
        return {"status": "not_implemented"}
    
    def missing_folders() -> list[str]:
        """Report missing folders. TODO: Implement in Phase 5."""
        return []
    
    def build_experiment_manifest() -> dict:
        """List all files by type. TODO: Implement in Phase 5."""
        return {}
    
    return {
        "render_path_report": render_path_report,
        "sanity_check_all_paths": sanity_check_all_paths,
        "missing_folders": missing_folders,
        "build_experiment_manifest": build_experiment_manifest,
    }

#%% CELL 03: Worker API

def configure(folders: dict) -> dict[str, callable]:
    """
    Return all report functions.
    
    Args:
        folders: Folder path registry from folders.py.
    
    Returns:
        Dictionary with report functions.
    """
    return _create_report_functions(folders)
```

**Test**:
```python
from pathlib import Path
from Config._path import folders, report

test_root = Path("/test")
folder_reg = folders.configure(test_root)
result = report.configure(folder_reg)

print(f"✓ Exported {len(result)} functions")
print("\n" + result["render_path_report"]())
```

**Quality Gate**:
- [ ] 4 functions exported
- [ ] render_path_report produces output
- [ ] No errors on import

---

### 2.9 Coordinator: `_path/__init__.py` (1 hour)

**Purpose**: Orchestrate all workers and assemble PATH bundle

**Dependencies**: All 8 workers

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Path Configuration Coordinator
===============================
Orchestrates path workers and assembles the PATH configuration bundle.

This module follows the Controller + Subpackage pattern established by
color.py and experiment.py, delegating path component construction to
specialized workers.
"""
from __future__ import annotations

import types
from pathlib import Path
from typing import Optional

#%% CELL 02: Dynamic Worker Import

# Support both direct execution and module import
if __name__ == "__main__":
    # Direct execution (e.g., python -m Config._path)
    from roots import configure as configure_roots
    from folders import configure as configure_folders
    from filename_policy import configure as configure_policy
    from name_builders import configure as configure_names
    from path_builders import configure as configure_paths
    from discovery import configure as configure_discovery
    from transforms import configure as configure_transforms
    from report import configure as configure_report
    from roots import detect_experiment_root
else:
    # Module import (e.g., from Config._path import configure)
    from . import roots as roots_module
    from . import folders as folders_module
    from . import filename_policy as policy_module
    from . import name_builders as names_module
    from . import path_builders as paths_module
    from . import discovery as discovery_module
    from . import transforms as transforms_module
    from . import report as report_module
    
    configure_roots = roots_module.configure
    configure_folders = folders_module.configure
    configure_policy = policy_module.configure
    configure_names = names_module.configure
    configure_paths = paths_module.configure
    configure_discovery = discovery_module.configure
    configure_transforms = transforms_module.configure
    configure_report = report_module.configure
    detect_experiment_root = roots_module.detect_experiment_root

#%% CELL 03: Configuration Assembly

def configure(root: Optional[Path] = None) -> dict:
    """
    Assemble the PATH configuration bundle.
    
    Args:
        root: Optional experiment root override. If None, auto-detect.
    
    Returns:
        Immutable dictionary with ~70 path components:
        - 13 folder paths
        - 9 suffix constants
        - 10 name builder functions
        - 10 path builder functions
        - 10 discovery functions
        - 7 transform functions
        - 4 report functions
        - 4 environment detection functions
    """
    # CELL 03.1: Determine Experiment Root
    experiment_root = root if root is not None else detect_experiment_root()
    
    # CELL 03.2: Delegate to Workers (dependency order)
    roots = configure_roots()
    folders = configure_folders(experiment_root)
    policy = configure_policy()
    names = configure_names()
    paths = configure_paths(folders, names)
    discovery = configure_discovery(folders)
    transforms = configure_transforms()
    reports = configure_report(folders)
    
    # CELL 03.3: Assemble Final Bundle
    bundle = {
        **folders,     # 13 folder paths
        **policy,      # 9 suffix constants
        **names,       # 10 name builders
        **paths,       # 10 path builders
        **discovery,   # 10 discovery functions
        **transforms,  # 7 transforms
        **reports,     # 4 reports
        **roots,       # 4 environment functions
    }
    
    # CELL 03.4: Validate
    expected_count = 13 + 9 + 10 + 10 + 10 + 7 + 4 + 4
    actual_count = len(bundle)
    assert actual_count == expected_count, f"Expected {expected_count} exports, got {actual_count}"
    
    return types.MappingProxyType(bundle)

#%% CELL 04: Module Exports

__all__ = ["configure"]
```

**Test**:
```python
import sys
sys.path.insert(0, "codes")
from Config._path import configure
from pathlib import Path

PATH = configure(Path("/test"))
print(f"✓ PATH bundle has {len(PATH)} exports")
print(f"✓ pTracked: {PATH['pTracked']}")
print(f"✓ tracked_name: {PATH['tracked_name']('fly1')}")
print(f"✓ Immutable: {type(PATH)}")
```

**Quality Gate**:
- [ ] 67 exports (13+9+10+10+10+7+4+4)
- [ ] Bundle is MappingProxyType (immutable)
- [ ] No import errors

---

## Phase 3: Create Controller (45 minutes)

### 3.1 Implement `codes/Config/path.py`

**Purpose**: Public API that exposes PATH bundle + backward compatibility

**Implementation**:
```python
#%% CELL 01: Module Header
"""
Path Configuration
==================
Experiment folder structure, filename policies, and path utilities.

This controller delegates to the _path subpackage, which handles:
- Environment detection and experiment root configuration
- Folder path constants (13 folders)
- Filename suffix policy (8 suffixes)
- Name builders (10 functions)
- Path builders (10 functions)
- Discovery functions (10 glob-based finders)
- Transform utilities (7 helpers)
- Diagnostic reports (4 functions)
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

#%% CELL 02: The Missing Body (Intentional)

# This cell is intentionally empty.
#
# Unlike color.py and experiment.py (which have user-configurable constants),
# path.py has NO module-level constants. The experiment root is determined
# dynamically at runtime via environment detection (Colab, Jupyter, local).
#
# All path configuration is delegated to the _path subpackage, which is
# imported in CELL 03 below.

#%% CELL 03: Delegation to Subpackage

from ._path import configure

# Default configuration (auto-detect environment)
PATH = configure()

#%% CELL 04: Backward Compatibility Layer

# The original path.py exported all constants and functions at module level.
# For backward compatibility, we explode the PATH dict to module-level attributes.

globals().update(PATH)

# Explicit exports (all ~67 items from PATH bundle)
__all__ = list(PATH.keys()) + ["PATH", "configure"]

#%% CELL 05: Public API

# Users can import either:
# 1. Individual items: from Config.path import pTracked, tracked_name
# 2. Full bundle: from Config.path import PATH
# 3. Reconfigure: from Config.path import configure; PATH = configure(custom_root)
```

**Test**:
```python
import sys
sys.path.insert(0, "codes")

# Test backward compat imports
from Config.path import pTracked, tracked_name, g_tracked

print(f"✓ pTracked: {pTracked}")
print(f"✓ tracked_name: {tracked_name('fly1')}")
print(f"✓ g_tracked: {g_tracked}")

# Test bundle import
from Config.path import PATH
print(f"✓ PATH bundle: {len(PATH)} exports")
```

**Quality Gate**:
- [ ] Backward compat imports work
- [ ] PATH bundle accessible
- [ ] configure() can override root
- [ ] No import errors

---

## Phase 4: Integration & Validation (1 hour)

### 4.1 Update `Config/__init__.py`

**Changes**:
```python
from .path import PATH

__all__ = ["EXPERIMENT", "COLOR", "PARAM", "PATH"]
```

**Test**:
```python
from Config import PATH
print(f"✓ PATH exported from Config: {len(PATH)} items")
```

---

### 4.2 Quality Gates (from validation-checklist.md)

Run all 8 quality gates:

1. **Gate 1: Structure Compliance**
   - [ ] 8 workers + 1 coordinator + 1 controller
   - [ ] All use cell markers
   - [ ] All have configure()

2. **Gate 2: Export Completeness**
   - [ ] 67 exports total
   - [ ] All original exports preserved

3. **Gate 3: Type Safety**
   - [ ] Folders are Path objects
   - [ ] Suffixes are strings
   - [ ] Functions are callable

4. **Gate 4: Immutability**
   - [ ] PATH is MappingProxyType

5. **Gate 5: Backward Compatibility**
   - [ ] Old imports still work

6. **Gate 6: Environment Detection**
   - [ ] is_colab() works
   - [ ] is_jupyter() works
   - [ ] Root detection works

7. **Gate 7: Function Testing**
   - [ ] Name builders return correct format
   - [ ] Path builders combine correctly
   - [ ] parse_base_fly works

8. **Gate 8: Documentation**
   - [ ] All workers have docstrings
   - [ ] CELL 02 in path.py is verbose

---

### 4.3 Integration Test

Create temporary test script:

```python
# _test_path_integration.py
import sys
sys.path.insert(0, "codes")
from pathlib import Path

# Test 1: Auto-detect mode
from Config.path import PATH
print(f"✓ Test 1: Auto-detect root = {PATH['pExperimentalFolder']}")

# Test 2: Custom root
from Config.path import configure
PATH2 = configure(Path("/custom/root"))
print(f"✓ Test 2: Custom root = {PATH2['pExperimentalFolder']}")

# Test 3: Backward compat
from Config.path import pTracked, tracked_name
print(f"✓ Test 3: pTracked = {pTracked}")
print(f"✓ Test 3: tracked_name('fly1') = {tracked_name('fly1')}")

# Test 4: Functions work
from Config.path import parse_base_fly, swap_suffix
base = parse_base_fly("fly1_tracked.csv")
print(f"✓ Test 4: parse_base_fly('fly1_tracked.csv') = {base}")

print("\n✅ ALL INTEGRATION TESTS PASSED")
```

---

## Phase 5: Commit & Merge (30 minutes)

### 5.1 Final Validation
- [ ] All quality gates passed
- [ ] Integration test passed
- [ ] No linter errors
- [ ] Git status clean (all changes staged)

### 5.2 Atomic Commit
```bash
git add codes/Config/path.py
git add codes/Config/_path/
git add codes/Config/__init__.py
git commit -m "refactor: Modularize path.py into controller + subpackage pattern"
```

### 5.3 Push & Create PR
```bash
git push origin refactor/path-py
# Create PR on GitHub
```

### 5.4 Merge to Main
```bash
git checkout main
git merge refactor/path-py --no-ff
git push origin main
```

### 5.5 Cleanup
```bash
git branch -d refactor/path-py
git push origin --delete refactor/path-py
rm _test_path_integration.py
```

---

## Success Criteria Checklist

- [ ] **Structure**: 8 workers + 1 coordinator + 1 controller
- [ ] **Exports**: 67 items (folders, suffixes, functions)
- [ ] **Backward Compat**: All original imports work
- [ ] **Quality Gates**: All 8 passed
- [ ] **Integration Test**: Passed
- [ ] **Config Package**: Exports PATH
- [ ] **Git History**: Atomic commit
- [ ] **Documentation**: All functions documented
- [ ] **New Features**: pDenoised, pResistant, and related functions added

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Function signature mismatch | Medium | High | Test each worker independently |
| Environment detection fails | Low | Medium | Test in multiple environments |
| Path separator issues | Low | Medium | Use `pathlib.Path` everywhere |
| Missing backward compat | Medium | High | Explicit test for all old imports |

---

## Post-Refactor Tasks (Phase 5+)

1. **Test GenerateExperiment.ipynb compatibility** (user's final checklist item)
2. **Implement Mixed PATH mode** (if needed)
3. **Add integration tests with real fixtures**
4. **Implement stubbed report functions**
5. **Add path validation diagnostics**

---

**Status**: Ready for execution ✅  
**Next**: Begin Phase 1 (Setup)  
**Estimated Time**: 6.5 hours total

---

**Note**: This plan follows the proven param.py pattern. The main difference is that path.py has functions (not just data), requiring careful testing of function behavior, not just data counts.

