# path.py Refactoring Plan

**Target**: `references/original/Config/path.py` (692 lines)  
**Goal**: Transform monolithic file into modular controller + subpackage pattern  
**Status**: Planning phase  
**Template**: Following param.py refactoring pattern

---

## Documents in This Directory

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Overview (this file) | ✅ Complete |
| `analysis.md` | Detailed breakdown of path.py structure | 🔄 Next |
| `decisions.md` | Architectural decisions (ADRs) | 📝 Pending |
| `implementation-plan.md` | Step-by-step execution plan | 📝 Pending |
| `validation-checklist.md` | Quality gates and testing | 📝 Pending |

---

## Key Differences from param.py

| Aspect | param.py | path.py |
|--------|----------|---------|
| **Nature** | Pure data (60 parameters) | Mixed (paths + ~50 functions) |
| **Complexity** | Low (just data dicts) | Medium (logic + data + I/O) |
| **User Config** | None (pure registry) | Configurable root path |
| **Testing** | Assert counts | Test functions + validate paths |
| **Workers** | 6 (by file type) | 7-8 (by responsibility) |

---

## High-Level Strategy

### 1. **Worker Breakdown** (by responsibility)
```
_path/
├── __init__.py          # Coordinator (configure pattern)
├── roots.py             # Experiment root + environment detection
├── folders.py           # All folder constants (~20 paths)
├── filename_policy.py   # Suffixes + KNOWN_SUFFIXES
├── name_builders.py     # Name construction functions (tracked_name, etc.)
├── path_builders.py     # Path construction functions (tracked_path, etc.)
├── discovery.py         # Glob functions (g_tracked, etc.)
├── transforms.py        # Helper utilities (swap_suffix, parse_base_fly, siblings)
└── report.py            # Diagnostics (missing_folders, sanity_checks)
```

### 2. **Key Principles** (from param.py success)
- ✅ Controller + subpackage pattern
- ✅ Configure() delegation for consistency
- ✅ Verbose CELL 02 explanation
- ✅ Numbered subsections where needed
- ✅ Independent worker testing
- ✅ Atomic commit after validation

### 3. **New Challenges** (unique to path.py)
- **Configurable root**: `pExperimentalFolder` is runtime-dependent
- **Environment detection**: Colab vs local vs template mode
- **Function testing**: Need to test logic, not just data
- **Path validation**: Optional (for diagnostics, not enforced)
- **Mixed PATH mode**: Separate input/output roots (future consideration)

---

## Execution Phases

### Phase 1: Analysis & Planning
- [ ] Analyze path.py structure (analysis.md)
- [ ] Document architectural decisions (decisions.md)
- [ ] Create detailed implementation plan (implementation-plan.md)
- [ ] Define quality gates (validation-checklist.md)

### Phase 2: Implementation
- [ ] Create feature branch: `refactor/path-py`
- [ ] Implement 8 workers incrementally
- [ ] Test each worker independently
- [ ] Create controller (path.py)

### Phase 3: Validation
- [ ] Run quality gates
- [ ] Validate backward compatibility
- [ ] Test environment detection
- [ ] Verify all ~50 exports work

### Phase 4: Integration
- [ ] Update Config/__init__.py to export PATH
- [ ] Run integration tests
- [ ] Atomic commit
- [ ] Merge to main

### Phase 5: Future (Post-Refactor)
- [ ] Test GenerateExperiment.ipynb compatibility
- [ ] Add Mixed PATH mode if needed
- [ ] Enhance environment detection

---

## Success Criteria

1. ✅ path.py refactored into 8 modular files
2. ✅ All ~50 exports preserved (backward compatible)
3. ✅ All quality gates passed
4. ✅ Independent worker tests passing
5. ✅ Config package exports PATH
6. ✅ Clean git history (atomic commit)

---

## Timeline Estimate

Based on param.py experience (4 hours):

- **Analysis & Planning**: 1.5 hours (more complex than param.py)
- **Implementation**: 4 hours (8 workers, more logic)
- **Validation**: 1 hour (function testing)
- **Total**: ~6.5 hours

---

## References

- **Template**: `plans/config-refactor/03-params/` (param.py refactoring)
- **Original**: `references/original/Config/path.py` (692 lines)
- **Patterns**: `_tools/playbook/01-architecture-patterns.md`
- **Workflow**: `_tools/playbook/02-refactoring-workflow.md`
- **Quality Gates**: `_tools/playbook/03-quality-gates.md`

---

**Status**: Ready to begin analysis phase  
**Next**: Create analysis.md

