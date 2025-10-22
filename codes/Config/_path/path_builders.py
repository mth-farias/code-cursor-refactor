#%% CELL 00 — HEADER & SCOPE
"""
path_builders.py — Canonical Path Constructors
===============================================

Build canonical Paths by combining folder locations with filenames.

Exports:
    configure(folders: dict, names: dict) → dict[str, callable]
    
Path Builders (10 total):
    - tracked_path(base: str) → Path
    - sleap_path(base: str) → Path
    - scored_path(base: str) → Path
    - pose_path(base: str) → Path
    - arenaimg_path(base: str) → Path
    - flyvideo_path(base: str) → Path
    - cropvideo_path(base: str) → Path
    - report_error_path() → Path
    - report_flag_path() → Path
    - flag_scored_path(base: str) → Path
    - flag_pose_path(base: str) → Path
    - error_tracked_copy_path(original_filename: str) → Path
    - error_pose_copy_path(original_filename: str) → Path
    
Conventions:
    - All functions return Path objects (under canonical folders)
    - "base" means a stem like 'BASE_flyN' (no suffix)
    - Error copy paths preserve original filename
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Callable

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for path_builders.py.

Why Empty?
    Path builders are pure functions combining folders + names.
    No build-time configuration needed (deps passed via configure()).
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure functions)

#%% CELL 03 — PATH BUILDER FACTORY

def _create_path_builders(folders: dict, names: dict) -> dict[str, Callable]:
    """
    Create path builder functions bound to folder locations and name builders.
    
    Args:
        folders: Dictionary with pTracked, pScored, etc. (from folders.py).
        names: Dictionary with tracked_name, scored_name, etc. (from name_builders.py).
        
    Returns:
        Dictionary with 13 path builder functions.
        
    Notes:
        - Uses closures to capture folder paths and name functions
        - Functions are stateless (pure)
        - Combines folder + name for canonical path
    """
    # Extract folders
    pTracked = folders["pTracked"]
    pSleap = folders["pSleap"]
    pScored = folders["pScored"]
    pPose = folders["pPose"]
    pArenaImage = folders["pArenaImage"]
    pFlyVideo = folders["pFlyVideo"]
    pCropVideo = folders["pCropVideo"]
    pError = folders["pError"]
    pFlag = folders["pFlag"]
    pFlagScored = folders["pFlagScored"]
    pFlagPose = folders["pFlagPose"]
    pErrorTracked = folders["pErrorTracked"]
    pErrorPose = folders["pErrorPose"]
    
    # Extract name builders
    tracked_name = names["tracked_name"]
    sleap_name = names["sleap_name"]
    scored_name = names["scored_name"]
    pose_name = names["pose_name"]
    arenaimg_name = names["arenaimg_name"]
    flyvideo_name = names["flyvideo_name"]
    cropvideo_name = names["cropvideo_name"]
    report_error_name = names["report_error_name"]
    report_flag_name = names["report_flag_name"]
    
    # --- Good output path builders ---
    def tracked_path(base: str) -> Path:
        """Canonical path for tracked file: pTracked / BASE_flyN_tracked.csv"""
        return pTracked / tracked_name(base)
    
    def sleap_path(base: str) -> Path:
        """Canonical path for sleap file: pSleap / BASE_flyN_sleap.csv"""
        return pSleap / sleap_name(base)
    
    def scored_path(base: str) -> Path:
        """Canonical path for scored file: pScored / BASE_flyN_scored.csv"""
        return pScored / scored_name(base)
    
    def pose_path(base: str) -> Path:
        """Canonical path for pose file: pPose / BASE_flyN_pose.csv"""
        return pPose / pose_name(base)
    
    def arenaimg_path(base: str) -> Path:
        """Canonical path for arena image: pArenaImage / BASE_flyN_arenaimg.png"""
        return pArenaImage / arenaimg_name(base)
    
    def flyvideo_path(base: str) -> Path:
        """Canonical path for fly video: pFlyVideo / BASE_flyN_flyvideo.avi"""
        return pFlyVideo / flyvideo_name(base)
    
    def cropvideo_path(base: str) -> Path:
        """Canonical path for crop video: pCropVideo / BASE_flyN_cropvideo.avi"""
        return pCropVideo / cropvideo_name(base)
    
    # --- Report path builders ---
    def report_error_path() -> Path:
        """Canonical path for error report: pError / REPORT_ERROR.csv"""
        return pError / report_error_name()
    
    def report_flag_path() -> Path:
        """Canonical path for flag report: pFlag / REPORT_FLAG.csv"""
        return pFlag / report_flag_name()
    
    # --- Flagged output path builders ---
    def flag_scored_path(base: str) -> Path:
        """Canonical path for flagged scored file: pFlagScored / BASE_flyN_scored.csv"""
        return pFlagScored / scored_name(base)
    
    def flag_pose_path(base: str) -> Path:
        """Canonical path for flagged pose file: pFlagPose / BASE_flyN_pose.csv"""
        return pFlagPose / pose_name(base)
    
    # --- Error input copy path builders ---
    def error_tracked_copy_path(original_filename: str) -> Path:
        """
        Canonical path for error tracked copy: pErrorTracked / original_filename.
        
        Args:
            original_filename: Original tracked filename (e.g., 'BASE_flyN_tracked.csv').
            
        Returns:
            Path to error copy (preserves original filename).
        """
        return pErrorTracked / Path(original_filename).name
    
    def error_pose_copy_path(original_filename: str) -> Path:
        """
        Canonical path for error pose copy: pErrorPose / original_filename.
        
        Args:
            original_filename: Original sleap filename (e.g., 'BASE_flyN_sleap.csv').
            
        Returns:
            Path to error copy (preserves original filename).
        """
        return pErrorPose / Path(original_filename).name
    
    return {
        "tracked_path": tracked_path,
        "sleap_path": sleap_path,
        "scored_path": scored_path,
        "pose_path": pose_path,
        "arenaimg_path": arenaimg_path,
        "flyvideo_path": flyvideo_path,
        "cropvideo_path": cropvideo_path,
        "report_error_path": report_error_path,
        "report_flag_path": report_flag_path,
        "flag_scored_path": flag_scored_path,
        "flag_pose_path": flag_pose_path,
        "error_tracked_copy_path": error_tracked_copy_path,
        "error_pose_copy_path": error_pose_copy_path,
    }


#%% CELL 04 — CONFIGURE

def configure(folders: dict, names: dict) -> dict[str, Callable]:
    """
    Generate path builder functions from folders and name builders.
    
    Args:
        folders: Dictionary with pTracked, pScored, etc. (from folders.py).
        names: Dictionary with tracked_name, scored_name, etc. (from name_builders.py).
        
    Returns:
        Dictionary with 13 path builder functions.
        
    Validation:
        Asserts 13 functions returned.
        
    Notes:
        - Called by coordinator with folders + names
        - Functions are closures capturing folder paths
        - Returns dict (not MappingProxyType) for coordinator assembly
    """
    builders = _create_path_builders(folders, names)
    
    # Validation
    assert len(builders) == 13, f"Expected 13 path builders, got {len(builders)}"
    
    return builders


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

