#%% CELL 00 — HEADER & SCOPE
'''
shared.py

Overview:
  Signals shared across multiple files (single source of truth).
  4 parameters: FrameIndex + 3 stimulus channels (VisualStim, Stim0, Stim1).

Use:
  FrameIndex: global per-frame reference aligned to BASE.FrameID.
  Stimuli: names/labels aligned with experiment.py::STIMULI.

Dependencies:
  schema.py (ParamSpec)
'''


#%% CELL 01 — IMPORTS
"""
Imports for schema definition.
"""
from .schema import ParamSpec


#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for SHARED parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _SHARED dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — SHARED PARAMETERS
"""
Signals shared across multiple files (single source of truth):
- FrameIndex: global per-frame reference aligned to BASE.FrameID.
- Stimuli channels: names/labels aligned with experiment.py::STIMULI.
"""
_SHARED: dict[str, ParamSpec] = {
	"FrameIndex": {
		"label": "Frame Index",
		"tags": ["tracked", "sleap", "pose", "scored"],
		"type": "int",
		"unit": "frames",
		"role": "continuous",
		"domain": None,
		"description": "Reference aligned to BASE.FrameID; not a local 0..N counter.",
	},
	"VisualStim": {
		"label": "VisualStim",
		"tags": ["tracked", "scored", "stimuli"],
		"type": "int",
		"unit": "state",
		"role": "binary",
		"domain": [0, 1],
		"description": "Visual stimulus on/off per frame.",
	},
	"Stim0": {
		"label": "RedLED",
		"tags": ["tracked", "scored", "stimuli"],
		"type": "int",
		"unit": "state",
		"role": "binary",
		"domain": [0, 1],
		"description": "Red LED stimulus on/off per frame.",
	},
	"Stim1": {
		"label": "GreenLED",
		"tags": ["tracked", "scored", "stimuli"],
		"type": "int",
		"unit": "state",
		"role": "binary",
		"domain": [0, 1],
		"description": "Green LED stimulus on/off per frame.",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return SHARED parameter definitions.
	
	Returns:
	    Dictionary of 4 SHARED parameters (FrameIndex + 3 stimulus channels).
	"""
	assert len(_SHARED) == 4, f"Expected 4 SHARED parameters, got {len(_SHARED)}"
	return _SHARED


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

