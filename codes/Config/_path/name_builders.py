#%% CELL 00 — HEADER & SCOPE
"""
name_builders.py — Filename Constructors
=========================================

Build filenames following suffix policy (strings only, no Paths).

Exports:
    configure(policy: dict) → dict[str, callable]
    
Name Builders (10 total):
    - stem_without_suffix(filename: str) → str
    - tracked_name(base: str) → str
    - sleap_name(base: str) → str
    - scored_name(base: str) → str
    - pose_name(base: str) → str
    - arenaimg_name(base: str) → str
    - flyvideo_name(base: str) → str
    - cropvideo_name(base: str) → str
    - report_error_name() → str
    - report_flag_name() → str
    
Conventions:
    - "base" means a stem like 'BASE_flyN' (no policy suffix)
    - *_name functions return strings (not Paths)
    - stem_without_suffix extracts base from any policy filename
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations
from pathlib import Path
from typing import Callable

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for name_builders.py.

Why Empty?
    Name builders are pure functions that depend only on policy suffixes.
    No build-time configuration needed (policy passed via configure()).
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure functions)

#%% CELL 03 — NAME BUILDER FACTORY

def _create_name_builders(policy: dict) -> dict[str, Callable]:
    """
    Create name builder functions bound to suffix policy.
    
    Args:
        policy: Dictionary with SUFFIX_* and REPORT_* keys.
        
    Returns:
        Dictionary with 10 name builder functions.
        
    Notes:
        - Uses closures to capture policy suffixes
        - Functions are stateless (pure)
        - stem_without_suffix is special (extracts base from any filename)
    """
    # Extract suffixes from policy
    SUFFIX_TRACKED = policy["SUFFIX_TRACKED"]
    SUFFIX_SLEAP = policy["SUFFIX_SLEAP"]
    SUFFIX_ARENAIMG = policy["SUFFIX_ARENAIMG"]
    SUFFIX_FLYVIDEO = policy["SUFFIX_FLYVIDEO"]
    SUFFIX_CROPVIDEO = policy["SUFFIX_CROPVIDEO"]
    SUFFIX_SCORED = policy["SUFFIX_SCORED"]
    SUFFIX_POSE = policy["SUFFIX_POSE"]
    REPORT_ERROR_NAME = policy["REPORT_ERROR_NAME"]
    REPORT_FLAG_NAME = policy["REPORT_FLAG_NAME"]
    KNOWN_SUFFIXES = policy["KNOWN_SUFFIXES"]
    
    # --- Stem extractor ---
    def stem_without_suffix(filename: str) -> str:
        """
        Return the base stem without any known policy suffix.
        
        Args:
            filename: Filename or path string.
            
        Returns:
            Base stem (e.g., 'BASE_fly3_tracked.csv' → 'BASE_fly3').
            
        Notes:
            - Tries all KNOWN_SUFFIXES in order
            - Falls back to Path.stem if no match
        """
        name = Path(filename).name
        for suf in KNOWN_SUFFIXES:
            if name.endswith(suf):
                return name[: -len(suf)]
        return Path(name).stem
    
    # --- Per-fly artifact name builders ---
    def tracked_name(base: str) -> str:
        """Build tracked filename: base + '_tracked.csv'"""
        return f"{base}{SUFFIX_TRACKED}"
    
    def sleap_name(base: str) -> str:
        """Build sleap filename: base + '_sleap.csv'"""
        return f"{base}{SUFFIX_SLEAP}"
    
    def scored_name(base: str) -> str:
        """Build scored filename: base + '_scored.csv'"""
        return f"{base}{SUFFIX_SCORED}"
    
    def pose_name(base: str) -> str:
        """Build pose filename: base + '_pose.csv'"""
        return f"{base}{SUFFIX_POSE}"
    
    def arenaimg_name(base: str) -> str:
        """Build arena image filename: base + '_arenaimg.png'"""
        return f"{base}{SUFFIX_ARENAIMG}"
    
    def flyvideo_name(base: str) -> str:
        """Build fly video filename: base + '_flyvideo.avi'"""
        return f"{base}{SUFFIX_FLYVIDEO}"
    
    def cropvideo_name(base: str) -> str:
        """Build crop video filename: base + '_cropvideo.avi'"""
        return f"{base}{SUFFIX_CROPVIDEO}"
    
    # --- Report name builders (no args) ---
    def report_error_name() -> str:
        """Return error report filename: 'REPORT_ERROR.csv'"""
        return REPORT_ERROR_NAME
    
    def report_flag_name() -> str:
        """Return flag report filename: 'REPORT_FLAG.csv'"""
        return REPORT_FLAG_NAME
    
    return {
        "stem_without_suffix": stem_without_suffix,
        "tracked_name": tracked_name,
        "sleap_name": sleap_name,
        "scored_name": scored_name,
        "pose_name": pose_name,
        "arenaimg_name": arenaimg_name,
        "flyvideo_name": flyvideo_name,
        "cropvideo_name": cropvideo_name,
        "report_error_name": report_error_name,
        "report_flag_name": report_flag_name,
    }


#%% CELL 04 — CONFIGURE

def configure(policy: dict) -> dict[str, Callable]:
    """
    Generate name builder functions from suffix policy.
    
    Args:
        policy: Dictionary with SUFFIX_* and REPORT_* keys (from filename_policy).
        
    Returns:
        Dictionary with 10 name builder functions.
        
    Validation:
        Asserts 10 functions returned.
        
    Notes:
        - Called by coordinator with policy from filename_policy
        - Functions are closures capturing policy suffixes
        - Returns dict (not MappingProxyType) for coordinator assembly
    """
    builders = _create_name_builders(policy)
    
    # Validation
    assert len(builders) == 10, f"Expected 10 name builders, got {len(builders)}"
    
    return builders


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

