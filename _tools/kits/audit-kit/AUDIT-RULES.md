# Audit Rules

**Version**: 1.0.0  
**Purpose**: Clear CAN/CANNOT rules for each audit phase type  
**Status**: Enforcement document (violations = failed audit)

---

## Universal Rules (All Phases)

### CAN

- Document what you observe
- Record errors exactly as encountered
- Mark items as UNCLEAR if uncertain
- Request clarification before proceeding
- Take breaks (use handoff-kit)

### CANNOT

- Assume anything works without evidence
- Hide errors or failures
- Skip items to save time
- Modify code during audit
- Proceed without gate validation

---

## Phase Type: Discovery (Scanning)

**Purpose**: Identify what exists

### CAN

- Scan directories recursively
- List files, count lines, extract metadata
- Use automated tools (AST parsers, file scanners)
- Record structural information (classes, functions)
- Note files that can't be parsed

### CANNOT

- Skip files based on "importance"
- Filter results based on what "should" exist
- Modify files during scan
- Interpret code behavior (just structure)
- Assign status (working/broken)

**Example Phase**: Code scan, file inventory

---

## Phase Type: Testing (Verification)

**Purpose**: Determine if things work

### CAN

- Execute import tests
- Run automated tests
- Measure execution time
- Record success/failure objectively
- Save exact error messages

### CANNOT

- Mark as "probably works" without test
- Skip tests for "simple" files
- Hide test failures
- Fix issues during testing
- Assume "if one works, others do too"

**Example Phase**: Import verification, test execution

---

## Phase Type: Tracing (Integration)

**Purpose**: Understand connections and usage

### CAN

- Follow import chains recursively
- Build dependency graphs
- Identify what's used vs orphaned
- Categorize based on actual usage
- Document integration paths

### CANNOT

- Assume usage based on "looks important"
- Mark as used without import proof
- Skip complex dependency chains
- Guess at indirect usage

**Example Phase**: Server integration, dependency tracing

---

## Phase Type: Documentation (Claims)

**Purpose**: Extract what's documented/claimed

### CAN

- Read all documentation in scope
- Extract feature claims
- Record claims without verifying (yet)
- Cite specific sources (file:line)
- Track evolution across document versions

### CANNOT

- Verify claims during extraction (that's cross-reference phase)
- Skip documents that seem "less important"
- Paraphrase claims (quote or summarize accurately)
- Add claims not in documentation

**Example Phase**: Documentation parse, claim extraction

---

## Phase Type: Cross-Reference (Reconciliation)

**Purpose**: Compare different sources of truth

### CAN

- Compare claims vs code reality
- Assign status based on evidence from multiple phases
- Flag contradictions for investigation
- Calculate gap metrics
- Categorize findings objectively

### CANNOT

- Give "benefit of doubt" to questionable items
- Mark as verified without multi-phase evidence
- Hide contradictions
- Bias toward positive findings

**Example Phase**: Truth table, gap analysis

---

## Phase Type: Reporting (Communication)

**Purpose**: Present findings clearly

### CAN

- Format results for different audiences
- Create visualizations from data
- Organize by category/priority
- Include evidence citations
- Make recommendations based on findings

### CANNOT

- Add findings not in audit outputs
- Change statuses from truth table
- Hide negative findings
- Editorialize without evidence

**Example Phase**: Document generation, final report

---

## Gate Validation Rules

### Before Proceeding to Next Phase

**MUST verify**:
- All items in current phase processed
- Output file exists and is valid
- Gate criteria all met
- No unresolved blockers
- Evidence properly cited

**MUST NOT**:
- Skip gate validation
- Proceed with partial phase completion
- Override gate failure without fixing
- Hide gate failures

---

## Evidence Rules

### Valid Evidence Types

- Scan outputs (JSON, logs)
- Test results (pass/fail, error messages)
- File references (path:line)
- Metrics (counts, percentages, timings)
- Screenshots (if applicable)

### Invalid Evidence Types

- Opinions ("I think")
- Assumptions ("Should be")
- Generalizations ("Everything seems")
- Second-hand ("Documentation says", without verification)

---

## Common Violations & Penalties

| Violation | Severity | Action |
|-----------|----------|--------|
| Skipped files/items | Critical | Re-run phase completely |
| Hidden errors | Critical | Re-run phase, document all errors |
| Assumed without testing | High | Test the items, update results |
| Proceeded with failed gate | High | Go back, pass gate properly |
| No evidence citations | Medium | Add citations, re-validate |
| Vague findings | Medium | Specify findings, add details |

---

## Self-Audit Questions

**During execution, ask yourself**:

- Am I following the phase rule?
- Am I documenting evidence?
- Am I making assumptions?
- Would someone else get same results?
- Can I cite evidence for this finding?

**If answer is "no" to any**: Stop, correct, then continue

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

