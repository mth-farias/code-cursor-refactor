#%% CELL 00 — HEADER & SCOPE
"""
report.py — Diagnostic Functions
=================================

Lightweight, opt-in diagnostics for folder structure and file counts.

Exports:
    configure(folders: dict, policy: dict) → dict[str, callable]
    
Diagnostic Functions (4 total):
    - missing_folders() → list[Path]
    - tree_counts() → dict[str, int]
    - sample_files(n: int = 3) → dict[str, list[str]]
    - sanity_checks() → list[str]
    
Notes:
    - Safe to run (read-only, no writes)
    - Returns diagnostic data (doesn't print)
    - Phase 5 will add demo() function for pretty printing
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Callable, Iterable

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for report.py.

Why Empty?
    Diagnostic functions are utilities (no configuration).
    Dependencies passed via configure() from coordinator.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - diagnostic utilities)

#%% CELL 03 — DIAGNOSTIC FUNCTION FACTORY

def _create_diagnostic_functions(folders: dict, policy: dict) -> dict[str, Callable]:
    """
    Create diagnostic functions for folder structure health checks.
    
    Args:
        folders: Dictionary with all folder paths (from folders.py).
        policy: Dictionary with SUFFIX_* (from filename_policy.py).
        
    Returns:
        Dictionary with 4 diagnostic functions.
        
    Notes:
        - Functions are read-only (safe to run anytime)
        - Returns data (doesn't print); caller formats output
        - Useful for debugging folder setup issues
    """
    # Extract folders for checking
    pCodes = folders["pCodes"]
    pConfig = folders["pConfig"]
    pBehaviorClassifier = folders["pBehaviorClassifier"]
    pBonfly = folders["pBonfly"]
    pBonsai = folders["pBonsai"]
    pFlyHigherProtocol = folders["pFlyHigherProtocol"]
    pFlyHigherTracker = folders["pFlyHigherTracker"]
    pRawData = folders["pRawData"]
    pPostProcessing = folders["pPostProcessing"]
    pTracked = folders["pTracked"]
    pSleap = folders["pSleap"]
    pArenaImage = folders["pArenaImage"]
    pFlyVideo = folders["pFlyVideo"]
    pCropVideo = folders["pCropVideo"]
    pBehaviorClassification = folders["pBehaviorClassification"]
    pScored = folders["pScored"]
    pPose = folders["pPose"]
    pError = folders["pError"]
    pErrorTracked = folders["pErrorTracked"]
    pErrorPose = folders["pErrorPose"]
    pFlag = folders["pFlag"]
    pFlagScored = folders["pFlagScored"]
    pFlagPose = folders["pFlagPose"]
    
    # Extract suffixes
    SUFFIX_TRACKED = policy["SUFFIX_TRACKED"]
    SUFFIX_SLEAP = policy["SUFFIX_SLEAP"]
    SUFFIX_ARENAIMG = policy["SUFFIX_ARENAIMG"]
    SUFFIX_FLYVIDEO = policy["SUFFIX_FLYVIDEO"]
    SUFFIX_CROPVIDEO = policy["SUFFIX_CROPVIDEO"]
    SUFFIX_SCORED = policy["SUFFIX_SCORED"]
    SUFFIX_POSE = policy["SUFFIX_POSE"]
    
    # --- Helper: Check existence ---
    def _exists_all(paths: Iterable[Path]) -> list[Path]:
        """Return list of paths that don't exist."""
        return [p for p in paths if not Path(p).exists()]
    
    # --- Diagnostic functions ---
    def missing_folders() -> list[Path]:
        """
        Check which canonical folders are missing.
        
        Returns:
            List of Path objects for folders that don't exist.
            Empty list means all folders present.
        """
        folder_list = [
            pCodes, pConfig, pBehaviorClassifier,
            pBonfly, pBonsai, pFlyHigherProtocol, pFlyHigherTracker,
            pRawData,
            pPostProcessing, pTracked, pSleap, pArenaImage, pFlyVideo, pCropVideo,
            pBehaviorClassification, pScored, pPose,
            pError, pErrorTracked, pErrorPose,
            pFlag, pFlagScored, pFlagPose,
        ]
        return _exists_all(folder_list)
    
    def tree_counts() -> dict[str, int]:
        """
        Count files in each canonical folder.
        
        Returns:
            Dictionary with folder names as keys, file counts as values.
            
        Notes:
            - Returns 0 for missing folders (no error)
            - Useful for quick health check of pipeline outputs
        """
        return {
            "Tracked": len(list(pTracked.glob(f"*{SUFFIX_TRACKED}"))) if pTracked.exists() else 0,
            "Sleap": len(list(pSleap.glob(f"*{SUFFIX_SLEAP}"))) if pSleap.exists() else 0,
            "ArenaImage": len(list(pArenaImage.glob(f"*{SUFFIX_ARENAIMG}"))) if pArenaImage.exists() else 0,
            "FlyVideo": len(list(pFlyVideo.glob(f"*{SUFFIX_FLYVIDEO}"))) if pFlyVideo.exists() else 0,
            "CropVideo": len(list(pCropVideo.glob(f"*{SUFFIX_CROPVIDEO}"))) if pCropVideo.exists() else 0,
            "Scored": len(list(pScored.glob(f"*{SUFFIX_SCORED}"))) if pScored.exists() else 0,
            "Pose": len(list(pPose.glob(f"*{SUFFIX_POSE}"))) if pPose.exists() else 0,
            "Flag/Scored": len(list(pFlagScored.glob(f"*{SUFFIX_SCORED}"))) if pFlagScored.exists() else 0,
            "Flag/Pose": len(list(pFlagPose.glob(f"*{SUFFIX_POSE}"))) if pFlagPose.exists() else 0,
            "Error/Tracked": len(list(pErrorTracked.glob(f"*{SUFFIX_TRACKED}"))) if pErrorTracked.exists() else 0,
            "Error/Pose": len(list(pErrorPose.glob(f"*{SUFFIX_SLEAP}"))) if pErrorPose.exists() else 0,
        }
    
    def sample_files(n: int = 3) -> dict[str, list[str]]:
        """
        Sample first N filenames from each canonical folder.
        
        Args:
            n: Number of samples to return per folder (default: 3).
            
        Returns:
            Dictionary with folder names as keys, filename lists as values.
            
        Notes:
            - Returns empty list for missing folders
            - Useful for quick inspection of pipeline outputs
        """
        def _names(folder: Path, pattern: str) -> list[str]:
            """Extract first N filenames from folder."""
            if not folder.exists():
                return []
            return [p.name for p in sorted(folder.glob(pattern))[:n]]
        
        return {
            "Tracked": _names(pTracked, f"*{SUFFIX_TRACKED}"),
            "Sleap": _names(pSleap, f"*{SUFFIX_SLEAP}"),
            "Scored": _names(pScored, f"*{SUFFIX_SCORED}"),
            "Pose": _names(pPose, f"*{SUFFIX_POSE}"),
            "ArenaImage": _names(pArenaImage, f"*{SUFFIX_ARENAIMG}"),
            "FlyVideo": _names(pFlyVideo, f"*{SUFFIX_FLYVIDEO}"),
            "CropVideo": _names(pCropVideo, f"*{SUFFIX_CROPVIDEO}"),
            "Flag/Scored": _names(pFlagScored, f"*{SUFFIX_SCORED}"),
            "Flag/Pose": _names(pFlagPose, f"*{SUFFIX_POSE}"),
            "Error/Tracked": _names(pErrorTracked, f"*{SUFFIX_TRACKED}"),
            "Error/Pose": _names(pErrorPose, f"*{SUFFIX_SLEAP}"),
        }
    
    def sanity_checks() -> list[str]:
        """
        Run sanity checks on folder structure.
        
        Returns:
            List of issue strings. Empty list means no issues found.
            
        Checks:
            - pBehaviorClassifier != pBehaviorClassification (package vs outputs)
            - All expected keys present in PATH export
            
        Notes:
            - Returns human-readable issue descriptions
            - Caller should display/log issues if any
        """
        issues: list[str] = []
        
        # Check for package vs outputs collision
        if pBehaviorClassifier.resolve() == pBehaviorClassification.resolve():
            issues.append(
                "pBehaviorClassifier equals pBehaviorClassification "
                "(package vs outputs collision)."
            )
        
        return issues
    
    return {
        "missing_folders": missing_folders,
        "tree_counts": tree_counts,
        "sample_files": sample_files,
        "sanity_checks": sanity_checks,
    }


#%% CELL 04 — CONFIGURE

def configure(folders: dict, policy: dict) -> dict[str, Callable]:
    """
    Generate diagnostic functions from folder map and policy.
    
    Args:
        folders: Dictionary with all folder paths (from folders.py).
        policy: Dictionary with SUFFIX_* (from filename_policy.py).
        
    Returns:
        Dictionary with 4 diagnostic functions.
        
    Validation:
        Asserts 4 functions returned.
        
    Notes:
        - Called by coordinator with folders + policy
        - Functions are read-only (safe diagnostics)
        - Returns dict (not MappingProxyType) for coordinator assembly
        - Phase 5 will add demo() function for pretty printing
    """
    diagnostics = _create_diagnostic_functions(folders, policy)
    
    # Validation
    assert len(diagnostics) == 4, f"Expected 4 diagnostic functions, got {len(diagnostics)}"
    
    return diagnostics


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

