#%% CELL 00 — HEADER & SCOPE
'''
schema.py

Overview:
  Defines ParamSpec TypedDict - the schema for all parameter entries.

Use:
  Imported by all worker modules (base.py, shared.py, etc.).
  Ensures type consistency across parameter definitions.

Dependencies:
  None (pure schema definition).
'''


#%% CELL 01 — IMPORTS
"""
Imports for TypedDict and type hints.
"""
from typing import TypedDict, Literal, Any


#%% CELL 02 — SCHEMA DEFINITION
"""
Shape of each parameter entry in the registry.

Fields:
  label       — Human-readable name for reports/UI.
  tags        — Provenance tags (which file(s): BASE, tracked, sleap, pose, scored; plus "stimuli" if applicable).
  type        — Primitive storage type: "int" | "float" | "string" | "bool".
  unit        — Physical/logical unit: "frames","sec","mm","deg","px","unitless","fraction","state","classification","category" or None.
  role        — Semantic role: "binary" | "categorical" | "continuous".
  domain      — Legal values (list of categories or [min,max]) or None if unbounded.
  description — One-line explanation of the column.
"""
class ParamSpec(TypedDict, total=False):
	label: str
	tags: list[str]
	type: Literal["int","float","string","bool"]
	unit: str | None
	role: Literal["binary","categorical","continuous"]
	domain: list[Any] | None
	description: str


#%% CELL 03 — EXPORTS
"""
Public API.
"""
__all__ = ["ParamSpec"]

