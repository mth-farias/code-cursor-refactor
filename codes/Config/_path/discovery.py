#%% CELL 00 — HEADER & SCOPE
"""
discovery.py — File Discovery Functions
========================================

Glob-based discovery for canonical artifacts (sorted, deterministic).

Exports:
    configure(folders: dict, policy: dict, names: dict) → dict[str, callable]
    
Discovery Functions (13 total):
    Basic Discovery (7):
        - g_tracked() → list[Path]
        - g_sleap() → list[Path]
        - g_scored() → list[Path]
        - g_pose() → list[Path]
        - g_arenaimg() → list[Path]
        - g_flyvideo() → list[Path]
        - g_cropvideo() → list[Path]
    
    QC Discovery (4):
        - g_flag_scored() → list[Path]
        - g_flag_pose() → list[Path]
        - g_error_tracked_copies() → list[Path]
        - g_error_pose_copies() → list[Path]
    
    Filtered Discovery (2):
        - g_tracked_missing_sleap() → list[Path]
        - g_tracked_missing_scored() → list[Path]
    
    Sibling Resolver (1):
        - siblings(from_path: Path | str) → dict[str, Path | Callable]
        
Notes:
    - Uses non-recursive glob in canonical folders
    - Returns sorted Paths for deterministic behavior
    - No filesystem I/O except glob (safe for testing)
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Callable

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for discovery.py.

Why Empty?
    Discovery functions are pure (no configuration beyond folder paths).
    Dependencies passed via configure() from coordinator.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure functions)

#%% CELL 03 — DISCOVERY FUNCTION FACTORY

def _create_discovery_functions(folders: dict, policy: dict, names: dict, paths: dict) -> dict[str, Callable]:
    """
    Create file discovery functions bound to folder paths and suffix policy.
    
    Args:
        folders: Dictionary with pTracked, pScored, etc. (from folders.py).
        policy: Dictionary with SUFFIX_* (from filename_policy.py).
        names: Dictionary with stem_without_suffix, sleap_name, etc. (from name_builders.py).
        paths: Dictionary with sleap_path, scored_path, etc. (from path_builders.py).
        
    Returns:
        Dictionary with 14 discovery functions.
        
    Notes:
        - Uses closures to capture folder paths and suffixes
        - All functions return sorted lists for determinism
        - glob() is only filesystem I/O (safe, read-only)
    """
    # Extract folders
    pTracked = folders["pTracked"]
    pSleap = folders["pSleap"]
    pScored = folders["pScored"]
    pPose = folders["pPose"]
    pArenaImage = folders["pArenaImage"]
    pFlyVideo = folders["pFlyVideo"]
    pCropVideo = folders["pCropVideo"]
    pFlagScored = folders["pFlagScored"]
    pFlagPose = folders["pFlagPose"]
    pErrorTracked = folders["pErrorTracked"]
    pErrorPose = folders["pErrorPose"]
    
    # Extract suffixes
    SUFFIX_TRACKED = policy["SUFFIX_TRACKED"]
    SUFFIX_SLEAP = policy["SUFFIX_SLEAP"]
    SUFFIX_SCORED = policy["SUFFIX_SCORED"]
    SUFFIX_POSE = policy["SUFFIX_POSE"]
    SUFFIX_ARENAIMG = policy["SUFFIX_ARENAIMG"]
    SUFFIX_FLYVIDEO = policy["SUFFIX_FLYVIDEO"]
    SUFFIX_CROPVIDEO = policy["SUFFIX_CROPVIDEO"]
    
    # Extract name utilities
    stem_without_suffix = names["stem_without_suffix"]
    sleap_name = names["sleap_name"]
    scored_name = names["scored_name"]
    
    # Extract path utilities
    sleap_path = paths["sleap_path"]
    scored_path = paths["scored_path"]
    
    # --- Basic discovery functions ---
    def g_tracked() -> list[Path]:
        """Discover all tracked files in pTracked/."""
        return sorted(pTracked.glob(f"*{SUFFIX_TRACKED}"))
    
    def g_sleap() -> list[Path]:
        """Discover all sleap files in pSleap/."""
        return sorted(pSleap.glob(f"*{SUFFIX_SLEAP}"))
    
    def g_scored() -> list[Path]:
        """Discover all scored files in pScored/."""
        return sorted(pScored.glob(f"*{SUFFIX_SCORED}"))
    
    def g_pose() -> list[Path]:
        """Discover all pose files in pPose/."""
        return sorted(pPose.glob(f"*{SUFFIX_POSE}"))
    
    def g_arenaimg() -> list[Path]:
        """Discover all arena images in pArenaImage/."""
        return sorted(pArenaImage.glob(f"*{SUFFIX_ARENAIMG}"))
    
    def g_flyvideo() -> list[Path]:
        """Discover all fly videos in pFlyVideo/."""
        return sorted(pFlyVideo.glob(f"*{SUFFIX_FLYVIDEO}"))
    
    def g_cropvideo() -> list[Path]:
        """Discover all crop videos in pCropVideo/."""
        return sorted(pCropVideo.glob(f"*{SUFFIX_CROPVIDEO}"))
    
    # --- QC discovery functions ---
    def g_flag_scored() -> list[Path]:
        """Discover flagged scored files in pFlagScored/."""
        return sorted(pFlagScored.glob(f"*{SUFFIX_SCORED}"))
    
    def g_flag_pose() -> list[Path]:
        """Discover flagged pose files in pFlagPose/."""
        return sorted(pFlagPose.glob(f"*{SUFFIX_POSE}"))
    
    def g_error_tracked_copies() -> list[Path]:
        """Discover error tracked copies in pErrorTracked/."""
        return sorted(pErrorTracked.glob(f"*{SUFFIX_TRACKED}"))
    
    def g_error_pose_copies() -> list[Path]:
        """Discover error pose copies in pErrorPose/."""
        return sorted(pErrorPose.glob(f"*{SUFFIX_SLEAP}"))
    
    # --- Filtered discovery functions ---
    def g_tracked_missing_sleap() -> list[Path]:
        """
        Tracked files that have no corresponding Sleap file.
        
        Returns:
            List of tracked Paths missing their sleap companion.
        """
        missing = []
        for fp in g_tracked():
            base = stem_without_suffix(fp.name)
            if not sleap_path(base).exists():
                missing.append(fp)
        return missing
    
    def g_tracked_missing_scored() -> list[Path]:
        """
        Tracked files that have no corresponding Scored file (work to do).
        
        Returns:
            List of tracked Paths missing their scored output.
        """
        missing = []
        for fp in g_tracked():
            base = stem_without_suffix(fp.name)
            if not scored_path(base).exists():
                missing.append(fp)
        return missing
    
    # --- Sibling resolver ---
    def siblings(from_path: Path | str) -> dict[str, Path | Callable]:
        """
        For any policy filename or stem, return all canonical sibling paths.
        
        Args:
            from_path: Any filename, path, or stem with a policy suffix.
            
        Returns:
            Dictionary with sibling path keys:
                - base (str): Base stem
                - tracked, sleap, scored, pose, arenaimg, flyvideo, cropvideo (Path)
                - flag_scored, flag_pose (Path)
                - error_tracked_copy, error_pose_copy (Callable)
                
        Notes:
            - Error copy paths are callables (need original filename preserved)
            - All other paths are concrete Path objects
        """
        name = Path(from_path).name
        base = stem_without_suffix(name)
        
        # Import path builders from outer scope (already have them in paths dict)
        tracked_path_fn = paths["tracked_path"]
        sleap_path_fn = paths["sleap_path"]
        scored_path_fn = paths["scored_path"]
        pose_path_fn = paths["pose_path"]
        arenaimg_path_fn = paths["arenaimg_path"]
        flyvideo_path_fn = paths["flyvideo_path"]
        cropvideo_path_fn = paths["cropvideo_path"]
        flag_scored_path_fn = paths["flag_scored_path"]
        flag_pose_path_fn = paths["flag_pose_path"]
        error_tracked_copy_path_fn = paths["error_tracked_copy_path"]
        error_pose_copy_path_fn = paths["error_pose_copy_path"]
        
        return {
            "base": base,
            "tracked": tracked_path_fn(base),
            "sleap": sleap_path_fn(base),
            "scored": scored_path_fn(base),
            "pose": pose_path_fn(base),
            "arenaimg": arenaimg_path_fn(base),
            "flyvideo": flyvideo_path_fn(base),
            "cropvideo": cropvideo_path_fn(base),
            "flag_scored": flag_scored_path_fn(base),
            "flag_pose": flag_pose_path_fn(base),
            "error_tracked_copy": (lambda orig=name: error_tracked_copy_path_fn(orig)),
            "error_pose_copy": (lambda orig=name: error_pose_copy_path_fn(orig)),
        }
    
    return {
        "g_tracked": g_tracked,
        "g_sleap": g_sleap,
        "g_scored": g_scored,
        "g_pose": g_pose,
        "g_arenaimg": g_arenaimg,
        "g_flyvideo": g_flyvideo,
        "g_cropvideo": g_cropvideo,
        "g_flag_scored": g_flag_scored,
        "g_flag_pose": g_flag_pose,
        "g_error_tracked_copies": g_error_tracked_copies,
        "g_error_pose_copies": g_error_pose_copies,
        "g_tracked_missing_sleap": g_tracked_missing_sleap,
        "g_tracked_missing_scored": g_tracked_missing_scored,
        "siblings": siblings,
    }


#%% CELL 04 — CONFIGURE

def configure(folders: dict, policy: dict, names: dict, paths: dict) -> dict[str, Callable]:
    """
    Generate discovery functions from folders, policy, and utilities.
    
    Args:
        folders: Dictionary with pTracked, pScored, etc. (from folders.py).
        policy: Dictionary with SUFFIX_* (from filename_policy.py).
        names: Dictionary with name builders (from name_builders.py).
        paths: Dictionary with path builders (from path_builders.py).
        
    Returns:
        Dictionary with 14 discovery functions.
        
    Validation:
        Asserts 14 functions returned.
        
    Notes:
        - Called by coordinator with all dependencies
        - Functions are closures capturing paths and suffixes
        - Returns dict (not MappingProxyType) for coordinator assembly
    """
    discovery = _create_discovery_functions(folders, policy, names, paths)
    
    # Validation
    assert len(discovery) == 14, f"Expected 14 discovery functions, got {len(discovery)}"
    
    return discovery


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

