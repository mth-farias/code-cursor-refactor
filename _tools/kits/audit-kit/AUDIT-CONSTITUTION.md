# Audit Kit Constitution

**Version**: 1.0.0  
**Status**: Stable  
**Last Updated**: 2025-10-21

---

## Purpose

This constitution defines the immutable principles that govern all audits conducted with this kit.

**Constitutions are STABLE** - they change rarely and only with strong justification.  
**Guidelines evolve** - they adapt based on experience (see HOW-TO-RUN-AN-AUDIT.md).

---

## Core Principles

### 1. Evidence-Based Discovery

**Principle**: Truth emerges from verifiable evidence, not assumptions or claims.

**This Means**:
- Every finding must cite specific evidence (file:line, test result, scan output)
- Documentation claims are extracted but not trusted until verified
- "Probably works" is not a valid status
- Absence of evidence is documented, not hidden

**Rationale**: Audits reveal reality. Reality is objective. Assumptions introduce bias.

---

### 2. Systematic Over Selective

**Principle**: Completeness requires systematic coverage, not cherry-picking.

**This Means**:
- All files in scope must be scanned (no skipping "unimportant" files)
- All phases must complete before proceeding (no jumping ahead)
- Gates must pass before advancing (no shortcuts)
- Partial work is clearly marked as partial

**Rationale**: Selective audits hide problems. Systematic audits find them.

---

### 3. Non-Destructive Observation

**Principle**: Audits observe and document; they do not modify.

**This Means**:
- Read-only operations during audit phases
- Issues are recorded, not fixed
- Broken code is documented as broken
- Fixes happen in separate repair phase (not audit phase)

**Rationale**: Mixing audit and repair contaminates results. Separate concerns.

---

### 4. Reproducible Process

**Principle**: Audits must be repeatable with consistent results.

**This Means**:
- Use automated scanning where possible (eliminates human variance)
- Document methodology clearly (others can reproduce)
- Output formats are standardized (consistent structure)
- Process is version-controlled (track improvements)

**Rationale**: Reproducibility enables validation. One-off processes can't be trusted.

---

### 5. Progressive Validation

**Principle**: Each phase builds on and validates previous phase outputs.

**This Means**:
- Phase N requires Phase N-1 outputs (no skipping)
- Later phases cross-reference earlier phases
- Contradictions are investigated and resolved
- Final truth table reconciles all phases

**Rationale**: Sequential validation catches errors through multiple perspectives.

---

## Quality Enforcement

Based on 4-layer enforcement from 00-know-how/planning/04-quality-enforcement.md:

### Layer 1: Declarative (AUDIT-RULES.md)
Rules explicitly state what CAN and CANNOT be done in each phase.

### Layer 2: Structural (Templates)
Templates force required fields - can't skip evidence citations or status assignments.

### Layer 3: Procedural (Gates)
Quality gates at each phase boundary - must pass to proceed.

### Layer 4: Meta (Cross-Reference)
Phase 6 validates all previous phases - can't fake without faking everything.

---

## Forbidden Practices

These practices violate the constitution and must never occur:

1. **Assuming code works without testing**
2. **Trusting documentation without code verification**
3. **Cherry-picking files/features to audit**
4. **Skipping phases or gates**
5. **Hiding errors or failures**
6. **Modifying code during audit**
7. **Guessing when evidence is unclear**
8. **Proceeding with incomplete phase outputs**

---

## Success Criteria

An audit is successful when:

1. All phases completed sequentially
2. All gates passed with evidence
3. Truth table reconciles claims vs reality
4. Results are reproducible
5. No gaming or shortcuts detected
6. Output documents provide clear, actionable insights

---

## Evolution

This constitution may evolve when:
- Fundamental flaw in principles discovered
- Major new audit methodology emerges
- Principles proven ineffective through multiple audits

**Process**: Propose change → Validate through pilot → Update constitution → Version bump

**Frequency**: Rare (constitution should be stable foundation)

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

