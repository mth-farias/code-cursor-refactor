# Decision Log - Config Package Refactoring

**Purpose**: Record all architectural decisions with rationale  
**Format**: ADR (Architecture Decision Record)  
**Status**: Living document (update when new decisions made)

---

## Overview

This log captures **why** decisions were made, not just **what** was decided.

**Current Decisions**: 8 ADRs

---

## ADR-001: Use Controller + Subpackage Pattern

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: param.py was 714 lines, hard to navigate and test

### Decision

Refactor monolithic files into:
```
module.py (controller)
    ↓ imports
_module/ (subpackage)
    ├── __init__.py (coordinator)
    ├── worker1.py
    ├── worker2.py
    └── report.py
```

### Rationale

**Pros**:
- Focused, single-purpose modules (~100 lines each)
- Independently testable workers
- Clear separation of concerns
- Easier to navigate and understand
- Pattern already proven in experiment.py and color.py

**Cons**:
- More files to manage
- Need to understand subpackage structure
- Slightly more complex import path

**Alternatives Considered**:
1. Keep monolithic (rejected - too hard to maintain)
2. Split into separate top-level files (rejected - loses cohesion)
3. Use classes instead of modules (rejected - not pythonic for data)

### Outcome

Applied to param.py: 714 lines → 9 modular files  
**Success**: All quality gates passed, much easier to work with

### References

- `_tools/playbook/01-architecture-patterns.md`
- `codes/Config/param.py` (implementation)
- `codes/Config/_param/` (subpackage)

---

## ADR-002: Remove "Noisy" from Behavior_Denoised Domain

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: Original param.py had "Noisy" in Behavior_Denoised domain

### Decision

Remove "Noisy" from `Behavior_Denoised` parameter domain.

**Before**:
```python
"domain": ["Jump", "Walk", "Stationary", "Freeze", "Resistant_Freeze", "Noisy"]
```

**After**:
```python
"domain": ["Jump", "Walk", "Stationary", "Freeze", "Resistant_Freeze"]
```

### Rationale

"Noisy" is not a real behavioral category. It's a NaN placeholder used during gap-filling in the denoising algorithm. Including it in the domain:
- Misleads users about valid categories
- Suggests it's a legitimate classification
- Creates confusion about data quality

**Actual behavior**: "Noisy" marks frames with insufficient data, not a behavior type.

### Outcome

Quality gate specifically validates "Noisy" removal  
Schema now accurately reflects valid behavioral categories

### References

- User requirement: "remove Noisy from final product"
- `plans/config-refactor/03-params/decisions.md`
- `codes/Config/_param/scored.py` (implementation)

---

## ADR-003: Verbose CELL 02 Explanation for Empty Sections

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: Pure-data modules like param.py have no user constants

### Decision

Include CELL 02 even when empty, with verbose explanation:

```python
#%% CELL 02 — USER CONSTANTS
"""
No user constants needed for [module].

Why Empty?
    [Detailed explanation of why this cell exists but is empty]
    Pattern consistency requires CELL 02 even when empty.
"""
# (intentionally empty - pure registry)
```

### Rationale

**Pattern Consistency**: All modules should follow the same cell structure  
**Explicit Reasoning**: Explain why empty (not an oversight)  
**Educational**: Helps future developers understand design

**Alternative**: Skip CELL 02 entirely when empty  
**Rejected**: Breaks pattern consistency, creates confusion

### Outcome

Applied to param.py controller and all workers  
Clear communication that emptiness is intentional, not a mistake

### References

- User requirement: "use more verbose explanation for CELL 02"
- `codes/Config/param.py` (example)
- `_tools/playbook/01-architecture-patterns.md`

---

## ADR-004: Apply Configure() Delegation Even for Pure Data

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: param.py is pure data (no user-configurable runtime behavior)

### Decision

Use `configure()` pattern for **all** modules, even pure-data registries.

```python
# param.py (controller)
_param = importlib.import_module("_param")
PARAM = _param.configure()  # Delegate to subpackage

# _param/__init__.py (coordinator)
def configure() -> MappingProxyType:
    """Assemble and return complete PARAM registry"""
    return MappingProxyType({...})
```

### Rationale

**Consistency Over Optimization**: Uniform API across all Config modules  
**Future-Proofing**: Easy to add configuration later if needed  
**Clear Contract**: All modules expose data via `configure()`

**Alternative**: Direct assignment for pure data  
**Rejected**: Creates two different patterns, reduces consistency

### Outcome

All Config modules now use identical import/configure pattern  
No need to remember "which modules use which pattern"

### References

- Adapted from experiment.py and color.py patterns
- `codes/Config/_param/__init__.py` (implementation)

---

## ADR-005: Use Numbered Subsections for Fine-Grained Organization

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: Large sections need internal organization without adding cells

### Decision

Use numbered subsections within cells:

```python
#%% CELL 03 — MAIN SECTION
#%% CELL 03.1 — First Subsection
#%% CELL 03.2 — Second Subsection
```

### Rationale

**Granular Organization**: Break large sections without excessive cells  
**Visual Chunking**: Easy to see subsection boundaries  
**Flexibility**: Can add/remove subsections without renumbering cells

**Alternative**: Create more cells (03, 04, 05...)  
**Rejected**: Cells should be for major sections, not every small grouping

### Outcome

Used in larger worker files (scored.py, sleap.py)  
Improved readability without cell proliferation

### References

- `_tools/playbook/01-architecture-patterns.md`

---

## ADR-006: Atomic Commits After Full Validation

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: How to structure git commits during refactoring

### Decision

Create **one atomic commit** after:
1. All workers implemented
2. All quality gates passed
3. Full integration validated
4. Config/__init__.py updated

**Not**: Incremental commits per worker.

### Rationale

**Clean History**: One commit = one complete feature  
**Easy Rollback**: Can revert entire refactoring cleanly  
**Clear Semantics**: Commit message describes whole change  
**Quality Assurance**: Nothing committed until fully validated

**Alternative**: Commit each worker as created  
**Rejected**: Creates noisy history, harder to rollback, incomplete features

### Outcome

Two clean commits so far:
1. "refactor(Config): modularize param.py"
2. "chore: reorganize workspace with _tools/ for methodology"

Both represent complete, validated changes.

### References

- User requirement: "commit at end after all validations pass"
- `_tools/playbook/02-refactoring-workflow.md`

---

## ADR-007: Separate Methodology into _tools/

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: Where to put playbook and universal kits

### Decision

Create `_tools/` directory structure:
```
_tools/
├── playbook/       # Project-specific patterns
└── kits/           # Universal workflow kits
```

Separate from:
- `codes/` (source code)
- `tools/` (executable scripts)
- `plans/` (project plans)

### Rationale

**Clear Separation**:
- `_tools/` = HOW we work (methodology)
- `tools/` = WHAT we execute (scripts)
- `codes/` = Production code

**Logical Grouping**:
- kits/ = Universal, reusable
- playbook/ = Project-specific

**Benefits**:
- Single location for all "how we work" docs
- Easy to copy kits to other projects
- Underscore prefix groups with _archive/ and _handoff/
- Clean workspace organization

**Alternative**: Keep playbook in codes/  
**Rejected**: Mixes methodology with source code

### Outcome

Clean separation achieved  
Easy to find all methodology in one place

### References

- User suggestion: "move playbook to _tools/"
- `_tools/README.md`

---

## ADR-008: Keep Commit Messages Concise

**Date**: 2025-10-22 (Session 1)  
**Status**: ✅ Accepted  
**Context**: Verbosity vs brevity in commit messages

### Decision

Use **concise commit messages**:
- Short subject line (50-70 chars)
- Optional body for details
- No verbose bullet lists in commit itself

**Example**:
```
refactor(Config): modularize param.py
```

Not:
```
refactor(Config): modularize param.py

- Created 9 worker modules
- Added schema.py for TypedDict
- Implemented coordinator pattern
- Added report generation
[... 20 more lines]
```

### Rationale

**User Preference**: Explicit request for "low verbosity"  
**Git Best Practice**: Short subject, details in PR/documentation  
**Readability**: `git log --oneline` stays readable  
**Documentation**: Details belong in handoff/plans, not commits

**Alternative**: Verbose commit messages with full details  
**Rejected**: User preference + clutters git history

### Outcome

Two concise commits:
- "refactor(Config): modularize param.py"
- "chore: reorganize workspace with _tools/ for methodology"

Clean git log, details captured in handoff docs.

### References

- User requirement: "for commit messages keep verbosity low"
- Git log output

---

## Decision Summary Table

| ADR | Decision | Status | Impact |
|-----|----------|--------|--------|
| 001 | Controller + Subpackage Pattern | ✅ Accepted | High - Core architecture |
| 002 | Remove "Noisy" from Domain | ✅ Accepted | Medium - Data quality |
| 003 | Verbose CELL 02 Explanation | ✅ Accepted | Low - Documentation |
| 004 | Configure() for All Modules | ✅ Accepted | Medium - API consistency |
| 005 | Numbered Subsections | ✅ Accepted | Low - Code organization |
| 006 | Atomic Commits | ✅ Accepted | Medium - Git workflow |
| 007 | _tools/ Separation | ✅ Accepted | Medium - Workspace org |
| 008 | Concise Commit Messages | ✅ Accepted | Low - Git history |

---

## Future Decisions

Decisions to make for path.py refactoring:

- [ ] Worker breakdown strategy for path.py
- [ ] How to handle experiment folder maps (similar to param groups?)
- [ ] Path derivation helper functions (where do they go?)
- [ ] Testing strategy for path resolution
- [ ] Mixed PATH mode handling (Google Drive + local)

---

## Decision Review Process

**When to add**: Any architectural choice that affects >1 file or has alternatives  
**When to update**: If decision needs revision or proves problematic  
**When to reference**: During similar decisions (e.g., path.py will reference param.py ADRs)

---

**Last Updated**: 2025-10-22, end of Session 1  
**Next Review**: When starting path.py refactoring

