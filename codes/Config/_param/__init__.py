from __future__ import annotations

#%% CELL 00 — HEADER & SCOPE
'''
_param/__init__.py

Overview:
  Coordinator for the param parameter registry.
  Delegates to worker modules and assembles the final PARAM bundle.

Use:
  Called by parent param.py via configure().
  Returns immutable PARAM dictionary.

Dependencies:
  - schema (ParamSpec type)
  - base, shared, tracked, scored, sleap, pose (workers)
'''


#%% CELL 01 — IMPORTS
"""
Imports for worker modules and type definitions.
"""
from types import MappingProxyType

from . import base
from . import shared
from . import tracked
from . import scored
from . import sleap
from . import pose


#%% CELL 02 — CONFIGURE
"""
Main configuration function following delegation pattern.
"""
def configure() -> MappingProxyType:
	"""
	Assemble and return the complete PARAM registry.
	
	Returns:
	    Immutable dictionary of all CSV parameter specifications.
	    
	Assembly order:
	    BASE (3) → SHARED (4) → TRACKED (3) → SCORED (12) → SLEAP (24) → POSE (14)
	    Total: 60 parameters
	"""
	# Delegate to worker modules
	_BASE = base.configure()
	_SHARED = shared.configure()
	_TRACKED = tracked.configure()
	_SCORED = scored.configure()
	_SLEAP = sleap.configure()
	_POSE = pose.configure()
	
	# Assemble final registry
	_PARAM = {
		**_BASE,
		**_SHARED,
		**_TRACKED,
		**_SCORED,
		**_SLEAP,
		**_POSE,
	}
	
	# Validate total count
	expected_count = 60
	actual_count = len(_PARAM)
	assert actual_count == expected_count, (
		f"PARAM assembly failed: expected {expected_count} parameters, got {actual_count}"
	)
	
	# Return immutable view
	return MappingProxyType(_PARAM)


#%% CELL 03 — EXPORTS
"""
Public API.
"""
__all__ = ["configure"]

