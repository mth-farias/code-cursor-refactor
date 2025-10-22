#%% CELL 00 — HEADER & SCOPE
'''
tracked.py

Overview:
  Tracked geometry and motion proxy from tracked.csv.
  3 parameters: NormalizedCentroidX, NormalizedCentroidY, PixelChange.

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
No user constants needed for TRACKED parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _TRACKED dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — TRACKED PARAMETERS
"""
Tracked geometry and motion proxy from tracked.csv.
"""
_TRACKED: dict[str, ParamSpec] = {
	"NormalizedCentroidX": {
		"label": "Normalized Centroid X",
		"tags": ["tracked"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Centroid X normalized to arena width (0–1).",
	},
	"NormalizedCentroidY": {
		"label": "Normalized Centroid Y",
		"tags": ["tracked"],
		"type": "float",
		"unit": "fraction",
		"role": "continuous",
		"domain": [0.0, 1.0],
		"description": "Centroid Y normalized to arena height (0–1).",
	},
	"PixelChange": {
		"label": "Pixel Change",
		"tags": ["tracked"],
		"type": "int",
		"unit": "px",
		"role": "continuous",
		"domain": None,
		"description": "Count of changed pixels between consecutive frames (motion proxy).",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return TRACKED parameter definitions.
	
	Returns:
	    Dictionary of 3 TRACKED parameters (NormalizedCentroidX, NormalizedCentroidY, PixelChange).
	"""
	assert len(_TRACKED) == 3, f"Expected 3 TRACKED parameters, got {len(_TRACKED)}"
	return _TRACKED


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

