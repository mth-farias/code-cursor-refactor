# path.py Refactoring Plan - COMPLETE ✅

**Date**: October 22, 2025  
**Status**: Planning phase complete, ready for execution  
**Estimated Time**: 6.5 hours implementation

---

## Planning Documents Summary

| Document | Purpose | Status | Lines |
|----------|---------|--------|-------|
| `README.md` | Overview and roadmap | ✅ Complete | 150 |
| `analysis.md` | Detailed structure breakdown | ✅ Complete | 520 |
| `decisions.md` | 6 architectural decisions (ADR-005 to ADR-010) | ✅ Complete | 580 |
| `implementation-plan.md` | Step-by-step execution plan | ✅ Complete | 1,200 |
| `validation-checklist.md` | 8 quality gates + integration tests | ✅ Complete | 650 |
| **Total** | **Complete planning package** | ✅ | **~3,100 lines** |

---

## Key Decisions Made

### ADR-005: Experiment Root Configuration
**Decision**: Auto-detect with optional override  
**Rationale**: Best user experience (works out-of-box) + power user flexibility

### ADR-006: Configure() Delegation Pattern
**Decision**: Use configure() for all workers (even functions)  
**Rationale**: Consistency across Config modules, future-proofing

### ADR-007: Discovery Function Testing
**Decision**: Mocked unit tests + deferred integration tests  
**Rationale**: Fast feedback now, comprehensive testing later

### ADR-008: Mixed PATH Mode Timing
**Decision**: Defer to Phase 5 (post-refactor)  
**Rationale**: Focus on core refactoring first, add complexity only when needed

### ADR-009: Environment Detection Strategy
**Decision**: Check for known modules (google.colab) + IPython kernel  
**Rationale**: Reliable, standard practice, already used in original code

### ADR-010: Backward Compatibility Guarantee
**Decision**: Strict backward compatibility (all imports preserved)  
**Rationale**: Zero user migration, safe refactoring

---

## Implementation Structure

### Workers (8 files)
1. **roots.py** (20 min) - Environment detection + root configuration
2. **folders.py** (30 min) - 13 folder path constants
3. **filename_policy.py** (20 min) - 8 suffix constants + registry
4. **name_builders.py** (45 min) - 10 name builder functions
5. **path_builders.py** (45 min) - 10 path builder functions
6. **discovery.py** (45 min) - 10 file discovery functions
7. **transforms.py** (30 min) - 7 transform utilities
8. **report.py** (30 min) - 4 diagnostic functions

### Coordinator (1 file)
9. **_path/__init__.py** (1 hour) - Orchestrates all workers, assembles PATH bundle

### Controller (1 file)
10. **path.py** (45 min) - Public API + backward compatibility layer

---

## Export Summary

| Category | Count | Examples |
|----------|-------|----------|
| Folders | 13 | pExperimentalFolder, pTracked, pDenoised, pResistant |
| Suffixes | 9 | SUFFIX_TRACKED, SUFFIX_DENOISED, KNOWN_SUFFIXES |
| Name Builders | 10 | tracked_name, denoised_name, resistant_name |
| Path Builders | 10 | tracked_path, denoised_path, resistant_path |
| Discovery | 10 | g_tracked, g_denoised, g_resistant, g_all_experiments |
| Transforms | 7 | parse_base_fly, swap_suffix, siblings |
| Reports | 4 | render_path_report, sanity_check_all_paths |
| Environment | 4 | is_colab, is_jupyter, detect_experiment_root |
| **TOTAL** | **67** | |

---

## Quality Gates (8 gates)

1. ✅ **Structure Compliance** - Controller + subpackage pattern, cell markers
2. ✅ **Export Completeness** - All 67 exports present
3. ✅ **Type Safety** - Correct types for all exports
4. ✅ **Immutability** - PATH is MappingProxyType
5. ✅ **Backward Compatibility** - All original imports work
6. ✅ **Environment Detection** - Auto-detect works correctly
7. ✅ **Function Behavior** - All functions produce correct output
8. ✅ **Documentation** - Comprehensive docstrings + verbose CELL 02

---

## NEW Features Added

Based on `BehaviorScoringRefactor_add_denoise.txt`:

1. **pDenoised** - New folder for denoised outputs
2. **pResistant** - New folder for resistant behavior outputs
3. **SUFFIX_DENOISED** - New suffix "_denoised"
4. **SUFFIX_RESISTANT** - New suffix "_resistant"
5. **denoised_name()** - New name builder
6. **resistant_name()** - New name builder
7. **denoised_path()** - New path builder
8. **resistant_path()** - New path builder
9. **g_denoised()** - New discovery function
10. **g_resistant()** - New discovery function

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Function signature mismatch | Test each worker independently before integration |
| Environment detection fails | Test in multiple environments (Colab, Jupyter, local) |
| Path separator issues | Use `pathlib.Path` exclusively |
| Missing backward compat | Explicit tests for all old import patterns |
| Complex worker dependencies | Implement in dependency order (roots → folders → ... → report) |

---

## Success Criteria

All must be met before commit:

- [x] Planning complete (4 docs)
- [ ] 8 workers implemented
- [ ] 1 coordinator implemented
- [ ] 1 controller implemented
- [ ] All 8 quality gates passed
- [ ] Integration test passed
- [ ] Config package exports PATH
- [ ] Backward compatibility validated
- [ ] No linter errors
- [ ] Atomic commit to feature branch
- [ ] Merged to main

---

## Next Steps (Execution)

### Phase 1: Setup (15 min)
```bash
git checkout -b refactor/path-py
mkdir codes/Config/_path
# Create 9 Python files
```

### Phase 2: Implement Workers (3 hours)
Work through each worker in dependency order, testing independently.

### Phase 3: Create Controller (45 min)
Implement `codes/Config/path.py` with backward compat layer.

### Phase 4: Validation (1 hour)
Run all 8 quality gates, fix any issues, run integration test.

### Phase 5: Commit & Merge (30 min)
Atomic commit, push, create PR, merge to main, cleanup.

---

## Post-Refactor Tasks

After successful merge:

1. **Update _handoff docs** (session-end.md, status-snapshot.md)
2. **Test GenerateExperiment.ipynb compatibility** (user's final checklist item)
3. **Implement Mixed PATH mode** (if needed in Phase 5+)
4. **Add integration tests with real fixtures**
5. **Implement stubbed report functions**

---

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Planning | 1.5h | ✅ Complete |
| Setup | 15min | Next |
| Workers | 3h | Pending |
| Controller | 45min | Pending |
| Validation | 1h | Pending |
| Commit | 30min | Pending |
| **Total** | **6.5h** | |

---

## References

- **Original File**: `references/original/Config/path.py` (692 lines)
- **Template**: `plans/config-refactor/03-params/` (param.py refactoring)
- **Patterns**: `_tools/playbook/01-architecture-patterns.md`
- **Workflow**: `_tools/playbook/02-refactoring-workflow.md`
- **Quality Gates**: `_tools/playbook/03-quality-gates.md`
- **Refactoring Guide**: `references/original/REFACTOR_GUIDE.md`
- **Context Notes**: `plans/config-refactor/02-context/CONTEXT_NOTES.md`

---

## Approval Status

**Reviewer**: @user  
**Status**: Awaiting approval to begin execution

---

## Questions Before Execution?

1. ✅ Strategy clear?
2. ✅ Timeline acceptable?
3. ✅ Risks understood?
4. ✅ Quality gates sufficient?

---

**Ready to begin Phase 1 (Setup)** 🚀

---

## Notes

- This refactoring follows the proven param.py pattern (successfully completed earlier)
- Main difference: path.py has functions (not just data), requiring function testing
- GenerateExperiment.ipynb compatibility testing deferred to post-refactor validation
- Mixed PATH mode deferred to Phase 5 (post-refactor enhancement)

---

**Status**: 📋 Planning Complete → 🚀 Ready for Execution  
**Next**: Begin Phase 1 (Setup) when approved

