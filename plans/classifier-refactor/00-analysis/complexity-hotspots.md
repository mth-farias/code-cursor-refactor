# BehaviorClassifier Complexity Hotspots

**Date**: 2025-10-22  
**Purpose**: Identify areas requiring extra attention during refactoring

---

## Complexity Dimensions

| Dimension | Metric | Risk Level |
|-----------|--------|------------|
| **Size** | Lines per file | High (3 files >1,000 lines) |
| **Algorithm** | Numeric computation | High (_classifier.py) |
| **I/O** | File operations | Medium (_qc, _main) |
| **Performance** | Speed-critical | High (_classifier.py) |
| **Testing** | Validation difficulty | High (algorithms, I/O) |

---

## Hotspot #1: `_classifier.py` (1,370 lines)

### Complexity Factors
⚠️ **Algorithm Complexity**: NumPy operations, optional Numba JIT  
⚠️ **Performance Critical**: Main classification loop  
⚠️ **Correctness Critical**: Behavior labels must be bit-perfect  
⚠️ **State Management**: Layer1/Layer2 processing with state

### Risk Level: **VERY HIGH** 🔴

### Attention Required
1. **Algorithm Validation**: Outputs must match original exactly
2. **Performance Testing**: No regression allowed (within 5%)
3. **Careful Extraction**: Don't break NumPy vectorization
4. **JIT Compatibility**: Ensure numba decorators still work
5. **Edge Cases**: NaN handling, boundary conditions

### Mitigation Strategy
- Create comprehensive test suite BEFORE refactoring
- Benchmark current performance
- Validate outputs at each refactoring step
- Keep performance-critical paths intact
- Consider keeping some hot loops as single functions

---

## Hotspot #2: `_qc_error_flag.py` (1,372 lines)

### Complexity Factors
⚠️ **I/O Heavy**: CSV writes, folder creation  
⚠️ **Error Handling**: Must handle file system failures  
⚠️ **QC Logic**: Complex rules for error/flag detection  
⚠️ **Report Generation**: Formatting and aggregation

### Risk Level: **HIGH** 🟡

### Attention Required
1. **I/O Testing**: Mock file system operations
2. **Error Paths**: Validate all error handling
3. **QC Rules**: Ensure rules remain consistent
4. **Report Format**: Outputs must match original format
5. **Folder Structure**: Respect PATH conventions

### Mitigation Strategy
- Separate logic from I/O (pure functions vs side effects)
- Create fixtures for testing
- Validate report outputs against known good outputs
- Test error handling paths explicitly

---

## Hotspot #3: `_main.py` (1,254 lines)

### Complexity Factors
⚠️ **Orchestration Logic**: Coordinates all modules  
⚠️ **Progress Reporting**: User feedback during execution  
⚠️ **Error Handling**: Must handle failures gracefully  
⚠️ **File Discovery**: CSV loading and validation  
⚠️ **Pipeline State**: Manages multi-step processing

### Risk Level: **HIGH** 🟡

### Attention Required
1. **Pipeline Flow**: Maintain execution order
2. **Error Recovery**: Don't break error handling
3. **Progress Feedback**: Keep user experience smooth
4. **Integration**: All modules must work together
5. **Backward Compatibility**: Existing notebooks must work

### Mitigation Strategy
- Extract orchestration logic from implementation
- Test pipeline stages independently
- Create integration test suite
- Validate with real-world notebooks

---

## Hotspot #4: `_utils.py` (1,001 lines)

### Complexity Factors
⚠️ **Foundation**: Everything depends on it  
⚠️ **Wide Usage**: Called by all modules  
⚠️ **Diverse Functions**: 60+ utility functions  
⚠️ **Label Management**: Critical for correctness

### Risk Level: **MEDIUM-HIGH** 🟡

### Attention Required
1. **Breaking Changes**: Any change affects all modules
2. **Function Grouping**: Must identify natural boundaries
3. **Backward Compatibility**: Preserve all function signatures
4. **Testing**: Must validate each utility independently

### Mitigation Strategy
- Refactor first (other modules depend on it)
- Keep backward compatibility strict
- Test each utility function independently
- Group by concern (labels, onsets, validation, etc.)

---

## Performance-Critical Sections

### 1. Classification Loop (_classifier.py)
```
Speed calculation → behavior labels → denoising → layer processing
```
**Risk**: Vectorization break → 10-100x slowdown  
**Mitigation**: Benchmark before/after, keep hot paths intact

### 2. DataFrame Operations (_qc_error_flag.py, _main.py)
```
CSV loading → validation → aggregation → writing
```
**Risk**: Memory issues with large datasets  
**Mitigation**: Profile memory usage, test with large files

### 3. Onset Detection (_utils.py)
```
Frame-by-frame analysis → onset finding → duration calculation
```
**Risk**: Performance regression on long recordings  
**Mitigation**: Benchmark with various dataset sizes

---

## Testing Complexity

### Algorithm Testing
**Challenge**: Bit-perfect outputs required  
**Solution**: Capture current outputs, validate against them

### I/O Testing
**Challenge**: File system dependencies  
**Solution**: Mock file operations, use fixtures

### Integration Testing
**Challenge**: Full pipeline must work  
**Solution**: Test with real notebooks, real data

### Performance Testing
**Challenge**: No regression allowed  
**Solution**: Benchmark suite, automated comparison

---

## Refactoring Complexity Estimate

| Module | Size | Algorithm | I/O | Perf | Test | Total Complexity |
|--------|------|-----------|-----|------|------|------------------|
| _utils | 1,001 | Low | Low | Med | Med | **Medium** 🟡 |
| _classifier | 1,370 | **High** | Low | **High** | **High** | **Very High** 🔴 |
| _qc | 1,372 | Med | **High** | Low | Med | **High** 🟡 |
| _main | 1,254 | Med | Med | Low | **High** | **High** 🟡 |
| _colab | 649 | Low | Med | Low | Low | **Low** 🟢 |

---

## Risk Mitigation Checklist

### Before Refactoring
- [ ] Create comprehensive test suite
- [ ] Benchmark current performance
- [ ] Capture current outputs (golden files)
- [ ] Document known edge cases
- [ ] Set up CI/CD for automated testing

### During Refactoring
- [ ] Test each worker independently
- [ ] Validate outputs at each step
- [ ] Run performance benchmarks frequently
- [ ] Keep notes on breaking changes
- [ ] Maintain backward compatibility

### After Refactoring
- [ ] Full integration test suite
- [ ] Performance comparison report
- [ ] Backward compatibility validation
- [ ] Documentation updates
- [ ] User testing with real notebooks

---

## Estimated Effort by Complexity

| Module | Base Effort | Complexity Factor | Total Estimate |
|--------|-------------|-------------------|----------------|
| _utils | 2h | 1.5x | **3 hours** |
| _classifier | 2.5h | 2.0x | **5 hours** |
| _qc | 2h | 1.5x | **3 hours** |
| _main | 2h | 1.5x | **3 hours** |
| _colab | 1h | 1.0x | **1 hour** |
| **Testing/Validation** | - | - | **3 hours** |
| **Total** | - | - | **18 hours** |

**Buffer**: Add 20-30% for unknowns → **22-24 hours total**

---

## Top Risks Summary

1. **Algorithm Correctness** (_classifier.py)
   - Risk: Wrong outputs
   - Impact: Very High
   - Mitigation: Bit-perfect validation

2. **Performance Regression** (_classifier.py)
   - Risk: Slower execution
   - Impact: High
   - Mitigation: Benchmark suite

3. **Breaking Changes** (_utils.py)
   - Risk: Other modules break
   - Impact: High
   - Mitigation: Strict backward compat

4. **Integration Failures** (_main.py)
   - Risk: Pipeline doesn't work
   - Impact: Very High
   - Mitigation: End-to-end tests

5. **I/O Errors** (_qc_error_flag.py)
   - Risk: File operations fail
   - Impact: Medium
   - Mitigation: Mock + fixtures

---

## Analysis Status

- [x] Complexity dimensions identified
- [x] Hotspots mapped
- [x] Performance-critical sections noted
- [x] Testing strategy outlined
- [x] Risk mitigation planned
- [x] Effort estimated
- [ ] Detailed function-level analysis
- [ ] Benchmark baseline captured
- [ ] Test fixtures created

**Next**: Begin Phase 2 (Decisions)

