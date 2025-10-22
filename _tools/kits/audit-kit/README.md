# Audit Kit

**Version**: 1.0.0  
**Purpose**: Systematic discovery and validation of truth through evidence-based audits  
**Status**: Production-ready

---

## What Is This?

A complete toolkit for conducting rigorous, reproducible audits of code, documentation, systems, or processes.

**Philosophy**: Evidence over assumptions, systematic over selective, validation over trust.

---

## When To Use

Use audit-kit when you need to:
- Verify documentation claims against reality
- Assess actual state of a codebase
- Identify gaps between planned and built
- Determine what's actually in production
- Create evidence-based status reports

**Don't use** for:
- Simple file searches (use grep)
- One-off checks (too much overhead)
- Fixing issues (use repair-kit)

---

## Quick Start (5 minutes)

### 1. Plan Your Audit

Read: `HOW-TO-PLAN-AN-AUDIT.md`

Create: Your audit plan using `templates/audit-plan-template.md`

Time: 30-60 minutes

### 2. Run Your Audit

Read: `HOW-TO-RUN-AN-AUDIT.md`

Execute: Follow your plan phase by phase

Track: Use `progress/phase-tracker.md`

Time: Varies (typically 2-4 hours)

### 3. Validate Results

Check: `progress/gate-checklist.md` for each phase

Verify: All gates passed, all outputs generated

---

## What's Inside

### Core Documents

| File | Purpose | When To Read |
|------|---------|--------------|
| `AUDIT-CONSTITUTION.md` | Immutable principles | Before planning (understand philosophy) |
| `HOW-TO-PLAN-AN-AUDIT.md` | Create audit plans | Starting new audit |
| `HOW-TO-RUN-AN-AUDIT.md` | Execute audits | During execution |
| `AUDIT-RULES.md` | CAN/CANNOT rules | During execution (per phase) |
| `ANTI-GAMING-MEASURES.md` | Quality enforcement | When validating |

### Templates

| Template | Purpose |
|----------|---------|
| `audit-plan-template.md` | Structure for new audit plans |
| `phase-output.json` | Format for phase results |
| `feature-status.md` | How to document feature states |
| `section.md` | Section documentation format |

### Progress Tracking

| File | Purpose |
|------|---------|
| `phase-tracker.md` | Simple phase checklist |
| `gate-checklist.md` | Validation criteria |

---

## Core Principles (From Constitution)

1. **Evidence-Based**: Truth from verifiable evidence, not assumptions
2. **Systematic**: Complete coverage, not selective
3. **Non-Destructive**: Observe and document, don't modify
4. **Reproducible**: Same process = same results
5. **Progressive**: Each phase validates previous phases

---

## Typical Audit Flow

```
1. Define Scope
   ↓
2. Create Plan (HOW-TO-PLAN)
   ↓
3. User Reviews Plan
   ↓
4. Phase 0: Prepare Templates
   ↓
5. Phases 1-N: Execute & Validate
   ↓
6. Cross-Reference Phase
   ↓
7. Final Report
   ↓
8. User Reviews Results
   ↓
9. Decision: Document As-Is OR Enter Repair Mode
```

---

## Integration with Other Kits

**With repair-kit**: Audit identifies issues → Repair-kit fixes them → Re-audit validates  
**With handoff-kit**: Use handoff-kit if pausing audit mid-execution

---

## Success Criteria

An audit using this kit is successful when:
- All phases completed systematically
- All gates passed with evidence
- Results are reproducible
- No gaming detected
- Clear, actionable findings
- Truth validated through cross-reference

---

## Evolution

**This kit evolves** based on real audit executions:
- Update HOW-TO-RUN with learnings
- Add templates as patterns emerge
- Refine rules based on edge cases
- Update anti-gaming measures with new red flags

**Track changes** in parent CHANGELOG.md

---

## Examples

**Example 1**: Tech stack audit (code + docs + integration)  
**Example 2**: Documentation audit (claims vs reality)  
**Example 3**: Feature audit (planned vs built vs deployed)

See specific project implementations for detailed examples.

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

