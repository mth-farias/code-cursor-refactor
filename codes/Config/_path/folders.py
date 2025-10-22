#%% CELL 00 — HEADER & SCOPE
"""
folders.py — Canonical Folder Map
==================================

Declares experiment folder tree with 13 canonical subfolders.

Exports:
    configure(root: Path) → dict[str, Path]
    
Folder Keys (24 total):
    Packages/Tools:
        - pCodes, pConfig, pBehaviorClassifier
        - pBonfly, pBonsai, pFlyHigherProtocol, pFlyHigherTracker
    Data Roots:
        - pRawData, pPostProcessing, pBehaviorClassification
    PostProcessing Subfolders:
        - pTracked, pSleap, pArenaImage, pFlyVideo, pCropVideo
    Classification Subfolders:
        - pScored, pPose
    QC Subfolders:
        - pError, pErrorTracked, pErrorPose
        - pFlag, pFlagScored, pFlagPose
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for folders.py.

Why Empty?
    Folder structure is derived from experiment root at runtime.
    All paths computed via configure(root) delegation.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - runtime path construction)

#%% CELL 03 — FOLDER CONSTRUCTION

def _build_folders(root: Path) -> dict[str, Path]:
    """
    Build all canonical folder paths under experiment root.
    
    Args:
        root: Experiment root folder (e.g., /content/drive/MyDrive/Experiments)
        
    Returns:
        Dictionary with 24 folder path entries.
        
    Notes:
        - All paths are Path objects (not resolved, for cross-platform compatibility)
        - No filesystem I/O (pure path construction)
        - Mirrors layout documented in original path.py CELL 00
    """
    # --- Codes/ (importable packages) ---
    pCodes = root / "Codes"
    pConfig = pCodes / "Config"
    pBehaviorClassifier = pCodes / "BehaviorClassifier"
    
    # --- Bonfly/ (aux repos & tooling) ---
    pBonfly = root / "Bonfly"
    pBonsai = pBonfly / "Bonsai"
    pFlyHigherProtocol = pBonfly / "FlyHigher-Protocol"
    pFlyHigherTracker = pBonfly / "FlyHigher-Tracker"
    
    # --- RawData/ (acquisition) ---
    pRawData = root / "RawData"
    
    # --- PostProcessing/ (tracker & pose outputs) ---
    pPostProcessing = root / "PostProcessing"
    pTracked = pPostProcessing / "Tracked"
    pSleap = pPostProcessing / "Sleap"
    pArenaImage = pPostProcessing / "ArenaImage"
    pFlyVideo = pPostProcessing / "FlyVideo"
    pCropVideo = pPostProcessing / "CropVideo"
    
    # --- BehaviorClassification/ (outputs root) ---
    pBehaviorClassification = root / "BehaviorClassification"
    
    # Good outputs
    pScored = pBehaviorClassification / "Scored"
    pPose = pBehaviorClassification / "Pose"
    
    # Error (reports + verbatim input copies)
    pError = pBehaviorClassification / "Error"
    pErrorTracked = pError / "Tracked"
    pErrorPose = pError / "Pose"
    
    # Flag (reports + flagged outputs in subfolders)
    pFlag = pBehaviorClassification / "Flag"
    pFlagScored = pFlag / "Scored"
    pFlagPose = pFlag / "Pose"
    
    return {
        # Experiment root
        "pExperimentalFolder": root,
        
        # Codes/ (packages)
        "pCodes": pCodes,
        "pConfig": pConfig,
        "pBehaviorClassifier": pBehaviorClassifier,
        
        # Bonfly/ (tooling)
        "pBonfly": pBonfly,
        "pBonsai": pBonsai,
        "pFlyHigherProtocol": pFlyHigherProtocol,
        "pFlyHigherTracker": pFlyHigherTracker,
        
        # Data roots
        "pRawData": pRawData,
        "pPostProcessing": pPostProcessing,
        
        # PostProcessing subfolders
        "pTracked": pTracked,
        "pSleap": pSleap,
        "pArenaImage": pArenaImage,
        "pFlyVideo": pFlyVideo,
        "pCropVideo": pCropVideo,
        
        # Classification outputs
        "pBehaviorClassification": pBehaviorClassification,
        "pScored": pScored,
        "pPose": pPose,
        
        # Error & Flag (QC)
        "pError": pError,
        "pErrorTracked": pErrorTracked,
        "pErrorPose": pErrorPose,
        "pFlag": pFlag,
        "pFlagScored": pFlagScored,
        "pFlagPose": pFlagPose,
    }


#%% CELL 04 — CONFIGURE

def configure(root: Path) -> dict[str, Path]:
    """
    Generate canonical folder map for given experiment root.
    
    Args:
        root: Experiment root Path (absolute or relative).
        
    Returns:
        Dictionary with 24 folder path keys.
        
    Validation:
        Asserts 24 entries (1 root + 23 subfolders).
        
    Notes:
        - Called by coordinator with detected/overridden root
        - No filesystem access (pure path construction)
        - Returns dict (not MappingProxyType) for coordinator assembly
    """
    folders = _build_folders(root)
    
    # Validation: Expect 24 folder paths (1 root + 23 subfolders)
    assert len(folders) == 24, f"Expected 24 folder paths, got {len(folders)}"
    
    return folders


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

