#%% CELL 00 — HEADER & SCOPE
'''
scored.py

Overview:
  Derived kinematics and multi-layer classifier labels from scored.csv.
  13 parameters: Position, Speed, Motion, Layers (1/2), Resistant, Behavior.
  Includes denoised variants for Layers 1/2, Resistant, and Behavior.

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
No user constants needed for SCORED parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _SCORED dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — SCORED PARAMETERS
"""
Derived kinematics and multi-layer classifier labels from scored.csv.
Categorical domains are written in canonical order inline.
"""
_SCORED: dict[str, ParamSpec] = {
	"Position_X": {
		"label": "Position X",
		"tags": ["scored"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Centroid X position (mm) in arena coordinates.",
	},
	"Position_Y": {
		"label": "Position Y",
		"tags": ["scored"],
		"type": "float",
		"unit": "mm",
		"role": "continuous",
		"domain": None,
		"description": "Centroid Y position (mm) in arena coordinates.",
	},
	"Speed": {
		"label": "Speed",
		"tags": ["scored"],
		"type": "float",
		"unit": "mm/s",
		"role": "continuous",
		"domain": None,
		"description": "Instantaneous centroid speed (mm/s).",
	},
	"Motion": {
		"label": "Motion",
		"tags": ["scored"],
		"type": "int",
		"unit": "state",
		"role": "binary",
		"domain": [0, 1],
		"description": "Binary motion flag from PixelChange (1 = motion).",
	},

	# Layered labels
	"Layer1": {
		"label": "Layer 1",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Layer1_Jump", "Layer1_Walk", "Layer1_Stationary", "Layer1_Freeze"],
		"description": "First-pass classifier label per frame.",
	},
	"Layer1_Denoised": {
		"label": "Layer 1 (Denoised)",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Layer1_Jump", "Layer1_Walk", "Layer1_Stationary", "Layer1_Freeze"],
		"description": "Layer1 with micro-bouts removed (jump preserved).",
	},
	"Layer2": {
		"label": "Layer 2",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Layer2_Jump", "Layer2_Walk", "Layer2_Stationary", "Layer2_Freeze"],
		"description": "Windowed consensus over Layer1 (jump override).",
	},
	"Layer2_Denoised": {
		"label": "Layer 2 (Denoised)",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Layer2_Jump", "Layer2_Walk", "Layer2_Stationary", "Layer2_Freeze"],
		"description": "Consensus over Layer1_Denoised with half-missing rule.",
	},

	# Resistant tiers
	"Resistant": {
		"label": "Resistant",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Resistant_Walk", "Resistant_Stationary", "Resistant_Freeze"],
		"description": "Summary when a full bout covers a startle window.",
	},
	"Resistant_Denoised": {
		"label": "Resistant (Denoised)",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Resistant_Walk", "Resistant_Stationary", "Resistant_Freeze"],
		"description": "Resistant summary using denoised paths.",
	},

	# Behavior labels
	"Behavior": {
		"label": "Behavior",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Jump", "Walk", "Stationary", "Freeze", "Resistant_Freeze"],
		"description": "Behavior mapped from Layer2; Freeze may promote to Resistant_Freeze.",
	},
	"Behavior_Denoised": {
		"label": "Behavior (Denoised)",
		"tags": ["scored"],
		"type": "string",
		"unit": "classification",
		"role": "categorical",
		"domain": ["Jump", "Walk", "Stationary", "Freeze", "Resistant_Freeze"],
		"description": "Behavior from Layer2_Denoised (NaN placeholder removed from domain).",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return SCORED parameter definitions.
	
	Returns:
	    Dictionary of 12 SCORED parameters (Position, Speed, Motion, Layers, Resistant, Behavior).
	"""
	assert len(_SCORED) == 12, f"Expected 12 SCORED parameters, got {len(_SCORED)}"
	return _SCORED


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

