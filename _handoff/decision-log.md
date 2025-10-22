# Decision Log - Config Package Refactoring

**Purpose**: Record all architectural decisions with rationale  
**Format**: ADR (Architecture Decision Record)  
**Status**: Living document (update when new decisions made)

---

## Overview

This log captures **why** decisions were made, not just **what** was decided.

**Current Decisions**: 14 ADRs (8 from Session 1, 6 from Session 2)

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

## ADR-009: Experiment Root Configuration (path.py)

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: path.py needs configurable experiment root, unlike param.py

### Decision

Use **auto-detect with optional override**:

```python
# Default behavior (auto-detect)
from Config.path import PATH
print(PATH["pExperimentalFolder"])  # Auto-detected

# Override if needed
from Config.path import configure
PATH = configure(root=Path("/custom/path"))
```

### Rationale

**Three Options Considered**:

1. **Argument required**: `configure(root: Path)` - Explicit but breaks consistency
2. **Global setter**: Two-step process, mutation feels wrong
3. **Auto-detect + optional override** ✅ - Best UX

**Why Option 3**:
- Works out-of-box for most users (Colab, Jupyter, local)
- Consistent with other modules (no-arg configure)
- Power users can override when needed
- Backward compatible (existing code works)

**Environment Detection**:
- Colab: `/content/drive/MyDrive/Experiments`
- Jupyter: `{cwd}/Experiments`
- Local: `{cwd}/Experiments`

### Outcome

Best user experience achieved  
Consistency with color.py/experiment.py maintained  
Flexibility for advanced use cases

### References

- `plans/config-refactor/04-path/decisions.md` (detailed rationale)
- `references/original/Config/path.py` (original auto-detect logic)

---

## ADR-010: Configure() Delegation for All Workers (path.py)

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: path.py has functions, not just data - should we still use configure()?

### Decision

Use `configure()` pattern **for all workers**, even function-only workers.

**Example**:
```python
# _path/name_builders.py
def configure() -> dict[str, callable]:
    return {
        "tracked_name": tracked_name,
        "scored_name": scored_name,
        # ... all 10 name builders
    }
```

### Rationale

**Three Options Considered**:

1. **configure() for all** ✅ - Consistent pattern
2. **Direct imports** - Simpler but inconsistent
3. **Hybrid** (data vs functions) - Pragmatic but inconsistent

**Why Option 1**:
- Consistency across all Config modules
- Single point for testing (test configure())
- Future-proof (easy to add configuration later)
- Minimal cost (wrapping is trivial)

**Cost vs Benefit**:
- Cost: Slight wrapping overhead
- Benefit: Complete consistency, easier to understand
- Verdict: Benefits outweigh costs

### Outcome

All 8 workers use configure() pattern  
Consistent API across entire Config package  
Easy to test and extend

### References

- ADR-004 (original configure() decision)
- `plans/config-refactor/04-path/decisions.md`

---

## ADR-011: Discovery Function Testing Strategy (path.py)

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: Discovery functions depend on file system - how to test?

### Decision

Use **dual testing strategy**:

1. **Unit Tests** (now): Mock file system for fast feedback
2. **Integration Tests** (Phase 5): Real fixtures for full validation

**Unit Test Example**:
```python
@patch('pathlib.Path.glob')
def test_g_tracked(mock_glob):
    mock_glob.return_value = [Path("fly1_tracked.csv")]
    result = g_tracked()
    assert len(result) == 1
```

### Rationale

**Three Options Considered**:

1. **Mock file system** - Fast but doesn't test real behavior
2. **Test fixtures** - Real but requires setup
3. **Hybrid (both)** ✅ - Best of both worlds

**Why Option 3**:
- Unit tests catch obvious errors quickly
- Integration tests catch subtle bugs
- Can implement unit tests now, integration later
- Pragmatic: right tool for each test level

**Deferred Work**:
- Integration tests with real fixtures → Phase 5
- Focus on refactoring now, comprehensive testing later

### Outcome

Fast feedback during refactoring  
Full validation deferred to appropriate time  
Pragmatic balance of speed and thoroughness

### References

- `plans/config-refactor/04-path/validation-checklist.md`

---

## ADR-012: Defer Mixed PATH Mode to Phase 5 (path.py)

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: Mixed PATH mode (Google Drive input + local output) adds complexity

### Decision

**Defer Mixed PATH mode to Phase 5** (post-refactor enhancement).

**Current Implementation**: Single experiment root  
**Future Implementation**: Separate input/output roots

### Rationale

**Three Options Considered**:

1. **Implement now** - Complete but adds complexity
2. **Defer to Phase 5** ✅ - Focus on core first
3. **Architecture now, implement later** - YAGNI

**Why Option 2**:
- Core refactoring is more important
- Need to validate basic functionality first
- Mixed PATH mode adds significant complexity
- Can add later without breaking changes

**Risk Mitigation**:
- Document requirement in planning
- Design API to be extensible
- Validate basic paths work first

**Phase 5 Tasks**:
- Implement separate input/output roots
- Add background sync detection
- Test GenerateExperiment.ipynb compatibility

### Outcome

Reduced complexity in refactoring  
Focus on core functionality  
Clear path for future enhancement

### References

- User note: "Mixed PATH mode... not implemented yet"
- `plans/config-refactor/04-path/decisions.md`

---

## ADR-013: Environment Detection Strategy (path.py)

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: Need to detect Colab vs Jupyter vs local for root path

### Decision

Use **module-based detection** + **IPython kernel check**:

```python
def is_colab() -> bool:
    try:
        import google.colab
        return True
    except ImportError:
        return False

def is_jupyter() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        return shell == "ZMQInteractiveShell"
    except NameError:
        return False
```

### Rationale

**Options Considered**:

1. **Check for known modules** ✅ - Simple and reliable
2. **Check environment variables** - Less reliable
3. **Check for IPython kernel** - Standard approach

**Why Option 1 + 3**:
- Module presence is definitive
- Widely used in the community
- Original code already uses this pattern
- Low risk, well-established

**No Breaking Changes**:
- Preserves original detection logic
- Just modularizes it into _path/roots.py

### Outcome

Reliable environment detection  
Follows community standards  
Backward compatible with original

### References

- `references/original/Config/path.py` (original detection)
- `_path/roots.py` (implementation location)

---

## ADR-014: Strict Backward Compatibility for path.py

**Date**: 2025-10-22 (Session 2)  
**Status**: ✅ Accepted  
**Context**: Must existing imports continue to work after refactoring?

### Decision

**Strict backward compatibility** - All 67 exports preserved at module level.

**Before (original)**:
```python
from Config.path import pTracked, tracked_name, g_tracked
```

**After (refactored)** - MUST STILL WORK:
```python
from Config.path import pTracked, tracked_name, g_tracked  # ✅ Works!
```

**Implementation**:
```python
# path.py (controller)
PATH = configure()
globals().update(PATH)  # Explode dict to module-level
__all__ = list(PATH.keys()) + ["PATH"]
```

### Rationale

**Three Options Considered**:

1. **Strict backward compatibility** ✅ - Zero user migration
2. **Allow breaking changes** - Cleaner but risky
3. **Hybrid (new + deprecated old)** - More maintenance

**Why Option 1**:
- Refactoring should not break existing code
- User trust (imports remain stable)
- No deprecation warnings to manage
- Aligns with REFACTOR_GUIDE.md principles

**Quality Gate 5**: Explicitly validates all 67 exports work

### Outcome

Zero user migration required  
All existing code continues to work  
Safe refactoring achieved

### References

- Quality Gate 5 (backward compatibility validation)
- `plans/config-refactor/04-path/validation-checklist.md`

---

## Decision Summary Table

### Session 1 Decisions (param.py)

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

### Session 2 Decisions (path.py)

| ADR | Decision | Status | Impact |
|-----|----------|--------|--------|
| 009 | Experiment Root Configuration | ✅ Accepted | High - User experience |
| 010 | Configure() for All Workers | ✅ Accepted | Medium - Consistency |
| 011 | Discovery Function Testing | ✅ Accepted | Medium - Testing strategy |
| 012 | Defer Mixed PATH Mode | ✅ Accepted | Medium - Complexity management |
| 013 | Environment Detection Strategy | ✅ Accepted | Medium - Reliability |
| 014 | Strict Backward Compatibility | ✅ Accepted | High - User trust |

---

## Future Decisions

Decisions to make for future work:

### Phase 5 (Post-Refactor Enhancements)
- [ ] Mixed PATH mode implementation details (if needed)
- [ ] Integration test fixture structure
- [ ] GenerateExperiment.ipynb integration strategy
- [ ] Full report.py diagnostic functions

### BehaviorClassifier Refactoring
- [ ] Worker breakdown for BehaviorClassifier
- [ ] Testing strategy for behavior algorithms
- [ ] Denoising module structure
- [ ] Resistant behavior detection architecture

---

## Decision Review Process

**When to add**: Any architectural choice that affects >1 file or has alternatives  
**When to update**: If decision needs revision or proves problematic  
**When to reference**: During similar decisions (e.g., path.py references param.py ADRs)

**Review Cadence**: 
- Before each major refactoring phase
- When patterns need adjustment
- When new requirements emerge

---

**Last Updated**: 2025-10-22, end of Session 2  
**Next Review**: When starting path.py execution (Session 3)

