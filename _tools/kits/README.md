# Universal Kits System

**Version**: 1.0.0  
**Created**: 2025-10-21  
**Purpose**: Reusable toolkits for systematic work  
**Status**: Production-ready

---

## What Is This?

Three self-contained kits for systematic, high-quality work:

1. **audit-kit**: Discover truth through evidence-based audits
2. **repair-kit**: Fix issues systematically with safety and validation
3. **handoff-kit**: Preserve context across breaks and transitions

**Philosophy**: Built on 5 core principles from duck-e-academy/00-know-how:
- Systematic over ad-hoc
- Reflective over reactive
- Evolvable over static
- Quality over speed
- Continuity over isolation

---

## The Three Kits

### Audit Kit - Discovery & Truth

**Purpose**: Find out what's actually true (vs what's claimed or assumed)

**Use When**:
- Need to verify documentation claims
- Assess actual codebase state
- Identify gaps between plan and reality
- Determine production status

**Key Features**:
- Evidence-based (not assumption-based)
- Systematic coverage (not selective)
- Progressive validation (each phase validates previous)
- Anti-gaming measures (hard to fake results)

**Output**: Truth table showing reality vs claims

**Learn More**: [audit-kit/README.md](audit-kit/README.md)

---

### Repair Kit - Systematic Fixes

**Purpose**: Fix issues safely with validation and rollback

**Use When**:
- Audit identified specific issues
- Need to fix without breaking what works
- Want to validate fix actually worked
- Safety critical (need rollback capability)

**Key Features**:
- Plan-first (no improvisation)
- One issue at a time (focused fixes)
- Backup before modify (always reversible)
- Validate after fix (prove it worked)
- Rollback on failure (safety net)

**Output**: Validated fix with before/after proof

**Learn More**: [repair-kit/README.md](repair-kit/README.md)

---

### Handoff Kit - Continuity

**Purpose**: Preserve context across breaks and switches

**Use When**:
- Ending work session (>1 day break)
- Switching agents or people
- Phase/stage boundaries
- Before risky operations

**Key Features**:
- 4-component handoff (state + trajectory + guidance + artifacts)
- Hierarchical detail (L1 summary → L4 complete)
- Naive agent capable (no "you had to be there")
- Quality levels (minimal → comprehensive)

**Output**: Complete handoff enabling seamless continuation

**Learn More**: [handoff-kit/README.md](handoff-kit/README.md)

---

## Integrated Workflows

### Workflow 1: Discovery

```
Problem: "Is our tech stack documentation accurate?"
    ↓
Use: audit-kit
    ↓
Process: Run systematic audit (Phases 0-6)
    ↓
Output: Truth table (claims vs reality)
    ↓
Result: Know exactly what's true
```

**Time**: 2-4 hours  
**Kits Used**: audit-kit only

---

### Workflow 2: Discovery → Improvement

```
Problem: "Documentation is wrong, let's fix it"
    ↓
Step 1: audit-kit
    ↓
    Audit reveals: 269 files have BOM encoding (blocking imports)
    ↓
Step 2: repair-kit
    ↓
    Create fix plan → Execute → Validate → Merge
    ↓
Step 3: audit-kit (partial re-audit)
    ↓
    Verify: Import rate 13% → 98% ✅
    ↓
Result: Problem identified AND fixed AND verified
```

**Time**: 3-5 hours total  
**Kits Used**: audit-kit → repair-kit → audit-kit

---

### Workflow 3: Long-Running with Breaks

```
Day 1: Start audit (Phases 0-2 complete)
    ↓
    Use: handoff-kit
    Create: session-end.md (State + next steps)
    ↓
Day 2: Resume audit
    ↓
    Use: handoff-kit
    Read: 00-START-HERE.md → session-end.md
    Continue: Phases 3-4
    ↓
    Use: handoff-kit again
    Create: Updated session-end.md
    ↓
Day 3: Resume and complete
    ↓
    Use: handoff-kit
    Read: session-end.md
    Complete: Phases 5-6
```

**Time**: Multi-day work  
**Kits Used**: audit-kit + handoff-kit

---

### Workflow 4: Full Cycle (Audit → Fix → Validate)

```
1. DISCOVER (audit-kit)
   Run full audit → Identify issues → Prioritize
   ↓
2. PAUSE (handoff-kit)
   Create comprehensive handoff
   ↓
3. RESUME (handoff-kit)
   Read handoff → Orient → Continue
   ↓
4. FIX (repair-kit)
   For each issue:
     - Plan fix
     - Execute
     - Validate
     - Merge or rollback
   ↓
5. PAUSE (handoff-kit if needed)
   ↓
6. VERIFY (audit-kit partial re-audit)
   Re-run relevant phases → Confirm improvement
   ↓
7. DOCUMENT (audit-kit Phase 7)
   Generate final documentation showing improved state
```

**Time**: Multi-session work  
**Kits Used**: All three

---

## When To Use Which Kit

| Situation | Kit | Why |
|-----------|-----|-----|
| "Is this actually true?" | audit-kit | Verify claims |
| "This is broken, fix it" | repair-kit | Systematic fix |
| "Pausing for >1 day" | handoff-kit | Preserve context |
| "What's in production?" | audit-kit | Discover reality |
| "Fix made things worse" | repair-kit | Rollback capability |
| "Switching agents" | handoff-kit | Transfer context |
| "Document current state" | audit-kit Phase 7 | Generate docs |

---

## Kit Independence

Each kit is **self-contained**:
- Can be used alone
- Has own constitution (stable principles)
- Has own templates and guides
- Doesn't require other kits

But they **integrate well**:
- Audit finds issues → Repair fixes issues
- Any kit + Handoff = continuity across breaks
- Repair → Partial audit = validation

---

## Quality Standards

All kits follow:
- **4-layer enforcement**: Declarative + Structural + Procedural + Meta
- **Plan-first**: Create plan before execution
- **Evidence-based**: Verify, don't assume
- **Gate validation**: Can't proceed without passing gates
- **Evolution tracking**: VERSION + CHANGELOG

---

## Getting Started

### For Auditing

1. Read [audit-kit/README.md](audit-kit/README.md)
2. Read [audit-kit/HOW-TO-PLAN-AN-AUDIT.md](audit-kit/HOW-TO-PLAN-AN-AUDIT.md)
3. Create your audit plan
4. Follow [audit-kit/HOW-TO-RUN-AN-AUDIT.md](audit-kit/HOW-TO-RUN-AN-AUDIT.md)

### For Fixing

1. Read [repair-kit/README.md](repair-kit/README.md)
2. Read [repair-kit/HOW-TO-PLAN-A-FIX.md](repair-kit/HOW-TO-PLAN-A-FIX.md)
3. Create your fix plan
4. Follow [repair-kit/HOW-TO-RUN-A-FIX.md](repair-kit/HOW-TO-RUN-A-FIX.md)

### For Handoffs

1. Read [handoff-kit/README.md](handoff-kit/README.md)
2. Determine handoff type and detail level
3. Use appropriate templates
4. Validate handoff completeness

---

## Evolution

**Version 1.0.0**: Initial release based on:
- duck-e-academy/00-know-how principles
- Tech stack audit execution experience
- Proven patterns from successful projects

**Future versions**: Will evolve based on usage across multiple projects

See [CHANGELOG.md](CHANGELOG.md) for evolution history.

---

## Reusability

**These kits are UNIVERSAL**:
- Copy to any project
- Adapt templates to specific needs
- Keep constitutions stable
- Evolve guidelines based on experience

**Example**: Copy to `project-name/_utils/` and adapt for that project's specifics

---

## Contributing

Used these kits? Found improvements?

1. Document what worked/didn't
2. Extract patterns
3. Propose updates (with rationale)
4. Test in one kit first
5. Roll out to others if successful
6. Update VERSION and CHANGELOG

---

**Version**: 1.0.0 | **Created**: 2025-10-21 | **Status**: Production-Ready

