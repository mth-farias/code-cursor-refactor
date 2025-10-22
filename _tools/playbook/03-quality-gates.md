# Quality Gates

**Status**: ✅ ESTABLISHED (extends REFACTOR_GUIDE.md Section 13)

**Prerequisites**: Read REFACTOR_GUIDE.md PR Checklist (Section 13)

---

## Overview

Quality gates must pass before moving to next phase or declaring work complete.

**Philosophy**: Multiple checkpoints catch issues early

**Base**: REFACTOR_GUIDE.md checklist (comprehensive!)  
**Extension**: Architecture pattern compliance (from this playbook)

---

## Gate 1: Structure Compliance

**From REFACTOR_GUIDE** (Base Standards):
- [ ] Cell 00 docstring with metadata and overview
- [ ] `from __future__ import annotations` immediately after module docstring
- [ ] Imports consolidated in Cell 01 (stdlib → typing → third-party → local)
- [ ] No unused imports (lint clean)
- [ ] Every later cell starts with docstring banner
- [ ] Section titles ALL CAPS, no ASCII art
- [ ] 2 blank lines between cells, 2 before/after titles, 1 inside
- [ ] Tabs only (no spaces)
- [ ] Line length ≤ 100 characters
- [ ] Double quotes for strings
- [ ] No stray globals or unused code paths

**Extension** (Architecture Patterns):
- [ ] If modular: Architecture note in CELL 00 describes controller role
- [ ] If modular: configure() pattern used for delegation
- [ ] If long CELL 02: Numbered subsections (02.1, 02.2) for organization
- [ ] CELL 02 contains ONLY user constants (no derivations, no logic)
- [ ] CELL 03 handles processing/delegation (imports + configure())
- [ ] CELL 04 assembles bundle (MappingProxyType)
- [ ] CELL 05 optional report (only consumes bundle)

**Verification**: Visual inspection + linter

---

## Gate 2: Documentation Quality

**From REFACTOR_GUIDE**:
- [ ] Module docstring complete (file path, overview)
- [ ] Functions have Google-style docstrings (Args/Returns/Raises/Notes)
- [ ] Type hints on all functions
- [ ] Constants have descriptive inline comments (domain role)
- [ ] Constants grouped under titled sections
- [ ] Comments explain "why" not "what" (no code restatements)
- [ ] No vague comments ("stuff", "data", "things")

**Extension** (Architecture Patterns):
- [ ] If modular: Architecture docstring explains pattern clearly
- [ ] If modular: Submodule purpose documented in each file
- [ ] configure() function has comprehensive docstring
- [ ] Numbered subsections have descriptive titles and docstrings
- [ ] Examples provided for complex helpers

**Verification**: Manual review, docstring coverage check

---

## Gate 3: Public API Compliance

**From REFACTOR_GUIDE**:
- [ ] Exactly one immutable bundle per module
- [ ] Bundle wrapped in MappingProxyType
- [ ] `__all__` lists only the bundle name
- [ ] No legacy aliases in public API
- [ ] Helpers stateless, policy-light, no silent fallback
- [ ] No mutating public bundles after definition

**Extension** (Architecture Patterns):
- [ ] Bundle keys match original module (NO BREAKING CHANGES!)
- [ ] Bundle structure is flat or shallow (avoid deep nesting)
- [ ] If modular: Subpackage exports via __init__.py only
- [ ] If modular: Workers don't cross-talk (import via parent)
- [ ] Helper functions accessible if needed (in bundle or as callables)

**Verification**: API comparison test (new vs original)

---

## Gate 4: Pattern Compliance (New!)

**Controller Pattern** (if modular):
- [ ] Main file 200-300 lines (orchestrator role)
- [ ] Subpackage name starts with underscore (_module/)
- [ ] Subpackage has __init__.py coordinator
- [ ] Workers are 4-5 focused modules (single responsibility)
- [ ] Worker files have clear, descriptive names (not worker_a, worker_b)
- [ ] configure() function in __init__.py handles delegation
- [ ] Main file doesn't know worker implementation details

**configure() Delegation**:
- [ ] Single function call passes all user inputs
- [ ] All CELL 02 constants passed to configure()
- [ ] Subpackage coordinates across workers
- [ ] Main controller stays simple (no complex logic)

**Bundle Assembly**:
- [ ] CELL 04 collects results from subpackage
- [ ] Uses unpacking (**_subpackage._BUNDLE) when appropriate
- [ ] Combines user inputs + derived results
- [ ] Clear organization (inputs separate from derived)

**Verification**: Pattern checklist, code review

---

## Gate 5: Testing & Validation (New!)

**Import Test**:
- [ ] Module imports without errors
- [ ] `from Config import MODULE` works
- [ ] No circular import errors
- [ ] All dependencies available

**API Compatibility Test**:
- [ ] Bundle has same keys as original module
- [ ] Spot-check: Key values match original (sample 5-10 keys)
- [ ] Bundle is immutable (try to modify, should raise error)
- [ ] __all__ exports work correctly

**Integration Test**:
- [ ] No broken imports elsewhere in codebase
- [ ] Config/__init__.py exports module correctly
- [ ] Module works with ExampleFiles data (if applicable)
- [ ] Report runs without errors (CELL 05 if present)

**Verification**: Test scripts, manual testing

---

## Gate 6: Code Quality

**From REFACTOR_GUIDE**:
- [ ] Lint passes clean (Ruff, mypy, etc.)
- [ ] No type errors
- [ ] Fail fast for invalid config (descriptive errors)
- [ ] Config never creates directories or touches filesystem
- [ ] No silent fallbacks in helpers (explicit > implicit)
- [ ] Sanity checks where policy could drift

**Extension**:
- [ ] If modular: Submodules independently testable
- [ ] No code duplication (DRY principle)
- [ ] Appropriate use of NumPy/Pandas vectorization
- [ ] Half-open intervals [start, end) for frame ranges

**Verification**: Linter output, manual review

---

## Phased Gate Checklist

### After Phase 1 (Analysis)
**Must have**:
- [ ] Module completely read and understood
- [ ] Major sections identified
- [ ] Dependencies documented
- [ ] Structure decision made (modular vs flat)

### After Phase 2 (Planning)
**Must have**:
- [ ] Refactoring plan documented
- [ ] API compatibility plan (no breaking changes)
- [ ] If modular: Subpackage structure designed
- [ ] Testing strategy defined

### After Phase 3 (Execution)
**Must pass**:
- [ ] Gate 1: Structure Compliance ✅
- [ ] Gate 2: Documentation Quality ✅
- [ ] Gate 4: Pattern Compliance ✅ (if modular)
- [ ] Gate 6: Code Quality (linters) ✅

### After Phase 4 (Validation)
**Must pass**:
- [ ] Gate 3: Public API Compliance ✅
- [ ] Gate 5: Testing & Validation ✅
- [ ] All integration tests passed ✅

### After Phase 5 (Integration)
**Must have**:
- [ ] Module integrated into Config
- [ ] No broken dependencies
- [ ] Documentation complete
- [ ] All gates passed ✅

**Cannot proceed without green light on ALL gates!**

---

## Quick Reference: Gate Summary

| Gate | Focus | When to Check | Blocker? |
|------|-------|---------------|----------|
| Gate 1 | Structure | After Phase 3 | ✅ Yes |
| Gate 2 | Documentation | After Phase 3 | ✅ Yes |
| Gate 3 | Public API | After Phase 4 | ✅ Yes |
| Gate 4 | Patterns | After Phase 3 | ✅ Yes |
| Gate 5 | Testing | After Phase 4 | ✅ Yes |
| Gate 6 | Code Quality | After Phase 3 | ✅ Yes |

**All gates are blockers** - must pass before moving forward!

---

## Examples from Successful Refactorings

### color.py (PASSED all gates ✅)
- ✅ Controller pattern applied correctly
- ✅ 11 constants passed via configure()
- ✅ 4 focused submodules (colormaps, processing, resolvers, report)
- ✅ Bundle keys match original (verified)
- ✅ Imports cleanly, report runs
- ✅ Linters pass

### experiment.py (PASSED all gates ✅)
- ✅ Controller pattern applied correctly
- ✅ 4 constants passed via configure()
- ✅ 4 focused submodules (periods, stimuli, time, report)
- ✅ Bundle keys match original (verified)
- ✅ Imports cleanly, report runs
- ✅ Linters pass

---

## Enforcement

**Who checks**: Developer (self-check) → Reviewer (peer check) → Tests (automated)

**When**: After each phase, before moving forward

**If gates fail**:
1. Document what failed
2. Fix issues
3. Re-run gate checks
4. Only proceed when ALL gates pass

**No exceptions**: Quality gates are non-negotiable

---

## Notes for Refinement

**TODO: Add during refactoring**:
- [ ] Automated gate checking scripts?
- [ ] Performance benchmarks (speed comparison)?
- [ ] Memory usage checks (any impact from modular structure)?
- [ ] Backward compatibility tests (more comprehensive)?

---

**Status**: Quality gates established, proven with 2 modules ✅

**Next**: Apply these gates during param.py refactoring

**Last Updated**: 2025-10-22

