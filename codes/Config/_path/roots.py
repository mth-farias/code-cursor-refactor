#%% CELL 00 — HEADER & SCOPE
"""
roots.py — Experiment Root Configuration
==========================================

Environment detection and experiment folder root resolution.

Exports:
    is_colab() → bool
    is_jupyter() → bool
    is_template_mode() → bool
    detect_experiment_root(override: Path | None) → Path
    configure() → dict
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Optional

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for roots.py.

Why Empty?
    Environment detection is purely runtime-based (checks for modules,
    kernel state). No build-time constants required.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - runtime detection only)

#%% CELL 03 — ENVIRONMENT DETECTION

def is_colab() -> bool:
    """
    Detect if running in Google Colab environment.
    
    Returns:
        True if google.colab module is available, False otherwise.
    """
    try:
        import google.colab
        return True
    except ImportError:
        return False


def is_jupyter() -> bool:
    """
    Detect if running in Jupyter notebook environment.
    
    Returns:
        True if IPython kernel is active (ZMQInteractiveShell), False otherwise.
    """
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        return shell == "ZMQInteractiveShell"
    except NameError:
        return False


def is_template_mode() -> bool:
    """
    Detect if running in template mode (not yet implemented).
    
    Returns:
        Always False for now (stub for future Mixed PATH mode).
        
    Notes:
        Phase 5 will implement Mixed PATH mode detection.
        Placeholder preserves API stability.
    """
    return False


#%% CELL 04 — ROOT DETECTION

def detect_experiment_root(override: Optional[Path] = None) -> Path:
    """
    Detect or override the experiment root folder.
    
    Args:
        override: Optional explicit root path. If provided, used directly.
        
    Returns:
        Experiment root Path (resolved to absolute).
        
    Detection Logic:
        1. If override provided → use it
        2. If Colab → /content/drive/MyDrive/Experiments
        3. If Jupyter or local → {cwd}/Experiments
        
    Notes:
        - Colab default assumes Google Drive is mounted at standard location
        - Local/Jupyter assumes experiment folder adjacent to working directory
        - Does NOT create directories or check existence (pure path resolution)
    """
    if override is not None:
        return Path(override).resolve()
    
    if is_colab():
        # Colab: Use Google Drive default
        return Path("/content/drive/MyDrive/Experiments").resolve()
    
    # Jupyter or local: Use cwd/Experiments
    return (Path.cwd() / "Experiments").resolve()


#%% CELL 05 — CONFIGURE

def configure() -> dict[str, object]:
    """
    Export environment detection and root resolution functions.
    
    Returns:
        Dictionary with 4 detection functions.
        
    Keys:
        - is_colab: Environment detection function
        - is_jupyter: Environment detection function
        - is_template_mode: Mixed PATH mode detection (stub)
        - detect_experiment_root: Root resolution function
    """
    return {
        "is_colab": is_colab,
        "is_jupyter": is_jupyter,
        "is_template_mode": is_template_mode,
        "detect_experiment_root": detect_experiment_root,
    }


#%% CELL 06 — EXPORTS

__all__ = ["configure", "is_colab", "is_jupyter", "is_template_mode", "detect_experiment_root"]

