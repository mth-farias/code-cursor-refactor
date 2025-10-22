# ADR-001: Controller + Subpackage Architecture Pattern

**Date**: 2025-10-22  
**Status**: Accepted  
**Deciders**: Team

---

## Context

We're refactoring large Config modules (400-700 lines) to be more maintainable and modular.

**Problem**: Monolithic files difficult to navigate, test, and maintain:
- param.py: 714 lines (CSV schema registry)
- path.py: 692 lines (folder map and filename API)
- Original color.py: ~350 lines (before refactoring)
- Original experiment.py: ~500 lines (before refactoring)

**Question**: What architectural pattern should we use for splitting large modules?

---

## Decision

We adopt the **Controller + Subpackage** architecture pattern for Config modules > 400 lines.

### Pattern Structure

```
module.py                  # Controller (200-300 lines)
_module/                   # Implementation subpackage
    ├── __init__.py        # Coordinator (exports configure())
    ├── component_a.py     # Focused worker (single responsibility)
    ├── component_b.py     # Another worker
    ├── component_c.py     # Processing logic
    └── report.py          # Optional reporting
```

### Key Principles

1. **Controller orchestrates, workers implement**
   - Main file stays simple (recipe, not cookbook)
   - CELL 02: User constants ONLY
   - CELL 03: Import + configure()
   - CELL 04: Assemble bundle

2. **Single configure() call**
   - Pass all user inputs in one function
   - Subpackage coordinates across workers
   - Clean interface (controller doesn't know implementation details)

3. **Focused workers**
   - One responsibility per module (4-5 modules typical)
   - No cross-talk (siblings import via parent)
   - Stateless, testable functions

4. **Bundle assembly**
   - Collect results from subpackage
   - Unpack worker bundles (**_worker._BUNDLE)
   - Immutable MappingProxyType

---

## Alternatives Considered

### Alternative 1: Keep Monolithic
**Pros**:
- Simple (everything in one file)
- No import complexity
- Familiar

**Cons**:
- Hard to navigate (600+ lines)
- Hard to test (everything coupled)
- Poor separation of concerns
- Doesn't scale

**Rejected**: Monolithic doesn't meet maintainability goals for large modules

### Alternative 2: Flat Split (Multiple Top-Level Files)
**Structure**:
```
param_base.py
param_tracked.py
param_scored.py
```

**Pros**:
- Simple import structure
- Clear file boundaries

**Cons**:
- No clear orchestration
- Coordination scattered across files
- How to assemble final bundle? (which file owns it?)
- No single entry point

**Rejected**: Lacks coordination and assembly point

### Alternative 3: Functional Decomposition (No Controller)
**Structure**:
```
_param/__init__.py  # Everything here
_param/base.py
_param/tracked.py
```

**Pros**:
- No main file needed
- Direct imports

**Cons**:
- Where do user constants live? (scattered?)
- Where is final bundle assembled?
- No clear "entry point" for understanding
- Breaks REFACTOR_GUIDE convention (modules export bundles)

**Rejected**: Doesn't fit Config package conventions

---

## Rationale

### Why Controller + Subpackage?

**1. Proven Success** ✅
- color.py: 350 → 274 lines + _color/ (4 workers)
- experiment.py: 500 → 230 lines + _experiment/ (4 workers)
- Both follow identical pattern → consistency

**2. Maintainability** ✅
- Controller is easy to read (< 300 lines)
- Workers are focused (< 200 lines each)
- Clear separation of concerns

**3. Testability** ✅
- Workers independently testable
- configure() is single coordination point
- Mock subpackage for controller tests

**4. Consistency with REFACTOR_GUIDE** ✅
- Maintains cell structure (00, 01, 02, 03, 04, 05)
- Public API stays clean (one bundle)
- No breaking changes to existing API

**5. Scalability** ✅
- Add new workers without touching controller
- Subpackage grows independently
- Clear extension points

**6. Discoverability** ✅
- Main file shows "what" (user constants)
- Subpackage shows "how" (implementation)
- New developers: read controller first, then dive deeper

---

## Consequences

### Positive

**For Developers**:
- ✅ Easier to navigate (jump to relevant worker)
- ✅ Faster to understand (read controller overview)
- ✅ Safer to modify (changes isolated to workers)
- ✅ Simpler to test (test workers independently)

**For Codebase**:
- ✅ Consistency (same pattern across Config modules)
- ✅ No API breakage (bundles look identical externally)
- ✅ Better separation of concerns
- ✅ Scales to larger modules (path.py, param.py)

### Negative

**Complexity**:
- ❌ More files (1 main + 5-6 subpackage files)
- ❌ Import complexity (dynamic loading for script vs module)
- ❌ Learning curve (need to understand pattern)

**Overhead**:
- ❌ Initial setup time (create subpackage structure)
- ❌ More ceremony (configure(), bundle unpacking)

### Mitigation

**For Complexity**:
- Document pattern clearly (01-architecture-patterns.md) ✅
- Provide examples (color.py, experiment.py) ✅
- Use consistent naming (_module/, configure())

**For Overhead**:
- Template/skeleton for new modules (reduce setup time)
- Proven pattern reduces decision-making
- Quality gates ensure consistency

---

## Comparison: Before vs After

### Original (Monolithic)

```python
# module.py (600+ lines)
"""Everything in one file"""

# User constants
CONST_A = 1
CONST_B = 2

# Processing logic (section 1)
def build_something(): ...

# Processing logic (section 2)
def validate_something(): ...

# Processing logic (section 3)
def compute_something(): ...

# Assembly
bundle = {...}  # 100+ lines of assembly
```

**Issues**: Hard to navigate, coupled concerns, poor testability

### Refactored (Controller + Subpackage)

```python
# module.py (250 lines)
"""Controller: orchestrates configuration"""

CONST_A = 1
CONST_B = 2

_module.configure(CONST_A, CONST_B)
BUNDLE = MappingProxyType({**_module._RESULTS})

# _module/__init__.py (50 lines)
def configure(a, b):
    _RESULTS.update(worker_a.build(a))
    _RESULTS.update(worker_b.validate(b))

# _module/worker_a.py (120 lines)
def build(value): ...  # Focused implementation

# _module/worker_b.py (80 lines)
def validate(value): ...  # Focused implementation
```

**Benefits**: Clear structure, focused files, testable workers

---

## When to Apply This Pattern

**Always use if**:
- Module > 400 lines
- Natural separation of concerns exists

**Consider if**:
- Module 200-400 lines AND getting unwieldy
- Multiple distinct responsibilities

**Don't use if**:
- Module < 200 lines
- Single cohesive responsibility
- No clear split points

**Exceptions**: None identified yet (revisit after param.py and path.py)

---

## Review Schedule

**Review After**: param.py and path.py refactoring complete

**Questions to Answer**:
1. Did pattern scale to param.py (714 lines)?
2. Did pattern fit path.py (692 lines, different concerns)?
3. Any new issues discovered?
4. Any refinements needed?

**Next Review**: After Config refactoring complete (estimate: +2-3 weeks)

---

## References

- REFACTOR_GUIDE.md (base standards)
- 01-architecture-patterns.md (pattern details)
- codes/Config/color.py (example 1)
- codes/Config/experiment.py (example 2)
- plans/config-refactor/01-discussion/audit-and-brainstorm.md (pattern extraction)

---

**Status**: Accepted and proven ✅

**Supersedes**: None (first ADR for Config refactoring)

**Last Updated**: 2025-10-22

