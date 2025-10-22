from __future__ import annotations

#%% CELL 00 — HEADER & SCOPE
'''
param.py

Overview:
  Canonical registry of all CSV parameters across the pipeline:
    - BASE, tracked, scored, sleap, pose
  Each entry declares:
    label, tags, type, unit, role, domain, description.

Use:
  - Single source of truth for parameter documentation.
  - Validation of CSV columns at load time.
  - Generation of human-readable reports.

Dependencies:
  _param/ subpackage (controller + worker pattern).
'''


#%% CELL 01 — IMPORTS
"""
Imports for dynamic module loading.
"""
import importlib
import sys
from pathlib import Path


#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for param.

Why Empty?
    Unlike experiment.py and color.py, param.py contains only static schema
    definitions with no user-configurable runtime behavior. The entire
    parameter registry is a pure data structure—a TypedDict specification
    for CSV column metadata (label, tags, type, unit, role, domain, description).
    
    Each parameter definition is immutable metadata about the data pipeline's
    CSV columns. There are no thresholds to tune, no experimental conditions
    to select, no processing toggles to flip. The registry serves as the
    authoritative reference for CSV schema validation and report generation.
    
    Therefore, CELL 02 exists for structural consistency with the Config
    package's controller pattern, but remains intentionally empty. All
    registry logic lives in the _param/ subpackage workers (base.py,
    shared.py, tracked.py, scored.py, sleap.py, pose.py).
"""
# (intentionally empty - pure metadata registry)


#%% CELL 03 — DYNAMIC IMPORT
"""
Load the _param subpackage using dynamic import pattern.
Enables both script execution and module import contexts.
"""
try:
	# Package context (from Config import param)
	_param = importlib.import_module("._param", package="Config")
except ImportError:
	# Script context (python param.py)
	sys.path.insert(0, str(Path(__file__).parent))
	_param = importlib.import_module("_param")


#%% CELL 04 — CONFIGURE
"""
Delegate to _param subpackage coordinator.
"""
PARAM = _param.configure()


#%% CELL 05 — EXPORTS
"""
Public API - single immutable registry.
"""
__all__ = ["PARAM"]


#%% CELL 06 — REPORT
"""
When run directly, display human-readable parameter summary.
"""
if __name__ == "__main__":
	from _param.report import render_param_report
	print(render_param_report())

