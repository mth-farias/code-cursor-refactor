# Project Tools & Methodology

**Purpose**: All "how we work" documentation and workflow tools  
**Status**: Active  
**Last Updated**: 2025-10-22

---

## Structure

```
_tools/
├── kits/           # Universal workflow kits (reusable across projects)
│   ├── audit-kit/      → Discover truth through evidence-based audits
│   ├── repair-kit/     → Fix issues systematically with safety
│   └── handoff-kit/    → Preserve context across breaks
└── playbook/       # Project-specific patterns & guidelines
    ├── 01-architecture-patterns.md
    ├── 02-refactoring-workflow.md
    ├── 03-quality-gates.md
    └── 04-decision-records/
```

---

## What's What

### kits/ - Universal Workflows

**Source**: Proven patterns from multiple projects  
**Reusability**: Copy to any project, adapt as needed  
**Stability**: Constitutions stable, guidelines evolve

- **audit-kit**: When you need to verify what's actually true
- **repair-kit**: When you need to fix something safely
- **handoff-kit**: When you need to preserve context across breaks

See: `kits/README.md` for full overview

---

### playbook/ - Project-Specific Patterns

**Source**: Patterns established during Config refactoring  
**Scope**: Specific to this codebase (Config + BehaviorClassifier)  
**Purpose**: Extend REFACTOR_GUIDE.md with concrete implementations

- Architecture patterns (controller+subpackage, configure() delegation)
- Refactoring workflow (quality gates, testing, commits)
- Decision records (ADRs documenting key choices)

See: `playbook/README.md` for full overview

---

## How They Work Together

**kits/** = Process frameworks (audit, repair, handoff)  
**playbook/** = Implementation guidelines (how we code here)

**Example**:
- Use **audit-kit** to verify current state
- Use **playbook** to understand coding patterns
- Use **repair-kit** to execute refactoring safely
- Use **handoff-kit** to preserve context between sessions

---

## Integration with Project

These tools support the main project structure:

```
Project Root/
├── _tools/         ← How we work (methodology)
├── codes/          → What we build (source code)
├── data/           → What we use (test data)
├── plans/          → What we're doing (project plans)
├── references/     → What we learned from (original code)
└── tools/          → What we execute (scripts, utilities)
```

---

**Status**: Production-ready  
**Next**: Use handoff-kit to create session handoffs

