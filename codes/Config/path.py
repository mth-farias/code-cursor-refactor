#%% CELL 00 — HEADER & SCOPE
"""
path.py — Path Configuration Controller
========================================

Canonical experiment folder map and filename API.

Overview:
    - Declares experiment folder tree (26 folders)
    - Centralizes filename suffix policy (9 constants)
    - Provides helpers to derive related filenames (10 name builders)
    - Provides canonical path builders (13 path builders)
    - Glob discovery for artifacts (14 discovery functions)
    - Transform utilities (7 functions)
    - Diagnostic functions (4 functions)
    - NO filesystem I/O except discovery globs — pure path math

Design:
    - Single source of truth for folder names and file suffixes
    - Keep code packages separate from generated outputs
    - Controller + subpackage pattern (orchestrates _path/ workers)
    
Architecture:
    path.py (controller) → _path/ (coordinator) → 8 workers
    
Public API:
    Primary: PATH dictionary (immutable MappingProxyType)
    Backward Compatible: Module-level exports (all PATH keys)
    
Usage:
    # Recommended (dictionary access)
    from Config.path import PATH
    print(PATH["pExperimentalFolder"])
    files = PATH["g_tracked"]()
    
    # Backward compatible (direct imports)
    from Config.path import pTracked, tracked_name, g_tracked
    
Configuration:
    # Auto-detect experiment root (default)
    from Config.path import PATH
    
    # Override experiment root
    from Config.path import configure
    PATH = configure(root=Path("/custom/experiment/folder"))
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
import importlib
from pathlib import Path
from types import MappingProxyType
from typing import Optional

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for path.py controller.

Why Empty?
    Controller delegates to _path coordinator (no direct logic).
    Configuration via configure(root=...) parameter at import time.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure delegation)

#%% CELL 03 — DELEGATION TO SUBPACKAGE

# Import coordinator
_path = importlib.import_module("._path", package="Config")

# Configure with auto-detected root (can be overridden by importing configure directly)
PATH: MappingProxyType = _path.configure()

#%% CELL 04 — BACKWARD COMPATIBILITY

# Explode PATH dictionary to module-level for backward compatibility
# This allows: from Config.path import pTracked, tracked_name, g_tracked
# (Original code expects module-level exports)
globals().update(PATH)

#%% CELL 05 — CONFIGURE FUNCTION (OPTIONAL OVERRIDE)

def configure(root: Optional[Path] = None) -> MappingProxyType:
    """
    Configure PATH with optional experiment root override.
    
    Args:
        root: Optional experiment root path. If None, auto-detects:
              - Colab: /content/drive/MyDrive/Experiments
              - Jupyter/Local: {cwd}/Experiments
              
    Returns:
        MappingProxyType with 87 path-related exports (immutable).
        
    Usage:
        # Override root
        from Config.path import configure
        PATH = configure(root=Path("/custom/experiment/folder"))
        
        # Access exports
        print(PATH["pExperimentalFolder"])
        files = PATH["g_tracked"]()
        
    Notes:
        - Does not mutate module-level PATH (returns new instance)
        - Use for ephemeral runs (Colab, external drives)
        - All exports are closures (capture root)
    """
    return _path.configure(root=root)


#%% CELL 06 — EXPORTS

# Export PATH + configure function + all individual keys
__all__ = ["PATH", "configure"] + list(PATH.keys())

