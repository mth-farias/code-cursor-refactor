from __future__ import annotations

#%% CELL 00 — HEADER & SCOPE
'''
report.py

Overview:
  Human-readable report generator for PARAM registry.
  Shows total count and per-section breakdown.

Use:
  Called by parent param.py when run directly (if __name__ == "__main__").
  Demonstrates registry structure and completeness.

Dependencies:
  - base, shared, tracked, scored, sleap, pose (workers)
'''


#%% CELL 01 — IMPORTS
"""
Imports for worker modules.
"""
from . import base
from . import shared
from . import tracked
from . import scored
from . import sleap
from . import pose


#%% CELL 02 — REPORT FUNCTION
"""
Generate formatted report of PARAM registry.
"""
def render_param_report() -> str:
	"""
	Generate a formatted report of the PARAM registry.
	
	Returns:
	    String containing the report with section breakdowns.
	"""
	# Get all sections
	sections = [
		("BASE", base.configure()),
		("SHARED", shared.configure()),
		("TRACKED", tracked.configure()),
		("SCORED", scored.configure()),
		("SLEAP", sleap.configure()),
		("POSE", pose.configure()),
	]
	
	# Calculate total
	total = sum(len(params) for _, params in sections)
	
	# Build report
	lines = []
	lines.append("PARAM registry summary")
	lines.append(f"Total parameters: {total}\n")
	
	for title, params in sections:
		lines.append(f"{title} ({len(params)})")
		for name in params:
			lines.append(f"  - {name}")
		lines.append("")
	
	return "\n".join(lines)


#%% CELL 03 — EXPORTS
"""
Public API.
"""
__all__ = ["render_param_report"]

