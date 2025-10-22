# Handoff Protocols

**Version**: 1.0.0  
**Purpose**: When and how to create handoffs  
**Based on**: 00-know-how/patterns/04-handoff-mechanisms.md

---

## When To Handoff

### Critical Handoff Points

✅ **Always handoff at**:
- Phase/stage boundaries
- Before breaks >24 hours
- Agent switches
- Before major decisions

⚠️ **Consider handoff at**:
- Complex task completion
- Before risky operations
- When context feels heavy

❌ **Don't handoff**:
- Every small action
- Mid-task (finish atomic unit first)
- When continuing immediately

---

## How To Handoff

### 1. Choose Template

**Based on handoff type**:
- Phase boundary: `session-end.md`
- Resuming: `session-start.md` (read this)
- First time: `00-START-HERE.md`
- Status only: `status-snapshot.md`
- Decisions: `decision-log.md`

### 2. Fill Required Sections

**All handoffs need**:
- State (where we are)
- Next steps (what to do)
- Artifacts (where things are)

**Comprehensive handoffs add**:
- Trajectory (how we got here)
- Decisions (why things are this way)
- Lessons (what we learned)

### 3. Validate Completeness

**Test**: Would naive agent know what to do?

**Check**:
- [ ] All questions answerable from handoff
- [ ] Next steps are specific
- [ ] Artifacts are findable
- [ ] No broken references

---

## Handoff Quality Levels

### Level 1: Minimal (5 min)
- Current status
- Next immediate step
- Key file locations

**Use for**: Same agent, short breaks

### Level 2: Standard (15 min)
- Complete state snapshot
- Next 3-5 steps
- All artifact references
- Recent decisions

**Use for**: Phase boundaries, agent switches

### Level 3: Comprehensive (30 min)
- Everything in Level 2 PLUS
- Full trajectory
- All decisions with rationale
- Lessons learned
- Recommendations

**Use for**: Project pauses, complex transitions

### Level 4: letter-4-future (60 min)
- Everything in Level 3 PLUS
- Meta-reflection
- Transferable patterns
- Complete resurrection capability

**Use for**: Project completion, long-term archival

---

## Integration

**With audit-kit**: Handoff between audit phases  
**With repair-kit**: Handoff between fix attempts  
**Standalone**: Any work requiring continuity

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

