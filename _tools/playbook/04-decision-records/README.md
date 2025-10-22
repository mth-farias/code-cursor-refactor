# Architectural Decision Records (ADRs)

**Purpose**: Document major architectural decisions made during Config refactoring

**Format**: ADR-XXX-title.md

---

## Active ADRs

### ADR-001: Controller + Subpackage Pattern
**Status**: Accepted  
**Date**: 2025-10-22  
**Context**: How to structure large Config modules (> 400 lines)?  
**Decision**: Use Controller + Subpackage architecture with configure() delegation  
**Impact**: All large Config modules follow this pattern

---

## ADR Lifecycle

**Proposed** → **Accepted** → **Deprecated** → **Superseded**

---

## ADR Template

```markdown
# ADR-XXX: Title

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded
**Deciders**: Names

## Context
What problem are we solving?

## Decision
What did we decide?

## Alternatives Considered
What else did we consider? Why rejected?

## Rationale
Why is this the best choice?

## Consequences
Positive and negative outcomes

## Review Schedule
When should we revisit this?
```

---

**Last Updated**: 2025-10-22

