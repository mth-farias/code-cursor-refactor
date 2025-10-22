#%% CELL 00 — HEADER & SCOPE
"""
_path/__init__.py — PATH Coordinator
=====================================

Orchestrates all path workers and assembles the final PATH dictionary.

Architecture:
    8 workers → coordinator → controller → PATH export
    
Workers (8):
    1. roots.py: Environment detection + root resolution
    2. folders.py: 26 folder paths (13 unique, rest derived)
    3. filename_policy.py: 9 suffix constants
    4. name_builders.py: 10 name functions
    5. path_builders.py: 13 path functions
    6. discovery.py: 14 discovery functions
    7. transforms.py: 7 transform utilities
    8. report.py: 4 diagnostic functions
    
Total Exports: 87 (validated)
    - 4 environment detection functions
    - 24 folder paths (1 root + 23 subfolders)
    - 10 suffix/report constants
    - 10 name builders
    - 13 path builders
    - 14 discovery functions
    - 7 transforms
    - 4 diagnostics
    - 1 backward compat alias (filename)
    = 87 unique exports
    
Design:
    - Coordinator receives optional root override
    - Calls workers in dependency order
    - Assembles single immutable PATH dictionary
    - Validates export count (67 expected)
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from types import MappingProxyType
from typing import Optional

# Import all workers
from . import roots
from . import folders
from . import filename_policy
from . import name_builders
from . import path_builders
from . import discovery
from . import transforms
from . import report

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for _path coordinator.

Why Empty?
    Coordinator orchestrates workers (no direct configuration).
    Runtime behavior controlled via configure(root=...) parameter.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure orchestration)

#%% CELL 03 — WORKER ORCHESTRATION

def _assemble_path(root: Optional[Path] = None) -> dict:
    """
    Assemble complete PATH dictionary by orchestrating all workers.
    
    Args:
        root: Optional experiment root override. If None, auto-detect.
        
    Returns:
        Dictionary with 87 path-related exports.
        
    Orchestration Order (respects dependencies):
        1. roots → 4 environment functions
        2. folders → 24 folder paths (needs root)
        3. filename_policy → 10 suffix constants
        4. name_builders → 10 name functions (needs policy)
        5. path_builders → 13 path functions (needs folders + names)
        6. discovery → 14 discovery functions (needs folders + policy + names + paths)
        7. transforms → 7 utilities (needs policy + names + folders)
        8. report → 4 diagnostics (needs folders + policy)
        
    Notes:
        - Each worker returns dict via configure()
        - Coordinator merges all dicts (no key conflicts)
        - Final dict contains 86 raw entries + 1 alias → 87 unique exports
    """
    # --- Phase 1: Root detection ---
    roots_data = roots.configure()
    detect_experiment_root = roots_data["detect_experiment_root"]
    
    # Resolve experiment root (auto-detect or override)
    experiment_root = detect_experiment_root(override=root)
    
    # --- Phase 2: Folder structure ---
    folders_data = folders.configure(root=experiment_root)
    
    # --- Phase 3: Filename policy ---
    policy_data = filename_policy.configure()
    
    # --- Phase 4: Name builders ---
    names_data = name_builders.configure(policy=policy_data)
    
    # --- Phase 5: Path builders ---
    paths_data = path_builders.configure(folders=folders_data, names=names_data)
    
    # --- Phase 6: Discovery functions ---
    discovery_data = discovery.configure(
        folders=folders_data,
        policy=policy_data,
        names=names_data,
        paths=paths_data,
    )
    
    # --- Phase 7: Transform utilities ---
    transforms_data = transforms.configure(
        policy=policy_data,
        names=names_data,
        folders=folders_data,
    )
    
    # --- Phase 8: Diagnostic functions ---
    report_data = report.configure(folders=folders_data, policy=policy_data)
    
    # --- Assemble final PATH dictionary ---
    path_dict = {}
    
    # Add environment detection functions (4)
    path_dict["is_colab"] = roots_data["is_colab"]
    path_dict["is_jupyter"] = roots_data["is_jupyter"]
    path_dict["is_template_mode"] = roots_data["is_template_mode"]
    path_dict["detect_experiment_root"] = roots_data["detect_experiment_root"]
    
    # Add folder paths (26)
    path_dict.update(folders_data)
    
    # Add suffix policy (10: 7 suffixes + 2 reports + KNOWN_SUFFIXES tuple)
    path_dict.update(policy_data)
    
    # Add name builders (10)
    path_dict.update(names_data)
    
    # Add path builders (13)
    path_dict.update(paths_data)
    
    # Add discovery functions (14)
    path_dict.update(discovery_data)
    
    # Add transform utilities (7)
    path_dict.update(transforms_data)
    
    # Add diagnostic functions (4)
    path_dict.update(report_data)
    
    # Add backward compatibility alias
    path_dict["filename"] = names_data["stem_without_suffix"]  # Legacy alias
    
    return path_dict


#%% CELL 04 — CONFIGURE

def configure(root: Optional[Path] = None) -> MappingProxyType:
    """
    Configure and return complete immutable PATH dictionary.
    
    Args:
        root: Optional experiment root override.
              If None, auto-detects based on environment:
                  - Colab: /content/drive/MyDrive/Experiments
                  - Jupyter/Local: {cwd}/Experiments
                  
    Returns:
        MappingProxyType with 87 path-related exports (immutable).
        
    Export Categories:
        - Environment detection: 4 functions
        - Folders: 24 paths
        - Suffix policy: 10 constants
        - Name builders: 10 functions
        - Path builders: 13 functions
        - Discovery: 14 functions
        - Transforms: 7 functions
        - Diagnostics: 4 functions
        - Backward compat: 1 alias (filename)
        
    Validation:
        Asserts 87 exports present (all workers + backward compat).
        
    Notes:
        - Immutable (MappingProxyType prevents modification)
        - All functions are closures (capture root/folders/policy)
        - Safe for module-level import (no side effects)
        
    Examples:
        # Auto-detect root
        PATH = configure()
        
        # Override root
        PATH = configure(root=Path("/custom/experiment/folder"))
        
        # Access exports
        print(PATH["pExperimentalFolder"])
        files = PATH["g_tracked"]()
    """
    path_dict = _assemble_path(root=root)
    
    # Validation: Expect 87 total exports
    # 4 env + 24 folders + 10 policy + 10 names + 13 paths + 14 discovery + 7 transforms + 4 diagnostics + 1 alias
    # = 4 + 24 + 10 + 10 + 13 + 14 + 7 + 4 + 1 = 87
    expected_count = 87
    actual_count = len(path_dict)
    
    assert actual_count == expected_count, (
        f"PATH export count mismatch: expected {expected_count}, got {actual_count}. "
        f"Keys: {sorted(path_dict.keys())}"
    )
    
    # Return immutable proxy
    return MappingProxyType(path_dict)


#%% CELL 05 — EXPORTS

__all__ = ["configure"]
