#%% CELL 00 — HEADER & SCOPE
"""
transforms.py — Path Transform Utilities
=========================================

Filename transformations and parsing utilities.

Exports:
    configure(policy: dict, names: dict) → dict[str, callable]
    
Transform Functions (7 total):
    Suffix Manipulation:
        - swap_suffix(filename: str, to_suffix: str) → str
        - parse_base_fly(stem: str) → tuple[str, int | None]
    
    Temp File Naming:
        - temp_path(final_path: Path | str) → Path
        - is_temp_path(path: Path | str) → bool
        - final_from_temp(temp_path: Path | str) → Path
    
    Root Rebasing:
        - with_root(new_root: Path | str) → dict[str, Path]
        - _rebase_path(p: Path, new_root: Path) → Path (internal)
        
Notes:
    - Pure functions (no filesystem I/O)
    - Naming only (atomic-write temp convention)
    - Root rebasing for ephemeral runs (Colab, etc.)
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Callable

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for transforms.py.

Why Empty?
    Transform functions are pure utilities (no configuration).
    Dependencies passed via configure() from coordinator.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure utilities)

#%% CELL 03 — TRANSFORM FUNCTION FACTORY

def _create_transform_functions(policy: dict, names: dict) -> dict[str, Callable]:
    """
    Create transform utility functions.
    
    Args:
        policy: Dictionary with SUFFIX_* and KNOWN_SUFFIXES (from filename_policy.py).
        names: Dictionary with stem_without_suffix (from name_builders.py).
        
    Returns:
        Dictionary with 7 transform functions.
        
    Notes:
        - All functions are pure (no filesystem I/O)
        - Temp naming uses '.~tmp' marker convention
        - Root rebasing useful for Colab/external drive runs
    """
    # Extract utilities
    stem_without_suffix = names["stem_without_suffix"]
    
    # --- Suffix manipulation ---
    def swap_suffix(filename: str, to_suffix: str) -> str:
        """
        Replace any known policy suffix with `to_suffix`.
        
        Args:
            filename: Filename or path string with policy suffix.
            to_suffix: New suffix to apply (e.g., '_scored.csv').
            
        Returns:
            Filename with new suffix (e.g., 'BASE_fly1_tracked.csv' → 'BASE_fly1_scored.csv').
            
        Notes:
            - If no known suffix matches, appends to_suffix to stem
            - Uses stem_without_suffix for extraction
        """
        base = stem_without_suffix(filename)
        return f"{base}{to_suffix}"
    
    def parse_base_fly(stem: str) -> tuple[str, int | None]:
        """
        Parse a 'BASE_flyN' stem into (BASE, N).
        
        Args:
            stem: Filename stem (e.g., 'BASE_fly1' or 'BASE_fly1_tracked.csv').
            
        Returns:
            Tuple of (BASE, fly_number) or (stem, None) if no fly suffix.
            
        Examples:
            'BASE_fly1' → ('BASE', 1)
            'BASE_fly12_tracked.csv' → ('BASE_fly12', 12)
            'BASE' → ('BASE', None)
        """
        s = Path(stem).stem
        if "_fly" in s:
            head, tail = s.rsplit("_fly", 1)
            try:
                return head, int(tail)
            except ValueError:
                return s, None
        return s, None
    
    # --- Temp file naming ---
    def temp_path(final_path: str | Path) -> Path:
        """
        Insert '.~tmp' before the file's final suffix for atomic writes.
        
        Args:
            final_path: Final path (e.g., 'a/b.csv').
            
        Returns:
            Temp path with marker (e.g., 'a/b.~tmp.csv').
            
        Notes:
            - Safe for atomic write-then-rename pattern
            - '.~tmp' marker is easily identifiable
        """
        p = Path(final_path)
        if p.suffix:
            return p.with_name(f"{p.stem}.~tmp{p.suffix}")
        return p.with_name(f"{p.name}.~tmp")
    
    def is_temp_path(path: str | Path) -> bool:
        """
        Check if path matches the '.~tmp' temp convention.
        
        Args:
            path: Path to check.
            
        Returns:
            True if path stem ends with '.~tmp'.
        """
        p = Path(path)
        return p.stem.endswith(".~tmp")
    
    def final_from_temp(temp_path_like: str | Path) -> Path:
        """
        Remove the '.~tmp' marker from a temp filename.
        
        Args:
            temp_path_like: Temp path (e.g., 'a/b.~tmp.csv').
            
        Returns:
            Final path (e.g., 'a/b.csv').
            
        Notes:
            - If not a temp path, returns path unchanged
            - Safe to call on any path
        """
        p = Path(temp_path_like)
        if p.stem.endswith(".~tmp"):
            return p.with_name(f"{p.stem[:-5]}{p.suffix}")
        return p
    
    # Note: with_root and _rebase_path need access to experiment root and folder map
    # These will be created later in coordinator with full context
    
    return {
        "swap_suffix": swap_suffix,
        "parse_base_fly": parse_base_fly,
        "temp_path": temp_path,
        "is_temp_path": is_temp_path,
        "final_from_temp": final_from_temp,
    }


#%% CELL 04 — ROOT REBASE UTILITIES

def _create_rebase_functions(folders: dict) -> dict[str, Callable]:
    """
    Create root rebasing functions (requires full folder map).
    
    Args:
        folders: Complete folder map with pExperimentalFolder (from folders.py).
        
    Returns:
        Dictionary with 2 rebase functions.
        
    Notes:
        - Called separately from transforms (needs full PATH context)
        - Useful for Colab runs with different drive mounts
        - Pure path math (no filesystem I/O)
    """
    pExperimentalFolder = folders["pExperimentalFolder"]
    
    # List of keys to rebase
    REBASE_KEYS = (
        "pCodes", "pConfig", "pBehaviorClassifier",
        "pBonfly", "pBonsai", "pFlyHigherProtocol", "pFlyHigherTracker",
        "pRawData",
        "pPostProcessing", "pTracked", "pSleap", "pArenaImage", "pFlyVideo", "pCropVideo",
        "pBehaviorClassification", "pScored", "pPose",
        "pError", "pErrorTracked", "pErrorPose",
        "pFlag", "pFlagScored", "pFlagPose",
    )
    
    def _rebase_path(p: Path, new_root: Path) -> Path:
        """
        Compute new_root / relative_to(pExperimentalFolder) for a path.
        
        Args:
            p: Path under current experiment root.
            new_root: New experiment root.
            
        Returns:
            Rebased path (resolved to absolute).
            
        Notes:
            - If p not under pExperimentalFolder, returns p unchanged
            - Handles path resolution automatically
        """
        try:
            rel = p.relative_to(pExperimentalFolder)
        except Exception:
            return p
        return (Path(new_root) / rel).resolve()
    
    def with_root(new_root: str | Path) -> dict[str, Path]:
        """
        Return folder map rebased under `new_root`.
        
        Args:
            new_root: New experiment root path.
            
        Returns:
            Dictionary with same folder keys, rebased paths.
            
        Notes:
            - Does not mutate globals (pure function)
            - Useful for ephemeral runs (Colab, external drives)
            - Returns new pExperimentalFolder + all rebased folders
            
        Example:
            PATH_COLAB = with_root('/content/drive/MyDrive/ExperimentX')
        """
        new_root = Path(new_root)
        mapping = {"pExperimentalFolder": new_root.resolve()}
        
        for key in REBASE_KEYS:
            if key in folders:
                mapping[key] = _rebase_path(folders[key], new_root)
        
        return mapping
    
    return {
        "_rebase_path": _rebase_path,
        "with_root": with_root,
    }


#%% CELL 05 — CONFIGURE

def configure(policy: dict, names: dict, folders: dict | None = None) -> dict[str, Callable]:
    """
    Generate transform utility functions.
    
    Args:
        policy: Dictionary with SUFFIX_* (from filename_policy.py).
        names: Dictionary with name builders (from name_builders.py).
        folders: Optional full folder map (for rebase functions).
        
    Returns:
        Dictionary with 5-7 transform functions (7 if folders provided).
        
    Validation:
        Asserts 5 or 7 functions returned.
        
    Notes:
        - Basic transforms: 5 functions (swap, parse, temp utilities)
        - With folders: +2 rebase functions (with_root, _rebase_path)
        - Called by coordinator with all dependencies
    """
    transforms = _create_transform_functions(policy, names)
    
    if folders is not None:
        # Add rebase functions if full folder map available
        rebase = _create_rebase_functions(folders)
        transforms.update(rebase)
    
    # Validation
    expected = 7 if folders is not None else 5
    assert len(transforms) == expected, f"Expected {expected} transform functions, got {len(transforms)}"
    
    return transforms


#%% CELL 06 — EXPORTS

__all__ = ["configure"]

