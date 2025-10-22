# How To Plan An Audit

**Version**: 1.0.0  
**Purpose**: Step-by-step guide to creating systematic audit plans  
**Estimated Time**: 30-60 minutes for a comprehensive audit plan

---

## Purpose

This guide teaches you how to CREATE an audit plan, not how to RUN one.

**Use this when**: Starting a new audit from scratch  
**Output**: A complete, systematic audit plan ready to execute

---

## The Planning Process

### Step 1: Define Scope (5 minutes)

**Questions to answer**:
- What are you auditing? (codebase, documentation, system, process)
- What's the boundary? (which directories, which time period, which features)
- What's OUT of scope? (what won't you audit)
- Why audit now? (what triggered this need)

**Output**: Scope statement

**Example**:
```markdown
## Audit Scope

**What**: Duck-e tech stack codebase
**Boundary**: 5 core directories (aether/akasha, 02-egg/*)
**Excluded**: External dependencies, virtual environments
**Trigger**: Documentation claims vs reality mismatch
**Goal**: Verify actual production state
```

---

### Step 2: Identify Audit Objectives (10 minutes)

**Questions to answer**:
- What questions will this audit answer?
- What decisions depend on audit results?
- What success looks like?
- What deliverables are needed?

**Output**: Objectives list + success criteria

**Example**:
```markdown
## Objectives

1. Determine which code actually imports successfully
2. Identify which files are used in production
3. Document gap between claims and reality
4. Produce 6 tech stack documents with verified statuses

## Success Criteria

- 100% of in-scope files analyzed
- Every feature has verified status (VERIFIED/BROKEN/PLANNED)
- All claims have evidence citations
- Documentation accurately reflects production state
```

---

### Step 3: Design Phase Structure (15 minutes)

**Questions to answer**:
- What phases are needed to gather evidence?
- What's the logical sequence? (each phase feeds next)
- What's the output of each phase?
- What gates validate each phase?

**Common Phase Types**:
- **Discovery**: What exists? (file scans, inventories)
- **Testing**: Does it work? (import tests, execution tests)
- **Tracing**: How is it connected? (dependency analysis, call graphs)
- **Documentation**: What's claimed? (extract from docs)
- **Cross-Reference**: Claims vs reality? (reconciliation, truth table)
- **Reporting**: Present findings (generate documents)

**Output**: Phase sequence with inputs/outputs

**Example**:
```markdown
## Phase Structure

Phase 0: Template Preparation
  Input: None
  Process: Create all templates and rules
  Output: 9 template files
  Gate: All templates complete, no ambiguity

Phase 1: Code Scan
  Input: Directory list
  Process: AST parsing, file inventory
  Output: phase1-code-scan.json
  Gate: All directories scanned, JSON valid

Phase 2: Import Verification
  Input: phase1-code-scan.json
  Process: Test each file import
  Output: phase2-imports.json
  Gate: All files tested, errors recorded

[... and so on]
```

---

### Step 4: Define Quality Gates (10 minutes)

**For each phase, specify**:
- What must be true to proceed?
- How to verify objectively?
- What metrics indicate success?
- What errors are blockers vs warnings?

**Gate Template**:
```markdown
## Phase X Gate

### Completion Criteria
- [ ] All X items processed
- [ ] Output file exists and is valid
- [ ] No skipped items

### Quality Criteria
- [ ] Evidence cited for all findings
- [ ] Errors recorded (not hidden)
- [ ] Metrics calculated correctly

### Validation
Run: [command to validate]
Expected: [what success looks like]

### Decision
Pass: Proceed to Phase X+1
Fail: Complete Phase X before proceeding
```

---

### Step 5: Design Output Formats (10 minutes)

**Questions to answer**:
- What format for intermediate outputs? (JSON, CSV, markdown)
- What structure for phase outputs?
- How will phases reference each other?
- What format for final deliverables?

**Best Practices**:
- JSON for machine-readable data (phases 1-6)
- Markdown for human-readable reports (phase 7)
- Consistent field names across phases
- Absolute paths for file references

**Output**: Template examples for each phase

---

### Step 6: Anti-Gaming Rules (10 minutes)

**Questions to answer**:
- What shortcuts might someone take?
- How to prevent gaming the process?
- What validation prevents faking results?
- What makes violations detectable?

**Common Gaming Attempts**:
- "Probably works" → Require actual test results
- "I checked some files" → Require count matching
- "Documentation says complete" → Require code verification
- "Skip complex files" → Require ALL files processed

**Output**: ANTI-GAMING-MEASURES.md with red flags

---

### Step 7: Create Plan Document (10 minutes)

**Use the audit-plan-template.md** (in templates/)

**Required sections**:
- Objective (what and why)
- Scope (boundaries)
- Phase structure (sequence)
- Each phase detailed (rule, process, output, gate)
- Success criteria
- Anti-gaming measures
- Timeline estimates

**Validation checklist**:
- [ ] Every phase has clear rule (CAN/CANNOT)
- [ ] Every phase has output format specified
- [ ] Every phase has gate criteria
- [ ] Dependencies between phases documented
- [ ] No ambiguous terms or instructions
- [ ] Timeline realistic
- [ ] Scope achievable

---

## Common Patterns

### Pattern 1: Code Quality Audit
```
Phase 0: Templates
Phase 1: File scan (what exists)
Phase 2: Import test (does it load)
Phase 3: Server trace (is it used)
Phase 4: Test execution (does it work)
Phase 5: Cross-reference
Phase 6: Report generation
```

### Pattern 2: Documentation Audit
```
Phase 0: Templates
Phase 1: Doc scan (what's documented)
Phase 2: Claim extraction (what's claimed)
Phase 3: Code verification (is it true)
Phase 4: Gap analysis
Phase 5: Report generation
```

### Pattern 3: Feature Audit
```
Phase 0: Templates
Phase 1: Feature inventory (what's planned)
Phase 2: Code search (is it built)
Phase 3: Integration test (does it work)
Phase 4: User verification (is it accessible)
Phase 5: Truth table
Phase 6: Report generation
```

---

## Anti-Patterns to Avoid

### Bad Plan 1: Too Many Phases
12+ phases with tiny deliverables → unnecessary overhead

**Better**: 5-7 meaningful phases with substantive outputs

### Bad Plan 2: Vague Gates
"Phase complete when done" → no objective criteria

**Better**: "Phase complete when all N files tested AND JSON valid AND no skipped items"

### Bad Plan 3: No Cross-Reference
Each phase independent → contradictions undetected

**Better**: Later phases validate earlier phases (evidence chain)

### Bad Plan 4: Subjective Statuses
"Looks good" → not reproducible

**Better**: "Imports successfully (Phase 2) + Used in server (Phase 3) = VERIFIED"

---

## Validation Checklist

Before executing your audit plan:

- [ ] Scope clearly defined
- [ ] Objectives specific and measurable
- [ ] 5-8 phases with logical sequence
- [ ] Each phase has rule, process, output, gate
- [ ] Output formats specified (with examples)
- [ ] Anti-gaming measures defined
- [ ] Success criteria clear
- [ ] Timeline reasonable
- [ ] All templates referenced exist
- [ ] No ambiguous instructions

**If all checked**: Plan ready to execute  
**If any unchecked**: Refine before starting

---

## Evolution

After completing audits using this guide:
- Extract patterns (what worked well)
- Identify anti-patterns (what didn't work)
- Update HOW-TO-RUN-AN-AUDIT.md (guidelines evolve)
- Rarely update this constitution (principles stable)

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

