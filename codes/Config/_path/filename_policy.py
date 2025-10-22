#%% CELL 00 — HEADER & SCOPE
"""
filename_policy.py — Filename Suffix Policy
============================================

Centralize all filename suffixes used across artifacts.

Exports:
    configure() → dict[str, str | tuple[str, ...]]
    
Suffix Constants (8 + 1):
    - SUFFIX_TRACKED, SUFFIX_SLEAP, SUFFIX_ARENAIMG, SUFFIX_FLYVIDEO, SUFFIX_CROPVIDEO
    - SUFFIX_SCORED, SUFFIX_POSE
    - REPORT_ERROR_NAME, REPORT_FLAG_NAME
    - KNOWN_SUFFIXES (tuple of all suffixes)
    
Notes:
    These suffixes are appended to base stems like 'BASE_flyN'.
    Example: 'BASE_fly1' + SUFFIX_TRACKED → 'BASE_fly1_tracked.csv'
"""

#%% CELL 01 — IMPORTS

from __future__ import annotations

#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for filename_policy.py.

Why Empty?
    Suffix policy is fixed by design (stable API contract).
    Changing suffixes would break compatibility with existing pipelines.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - fixed policy)

#%% CELL 03 — SUFFIX DEFINITIONS

# PostProcessing artifact suffixes (tracker & pose outputs)
SUFFIX_TRACKED: str = "_tracked.csv"
SUFFIX_SLEAP: str = "_sleap.csv"
SUFFIX_ARENAIMG: str = "_arenaimg.png"
SUFFIX_FLYVIDEO: str = "_flyvideo.avi"
SUFFIX_CROPVIDEO: str = "_cropvideo.avi"

# BehaviorClassification output suffixes
SUFFIX_SCORED: str = "_scored.csv"
SUFFIX_POSE: str = "_pose.csv"

# Report filenames (fixed CSV names)
REPORT_ERROR_NAME: str = "REPORT_ERROR.csv"
REPORT_FLAG_NAME: str = "REPORT_FLAG.csv"

# Ordered list of known fixed suffixes (for stem extraction and discovery)
KNOWN_SUFFIXES: tuple[str, ...] = (
    SUFFIX_TRACKED,
    SUFFIX_SLEAP,
    SUFFIX_ARENAIMG,
    SUFFIX_FLYVIDEO,
    SUFFIX_CROPVIDEO,
    SUFFIX_SCORED,
    SUFFIX_POSE,
)


#%% CELL 04 — CONFIGURE

def configure() -> dict[str, str | tuple[str, ...]]:
    """
    Export filename suffix policy.
    
    Returns:
        Dictionary with 9 suffix policy entries.
        
    Keys:
        - SUFFIX_TRACKED, SUFFIX_SLEAP, SUFFIX_ARENAIMG, SUFFIX_FLYVIDEO, SUFFIX_CROPVIDEO
        - SUFFIX_SCORED, SUFFIX_POSE
        - REPORT_ERROR_NAME, REPORT_FLAG_NAME
        - KNOWN_SUFFIXES
        
    Validation:
        Asserts 9 entries and 7 items in KNOWN_SUFFIXES.
        
    Notes:
        - Returns dict (not MappingProxyType) for coordinator assembly
        - KNOWN_SUFFIXES tuple used by stem_without_suffix and discovery functions
    """
    policy = {
        "SUFFIX_TRACKED": SUFFIX_TRACKED,
        "SUFFIX_SLEAP": SUFFIX_SLEAP,
        "SUFFIX_ARENAIMG": SUFFIX_ARENAIMG,
        "SUFFIX_FLYVIDEO": SUFFIX_FLYVIDEO,
        "SUFFIX_CROPVIDEO": SUFFIX_CROPVIDEO,
        "SUFFIX_SCORED": SUFFIX_SCORED,
        "SUFFIX_POSE": SUFFIX_POSE,
        "REPORT_ERROR_NAME": REPORT_ERROR_NAME,
        "REPORT_FLAG_NAME": REPORT_FLAG_NAME,
        "KNOWN_SUFFIXES": KNOWN_SUFFIXES,
    }
    
    # Validation
    assert len(policy) == 10, f"Expected 10 policy entries, got {len(policy)}"
    assert len(KNOWN_SUFFIXES) == 7, f"Expected 7 known suffixes, got {len(KNOWN_SUFFIXES)}"
    
    return policy


#%% CELL 05 — EXPORTS

__all__ = ["configure"]

