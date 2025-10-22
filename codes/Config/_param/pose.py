#%% CELL 00 — HEADER & SCOPE
'''
pose.py

Overview:
  Arena-calibrated positions in mm and orientation from pose.csv.
  14 parameters: View + View_X/Y + Orientation + 5 body parts × 2 coords (X/Y).

Use:
  Imported by _param/__init__.py::configure().
  Called via configure() pattern.

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
No user constants needed for POSE parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _POSE dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — POSE PARAMETERS
"""
Arena-calibrated positions in mm and orientation from pose.csv.
Starts with selected view and orientation, followed by body-part
positions in the order: Head, Thorax, Abdomen, LeftWing, RightWing.
"""
_POSE: dict[str, ParamSpec] = {
	"View": {
		"label": "View",
		"tags": ["pose"],
		"type": "string",
		"unit": "category",
		"role": "categorical",
		"domain": ["Left", "Right", "Top", "Vertical"],
		"description": "Selected camera view label (Bottom→Top normalized).",
	},
	"View_X": {
		"label": "View X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "X coordinate (mm) in the selected view, post-calibration.",
	},
	"View_Y": {
		"label": "View Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Y coordinate (mm) in the selected view, post-calibration.",
	},
	"Orientation": {
		"label": "Orientation",
		"tags": ["pose"],
		"type": "float",
		"unit": "deg",
		"role": "continuous",
		"domain": [0.0, 360.0],
		"description": "Body orientation (deg) from Thorax→View axis; 0–360 wrap.",
	},

	# Per-part positions in the selected view (mm)
	"Head_X": {
		"label": "Head X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Head keypoint X (mm) in the selected view.",
	},
	"Head_Y": {
		"label": "Head Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Head keypoint Y (mm) in the selected view.",
	},
	"Thorax_X": {
		"label": "Thorax X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Thorax keypoint X (mm) in the selected view.",
	},
	"Thorax_Y": {
		"label": "Thorax Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Thorax keypoint Y (mm) in the selected view.",
	},
	"Abdomen_X": {
		"label": "Abdomen X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Abdomen keypoint X (mm) in the selected view.",
	},
	"Abdomen_Y": {
		"label": "Abdomen Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Abdomen keypoint Y (mm) in the selected view.",
	},
	"LeftWing_X": {
		"label": "Left Wing X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Left wing keypoint X (mm) in the selected view.",
	},
	"LeftWing_Y": {
		"label": "Left Wing Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Left wing keypoint Y (mm) in the selected view.",
	},
	"RightWing_X": {
		"label": "Right Wing X",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Right wing keypoint X (mm) in the selected view.",
	},
	"RightWing_Y": {
		"label": "Right Wing Y",
		"tags": ["pose"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Right wing keypoint Y (mm) in the selected view.",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return POSE parameter definitions.
	
	Returns:
	    Dictionary of 14 POSE parameters (View + View_X/Y + Orientation + 5 body parts × 2).
	"""
	assert len(_POSE) == 14, f"Expected 14 POSE parameters, got {len(_POSE)}"
	return _POSE


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

