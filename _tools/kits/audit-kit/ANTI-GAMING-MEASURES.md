# Anti-Gaming Measures

**Version**: 1.0.0  
**Purpose**: Detect and prevent shortcuts, gaming, and quality violations  
**Enforcement**: Multi-layer validation

---

## Purpose

Audits are only valuable if honest. Gaming undermines trust.

**This document**: Red flags that indicate gaming + countermeasures

**Based on**: 4-layer quality enforcement (00-know-how/planning/04-quality-enforcement.md)

---

## Red Flags

### Category: Selective Auditing

**Red Flag 1**: File count doesn't match directory count
- **Indicates**: Cherry-picking files
- **Detection**: Manual directory count vs audit output
- **Countermeasure**: Require automated scan, no manual selection

**Red Flag 2**: "Important files" subset selected
- **Indicates**: Avoiding problematic files
- **Detection**: No clear selection criteria in plan
- **Countermeasure**: Require "all files" or specific exclusion rules

**Red Flag 3**: Gaps in file numbering or ordering
- **Indicates**: Skipped files
- **Detection**: Sequential analysis of outputs
- **Countermeasure**: Require complete lists, sorted

---

### Category: Evidence Fabrication

**Red Flag 4**: Claims without citations
- **Indicates**: Assumptions presented as facts
- **Detection**: Search for claims without (file:line) references
- **Countermeasure**: Template requires evidence field

**Red Flag 5**: Vague evidence ("somewhere in code")
- **Indicates**: Didn't actually verify
- **Detection**: Evidence not specific enough to verify
- **Countermeasure**: Require file:line format

**Red Flag 6**: Too many "SUCCESS" with no failures
- **Indicates**: Not actually testing or hiding failures
- **Detection**: Statistical anomaly (real systems have some failures)
- **Countermeasure**: Validate sample of "success" items

---

### Category: Gate Bypassing

**Red Flag 7**: Phases completed too quickly
- **Indicates**: Skipped validation or testing
- **Detection**: Time spent vs expected duration
- **Countermeasure**: Spot-check outputs for completeness

**Red Flag 8**: All gates passed without issues
- **Indicates**: Not actually validating
- **Detection**: Real audits find some gate issues
- **Countermeasure**: Review gate criteria application

**Red Flag 9**: Proceeding with failed gate
- **Indicates**: Ignoring quality standards
- **Detection**: Phase status tracking
- **Countermeasure**: Hard requirement - can't proceed with failed gate

---

### Category: Result Manipulation

**Red Flag 10**: Statuses changed from earlier phases
- **Indicates**: Editing history to look better
- **Detection**: Compare phase outputs for same item
- **Countermeasure**: Immutable phase outputs (don't edit previous)

**Red Flag 11**: Contradictions between phases not resolved
- **Indicates**: Not cross-referencing properly
- **Detection**: Automated contradiction check
- **Countermeasure**: Require reconciliation phase

**Red Flag 12**: Perfect metrics (100% everything)
- **Indicates**: Faked data or selective scope
- **Detection**: Real systems aren't perfect
- **Countermeasure**: Expect some failures, document them

---

## Countermeasures (4 Layers)

### Layer 1: Declarative (This Document)

**Mechanism**: Explicitly state what's forbidden
**Strength**: Clear expectations
**Limitation**: Can be ignored

### Layer 2: Structural (Templates)

**Mechanism**: Templates require evidence fields
**Strength**: Can't submit without filling fields
**Limitation**: Can fill with fake data

**Enhancement**: Templates include validation examples showing what real evidence looks like

### Layer 3: Procedural (Gates)

**Mechanism**: Gates check objective criteria
**Strength**: Human verification at checkpoints
**Limitation**: Requires validator time

**Enhancement**: Automate validation where possible (file counts, JSON validity)

### Layer 4: Meta (Cross-Reference)

**Mechanism**: Phase 6 validates all previous phases
**Strength**: Can't game without faking everything
**Limitation**: Only catches at end

**Enhancement**: Make cross-references easy to verify (clear format, specific citations)

---

## Validation Techniques

### Technique 1: Count Matching

**Method**: Sum of categories must equal total
**Example**: SUCCESS + ERRORS + SKIPPED must = TOTAL FILES
**Detects**: Hidden items, uncounted failures

### Technique 2: Sampling

**Method**: Manually verify random sample of findings
**Example**: Pick 5 random "SUCCESS" items, verify they actually work
**Detects**: Fabricated results

### Technique 3: Reproducibility

**Method**: Re-run phase, compare results
**Example**: Re-scan directory, compare file lists
**Detects**: Inconsistent process, selective results

### Technique 4: Cross-Phase Validation

**Method**: Same item checked in multiple phases
**Example**: File exists (Phase 1) + imports (Phase 2) + used (Phase 3)
**Detects**: Contradictions, fabricated status

---

## Self-Check Questions

**Before submitting any phase**:

- [ ] Did I test/scan ALL items in scope?
- [ ] Did I document ALL errors found?
- [ ] Can I cite evidence for every finding?
- [ ] Would someone else get same results?
- [ ] Did I follow the phase rule strictly?
- [ ] Did all gate criteria pass?

**If "no" to any**: Fix before proceeding

---

## Gaming Scenarios (Real Examples)

### Scenario 1: The "Probably Works" Shortcut

**What happened**: Marked 50 files as "working" without testing  
**Justification**: "They're simple, they should work"  
**Detection**: Phase 2 tested 0 files but reported 50 success  
**Caught by**: Count mismatch (tested ≠ reported)

**Lesson**: Test everything, no exceptions

---

### Scenario 2: The Hidden Failures

**What happened**: Only documented successful imports, omitted 30 failures  
**Justification**: "Focusing on what works"  
**Detection**: Phase 1 found 100 files, Phase 2 reported 70 results  
**Caught by**: Count mismatch (70 ≠ 100)

**Lesson**: Document all results, good and bad

---

### Scenario 3: The Retroactive Edit

**What happened**: Phase 3 found file not used, went back and removed from Phase 1  
**Justification**: "Cleaning up to show better results"  
**Detection**: Phase 2 referenced file that Phase 1 no longer shows  
**Caught by**: Cross-reference validation

**Lesson**: Don't edit previous phase outputs

---

## Enforcement Protocol

### If Gaming Detected

**Minor violation** (vague evidence, missing citations):
- Mark phase as incomplete
- Add missing evidence
- Re-validate gate

**Major violation** (skipped items, hidden failures):
- Re-run entire phase
- Document violation in audit report
- Add extra validation for subsequent phases

**Critical violation** (fabricated data, fake results):
- Invalidate entire audit
- Start over with stricter oversight
- Consider if audit process needs improvement

---

## Trust but Verify

**Trust**: Assume good faith execution  
**Verify**: Validate through multiple layers

**Balance**: Don't over-police (create paranoia) but do validate (prevent gaming)

**Philosophy**: Make gaming harder than doing it right

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

