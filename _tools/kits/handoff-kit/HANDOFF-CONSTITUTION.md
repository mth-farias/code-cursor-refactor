# Handoff Kit Constitution

**Version**: 1.0.0  
**Status**: Stable  
**Last Updated**: 2025-10-21

---

## Purpose

This constitution defines the immutable principles that govern all handoffs.

**Based on**: 00-know-how/patterns/04-handoff-mechanisms.md (4-component pattern)

---

## Core Principles

### 1. Complete Context Over Assumptions

**Principle**: Handoffs must contain complete context, never assume "you had to be there" knowledge.

**This Means**:
- State snapshot (where we are)
- Trajectory history (how we got here)
- Forward guidance (what's next)
- Knowledge artifacts (what we produced)

**Rationale**: Naive agent must be able to continue. Incomplete context = failed handoff.

---

### 2. Explicit State Over Implicit

**Principle**: Current state must be explicitly documented, not inferred.

**This Means**:
- Progress percentage (not "mostly done")
- Specific phase/step (not "somewhere in middle")
- Active blockers listed (not discovered later)
- Decisions documented with rationale

**Rationale**: Implicit state is lost. Explicit state is preserved.

---

### 3. Decision Trail Over Amnesia

**Principle**: Why decisions were made must be captured, not just what was decided.

**This Means**:
- Document decision rationale
- Note alternatives considered
- Explain trade-offs
- Record outcomes of decisions

**Rationale**: Future agents need to understand why, to make consistent decisions.

---

### 4. Artifact References Over Rediscovery

**Principle**: Point to what exists, don't make next agent search.

**This Means**:
- List all deliverables with paths
- Reference intermediate outputs
- Link to key documents
- Provide file locations

**Rationale**: Rediscovering artifacts wastes time. Direct references save effort.

---

### 5. Actionable Next Steps Over Vagueness

**Principle**: Next steps must be specific and executable, not conceptual.

**This Means**:
- "Read file.md lines 50-100" not "review documentation"
- "Run command X in directory Y" not "do some testing"
- "Create file.md with sections A,B,C" not "document findings"

**Rationale**: Vague instructions require context. Specific instructions are executable.

---

## Handoff Quality Criteria

A handoff is complete when:

1. **State** is explicit and current
2. **Trajectory** explains how we got here
3. **Guidance** provides clear next steps
4. **Artifacts** are all referenced
5. **Naive agent** could continue without asking questions

---

## Forbidden Practices

1. **Assuming context** ("they'll figure it out")
2. **Vague next steps** ("finish the work")
3. **Missing decisions** (why things are this way)
4. **Broken references** (links to files that moved)
5. **Stale state** (handoff out of date)

---

## Evolution

Update when:
- Better handoff patterns discovered
- Context loss still occurring despite handoffs
- New handoff types needed (e.g., emergency handoff)

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

