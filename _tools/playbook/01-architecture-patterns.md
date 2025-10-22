# Architecture Patterns

**Status**: ✅ ESTABLISHED (proven in color.py and experiment.py)

**Prerequisites**: Read REFACTOR_GUIDE.md first

---

## Pattern 1: Controller + Subpackage Architecture

### When to Use

**Use modular subpackage when**:
- Module > 400 lines
- Natural separation of concerns exists (e.g., colormaps, time helpers, reports)
- Multiple responsibilities that can be isolated

**Keep flat when**:
- Module < 200 lines
- Single cohesive responsibility
- No clear split points

**Gray area (200-400 lines)**:
- Use judgment: Is it getting hard to navigate?
- Does it have distinct sections that could be separate?
- Would splitting improve clarity?

### Structure

```python
# Main controller file (module.py)
module.py               # 200-300 lines (orchestrator)

# Implementation subpackage
_module/                # Focused workers
    ├── __init__.py     # Coordinator (exports configure(), _BUNDLES)
    ├── component_a.py  # Single responsibility (e.g., colormaps)
    ├── component_b.py  # Another concern (e.g., time conversions)
    ├── component_c.py  # Processing logic
    └── report.py       # Optional: reporting/visualization
```

### Controller Responsibilities

**Main File** (module.py):
1. **CELL 00**: Module docstring + architecture note
2. **CELL 01**: Imports (including dynamic _module loading)
3. **CELL 02**: User constants ONLY (no derivations, no logic)
4. **CELL 03**: Import subpackage + call configure()
5. **CELL 04**: Assemble final bundle from subpackage results
6. **CELL 05**: Optional report (delegates to subpackage)

**Keep it simple**: Controller should read like a recipe, not a cookbook.

### Subpackage Responsibilities

**__init__.py** (Coordinator):
- Imports from sibling modules
- Exports configure() function
- Exports result bundles (_TIME, _COLORS, etc.)
- Exports _REPORT dict if applicable

**Worker Modules**:
- Single responsibility each
- Stateless functions (or classes if complex)
- No cross-talk (siblings import via parent)
- Return clean data structures

---

## Pattern 2: configure() Delegation

### Purpose

Pass all user inputs to subpackage in one clean call.

### Implementation

```python
# In main controller (CELL 03)
_experiment.configure(
    FRAME_RATE,
    EXPERIMENTAL_PERIODS,
    STIMULI,
    ALIGNMENT_STIM
)

# In _experiment/__init__.py
def configure(frame_rate, periods, stimuli, alignment):
    """Initialize all submodules with user parameters."""
    global _TIME, _PERIODS, _STIMULI, _REPORT
    
    # Delegate to workers
    _TIME = time.build_time_bundle(frame_rate)
    _PERIODS = periods.process_periods(periods, frame_rate)
    _STIMULI = stimuli.validate_stimuli(stimuli, alignment)
    _REPORT = {"render_experiment_report": report.render_experiment_report}
```

### Benefits

- **Single call**: All configuration in one place
- **Coordination**: Subpackage can orchestrate across workers
- **Clean interface**: Main controller doesn't know implementation details
- **Testing**: Easy to test configure() in isolation

### Anti-Pattern

❌ **Don't**: Import and call each worker individually
```python
# BAD: Controller knows too much
from ._experiment import time, periods, stimuli
time_bundle = time.build_time_bundle(FRAME_RATE)
period_bundle = periods.process_periods(...)
# etc.
```

✅ **Do**: Single configure() call
```python
# GOOD: Clean delegation
_experiment.configure(FRAME_RATE, PERIODS, STIMULI, ALIGNMENT)
```

---

## Pattern 3: Numbered Subsections

### Purpose

Organize long CELL 02 (USER INPUT) into logical groups.

### Pattern

```python
#%% CELL 02 — USER INPUT
"""
Overview of what's defined in this cell.
Subsections below organize related constants.
"""

#%% CELL 02.1 — GROUP COLORS POLICY
"""Specific topic 1"""
CONSTANT_A = "value"
CONSTANT_B = 42

#%% CELL 02.2 — STIMULI & SENTINELS
"""Specific topic 2"""
CONSTANT_C = {...}

#%% CELL 02.3 — BEHAVIOR ANCHORS
"""Specific topic 3"""
CONSTANT_D = {...}
```

### When to Use

- CELL 02 would be > 50 lines
- Multiple distinct categories of constants
- Want easy navigation (VS Code cell jumping)

### Naming

- Use descriptive subsection names (not 02a, 02b)
- ALL CAPS titles
- Brief docstring explaining each subsection

---

## Pattern 4: Dynamic Module Loading

### Purpose

Handle both script execution (`python module.py`) and module import (`from Config import MODULE`).

### Implementation

```python
#%% CELL 03 — PROCESSING & ASSEMBLY
"""Import and configure internal processing modules."""

import importlib
from pathlib import Path

# Determine correct import method
current_dir = Path(__file__).parent
subpackage_path = current_dir / "_subpackage"

if subpackage_path.exists():
    # Direct import when running as script
    import sys
    sys.path.insert(0, str(current_dir))
    _subpackage = importlib.import_module("_subpackage")
else:
    # Relative import when imported as module
    from . import _subpackage

# Configure subpackage
_subpackage.configure(USER_CONSTANT_A, USER_CONSTANT_B)
```

### Why Needed

- **Script mode**: `python color.py` → needs absolute import
- **Module mode**: `from Config import COLOR` → needs relative import
- **Robustness**: Works in both contexts

### Trade-off

- More complex than simple `from . import _subpackage`
- But necessary for flexibility (running reports, testing)

---

## Pattern 5: Bundle Assembly

### Purpose

Construct final public bundle from subpackage results.

### Implementation

```python
#%% CELL 04 — PUBLIC API
"""
Immutable public bundle: EXPERIMENT.
Combines user inputs and derived results from subpackage.
"""

_PUBLIC = {
    # User inputs (from CELL 02)
    "FRAME_RATE": FRAME_RATE,
    "EXPERIMENTAL_PERIODS": EXPERIMENTAL_PERIODS,
    "STIMULI": STIMULI,
    
    # Derived results (from subpackage)
    **_experiment._TIME,      # Unpack time bundle
    **_experiment._PERIODS,   # Unpack period bundle
    **_experiment._STIMULI,   # Unpack stimulus bundle
}

EXPERIMENT = MappingProxyType(_PUBLIC)
__all__ = ["EXPERIMENT"]
```

### Bundle Structure Patterns

**Flat preferred** (easy access):
```python
bundle["frame_rate"]        # ✅ Good
bundle["seconds_to_frames"] # ✅ Good
```

**Nested if necessary** (avoid deep nesting):
```python
bundle["hex"]["behavior"]["Jump"]  # ✅ OK (2 levels)
bundle["a"]["b"]["c"]["d"]         # ❌ Too deep
```

**Unpacking subpackage results**:
```python
# If subpackage returns {"key1": val1, "key2": val2}
**_subpackage._BUNDLE  # Unpacks into parent dict
```

---

## Real Examples

### Example 1: color.py (Controller)

**Structure**: 274 lines → 4 submodules
```
color.py (controller)
_color/
    ├── colormaps.py    (matplotlib colormap builders)
    ├── processing.py   (derive layer colors, build resolvers)
    ├── report.py       (visual report generation)
    └── resolvers.py    (runtime color lookup functions)
```

**Pattern application**:
- ✅ Controller orchestrates, subpackage implements
- ✅ configure() passes 11 user constants
- ✅ CELL 02 uses numbered subsections (02.1-02.7)
- ✅ Dynamic module loading
- ✅ Bundle assembled from _color._RESOLVERS and _color._COLORMAPS

### Example 2: experiment.py (Controller)

**Structure**: 230 lines → 4 submodules
```
experiment.py (controller)
_experiment/
    ├── periods.py      (process period durations → frames)
    ├── stimuli.py      (validate stimulus registry)
    ├── time.py         (frame/second conversion helpers)
    └── report.py       (render experiment summary)
```

**Pattern application**:
- ✅ Controller orchestrates, subpackage implements
- ✅ configure() passes 4 user constants
- ✅ CELL 02 uses numbered subsections (02.1-02.4)
- ✅ Dynamic module loading
- ✅ Bundle assembled from _experiment._TIME, _PERIODS, _STIMULI

**Consistency**: Both modules follow identical pattern! ✅

---

## Decision Matrix

**When should code live?**

| Code Type | Location | Example |
|-----------|----------|---------|
| User constants | Main CELL 02 | FRAME_RATE, BEHAVIOR colors |
| Processing logic | Subpackage workers | build_colormap(), validate_periods() |
| Coordination | Subpackage __init__ | configure() function |
| Final assembly | Main CELL 04 | Build MappingProxyType bundle |
| Reporting | Subpackage report.py | render_experiment_report() |

---

## Anti-Patterns

❌ **Don't duplicate logic** in controller
```python
# BAD: Controller does processing
derived_value = USER_CONST * 2 + 10  # Logic in controller
```
```python
# GOOD: Delegate to subpackage
derived_value = _subpackage.compute_value(USER_CONST)
```

❌ **Don't mix user input with derivations** in CELL 02
```python
# BAD: CELL 02 has logic
FRAME_RATE = 60
PERIOD_FRAMES = PERIOD_SEC * FRAME_RATE  # Derivation!
```
```python
# GOOD: Pure constants in CELL 02, logic in CELL 03
FRAME_RATE = 60
PERIOD_SEC = 300.0
# ... then in CELL 03:
_experiment.configure(FRAME_RATE, PERIOD_SEC)
```

❌ **Don't create circular imports**
```python
# BAD: Main imports worker, worker imports main
# module.py
from ._subpackage import worker

# _subpackage/worker.py  
from ..module import CONSTANT  # Circular!
```
```python
# GOOD: Pass constants via configure()
# module.py
_subpackage.configure(CONSTANT)

# _subpackage/worker.py
# Receives CONSTANT as parameter, no import needed
```

---

## Pattern Summary

| Pattern | When | Proven | Benefits |
|---------|------|--------|----------|
| Controller + Subpackage | Module > 400 lines | ✅ Yes (2x) | Separation, testability |
| configure() Delegation | Always with subpackage | ✅ Yes (2x) | Clean interface |
| Numbered Subsections | Long CELL 02 | ✅ Yes (2x) | Navigation, organization |
| Dynamic Loading | Script + import contexts | ✅ Yes (2x) | Flexibility |
| Bundle Assembly | Always | ✅ Yes (all) | Immutable API |

---

## Next Steps

**For param.py and path.py**:
- Apply these proven patterns
- Document any variations we discover
- Refine patterns based on experience
- Add new patterns to this document

---

**Status**: Patterns established and proven ✅

**Examples**: See `../Config/color.py` and `../Config/experiment.py`

**Last Updated**: 2025-10-22

