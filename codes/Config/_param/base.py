#%% CELL 00 — HEADER & SCOPE
'''
base.py

Overview:
  Hardware counters and GPIO signals from BASE.csv.
  3 parameters: GPIO, FrameID, Timestamp.

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
No user constants needed for BASE parameter registry.

Why Empty?
    Pure data registry (no user-configurable constants).
    All definitions in _BASE dictionary below.
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)


#%% CELL 03 — BASE PARAMETERS
"""
Hardware counters and GPIO signals from BASE.csv.
"""
_BASE: dict[str, ParamSpec] = {
	"GPIO": {
		"label": "GPIO State",
		"tags": ["BASE"],
		"type": "int",
		"unit": "state",
		"role": "categorical",
		"domain": None,
		"description": "Digital input state from GPIO pins aligned to frame clock (stimulus markers).",
	},
	"FrameID": {
		"label": "Frame ID",
		"tags": ["BASE"],
		"type": "int",
		"unit": "frames",
		"role": "continuous",
		"domain": None,
		"description": "Camera frame counter ticks aligned to frame clock (may not start at 0).",
	},
	"Timestamp": {
		"label": "Timestamp",
		"tags": ["BASE"],
		"type": "int",
		"unit": "ns",
		"role": "continuous",
		"domain": None,
		"description": "Acquisition clock time in nanoseconds (monotonic, not Unix time).",
	},
}


#%% CELL 04 — CONFIGURE
"""
Configure function following delegation pattern.
"""
def configure() -> dict[str, ParamSpec]:
	"""
	Return BASE parameter definitions.
	
	Returns:
	    Dictionary of 3 BASE parameters (GPIO, FrameID, Timestamp).
	"""
	assert len(_BASE) == 3, f"Expected 3 BASE parameters, got {len(_BASE)}"
	return _BASE


#%% CELL 05 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

