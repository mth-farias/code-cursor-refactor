# Repair Kit

**Version**: 1.0.0  
**Purpose**: Systematic, safe fixes with validation and rollback  
**Status**: Production-ready

---

## What Is This?

A complete toolkit for fixing issues discovered in audits (or elsewhere) with built-in safety and validation.

**Philosophy**: Plan-first, one issue at a time, validate everything, rollback on failure.

---

## When To Use

Use repair-kit when:
- Audit identified specific issues
- Need to fix systematically (not ad-hoc)
- Safety critical (rollback needed)
- Want to validate fix worked

**Don't use** for:
- Exploratory changes
- Quick experiments
- Trivial one-line fixes

---

## Quick Start

1. **Plan**: Read `HOW-TO-PLAN-A-FIX.md`, create plan using template
2. **Execute**: Read `HOW-TO-RUN-A-FIX.md`, follow plan
3. **Validate**: Use `progress/validation-checklist.md`
4. **Decide**: Merge or rollback

---

## Core Principles (From Constitution)

1. **Plan-First**: Never improvise on critical systems
2. **One Issue**: Fix ONE thing at a time
3. **Backup**: Always preserve rollback ability
4. **Validate**: Prove fix worked
5. **Rollback**: If validation fails, revert immediately

---

## Integration

**After audit-kit**: Use audit findings to prioritize fixes  
**With handoff-kit**: Use if pausing mid-fix  
**Back to audit-kit**: Re-audit after fix to verify improvement

---

**Version**: 1.0.0 | **Last Updated**: 2025-10-21

