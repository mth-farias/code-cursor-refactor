#%% CELL 00 — HEADER & SCOPE
'''
sleap.py

Overview:
  Normalized view/body-part positions and confidences from sleap.csv.
  24 parameters: 3 views (Left, Right, Top) × 3 coords + 5 body parts × 3 coords.

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
No user constants needed for SLEAP parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _SLEAP dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — SLEAP PARAMETERS
"""
Normalized view/body-part positions and confidences from sleap.csv.
Views listed first (Left, Right, Top), followed by body parts
(Head, Thorax, Abdomen, LeftWing, RightWing).
"""
_SLEAP: dict[str, ParamSpec] = {
	# Left view
	"Left.Position.X": {
		"label": "Left View X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the left camera view.",
	},
	"Left.Position.Y": {
		"label": "Left View Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the left camera view.",
	},
	"Left.Confidence": {
		"label": "Left View Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the left view.",
	},

	# Right view
	"Right.Position.X": {
		"label": "Right View X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the right camera view.",
	},
	"Right.Position.Y": {
		"label": "Right View Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the right camera view.",
	},
	"Right.Confidence": {
		"label": "Right View Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the right view.",
	},

	# Top view
	"Top.Position.X": {
		"label": "Top View X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the top view.",
	},
	"Top.Position.Y": {
		"label": "Top View Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the top view.",
	},
	"Top.Confidence": {
		"label": "Top View Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the top view.",
	},

	# Body parts (normalized)
	"Head.Position.X": {
		"label": "Head X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the head keypoint.",
	},
	"Head.Position.Y": {
		"label": "Head Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the head keypoint.",
	},
	"Head.Confidence": {
		"label": "Head Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the head keypoint.",
	},

	"Thorax.Position.X": {
		"label": "Thorax X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the thorax keypoint.",
	},
	"Thorax.Position.Y": {
		"label": "Thorax Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the thorax keypoint.",
	},
	"Thorax.Confidence": {
		"label": "Thorax Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the thorax keypoint.",
	},

	"Abdomen.Position.X": {
		"label": "Abdomen X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the abdomen keypoint.",
	},
	"Abdomen.Position.Y": {
		"label": "Abdomen Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the abdomen keypoint.",
	},
	"Abdomen.Confidence": {
		"label": "Abdomen Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the abdomen keypoint.",
	},

	"LeftWing.Position.X": {
		"label": "Left Wing X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the left wing keypoint.",
	},
	"LeftWing.Position.Y": {
		"label": "Left Wing Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the left wing keypoint.",
	},
	"LeftWing.Confidence": {
		"label": "Left Wing Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the left wing keypoint.",
	},

	"RightWing.Position.X": {
		"label": "Right Wing X",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized X coordinate of the right wing keypoint.",
	},
	"RightWing.Position.Y": {
		"label": "Right Wing Y",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Normalized Y coordinate of the right wing keypoint.",
	},
	"RightWing.Confidence": {
		"label": "Right Wing Confidence",
		"tags": ["sleap"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Detection confidence score for the right wing keypoint.",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return SLEAP parameter definitions.
	
	Returns:
	    Dictionary of 24 SLEAP parameters (3 views + 5 body parts, each with Position.X, Position.Y, Confidence).
	"""
	assert len(_SLEAP) == 24, f"Expected 24 SLEAP parameters, got {len(_SLEAP)}"
	return _SLEAP


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

