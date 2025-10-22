# Feature Status Template

Use this format to document individual feature audit results.

---

## [Feature Name]

**Status**: VERIFIED | BUILT_NOT_USED | BROKEN | PLANNED | MISSING  
**Category**: [memory/agents/tools/security/etc.]  
**Priority**: P0 | P1 | P2

---

### Description

[What this feature does in 2-3 sentences]

---

### Implementation

**Location**: `path/to/implementation.py`  
**Class/Function**: `ClassName` or `function_name()`  
**Lines**: [start-end]

---

### Evidence

**Phase 1 (Exists)**: [Evidence citation]  
**Phase 2 (Imports)**: [Evidence citation]  
**Phase 3 (Used)**: [Evidence citation]  
**Phase 4 (Claimed)**: [Evidence citation]

---

### Status Determination

```
IF exists=YES AND imports=YES AND used=YES AND claimed=YES
  → STATUS: VERIFIED ✅
  
IF exists=YES AND imports=YES AND used=NO
  → STATUS: BUILT_NOT_USED 🏗️
  
IF exists=YES AND imports=NO
  → STATUS: BROKEN 🔴
  
IF exists=NO AND claimed=YES
  → STATUS: PLANNED 📋
  
IF exists=NO AND should_exist=YES
  → STATUS: MISSING ❓
```

**Assigned Status**: [STATUS] [SYMBOL]

**Rationale**: [Why this status based on evidence]

---

### Dependencies

**Requires**:
- [Dependency 1]
- [Dependency 2]

**Required By**:
- [Feature that depends on this]

---

### Notes

[Any additional observations, concerns, or recommendations]

---

**Last Updated**: YYYY-MM-DD  
**Verified By**: [Phase numbers]

