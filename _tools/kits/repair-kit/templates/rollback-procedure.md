# Rollback Procedure: [Fix Name]

**Fix Branch**: `fix/[issue-name]`  
**Affected Files**: [N] files  
**Backup Location**: `.fix-backups/[timestamp]/`

---

## When To Rollback

Rollback immediately if:
- Validation fails
- New errors introduced
- Metrics degrade
- Unintended side effects
- User rejects fix

---

## Rollback Steps

### Step 1: Verify Current Branch

```bash
git branch  # Confirm on fix/[issue-name]
```

### Step 2: Restore Files

```bash
# Restore all affected files from main
git checkout main -- [file1] [file2] ...

# OR restore all changed files
git checkout main -- .
```

### Step 3: Verify Restoration

```bash
# Check diff (should show no changes from main)
git diff main

# Verify import status unchanged
python -c "import [affected_module]"
```

### Step 4: Delete Fix Branch

```bash
# Switch back to main
git checkout main

# Delete fix branch
git branch -D fix/[issue-name]
```

### Step 5: Confirm Rollback Complete

- [ ] On main branch
- [ ] No uncommitted changes
- [ ] Fix branch deleted
- [ ] Files restored to pre-fix state
- [ ] Metrics match pre-fix baseline

---

## Verification Commands

```bash
# Current branch
git branch --show-current

# Changes from main
git diff main --stat

# Recent commits
git log --oneline -5
```

---

## Alternative: Restore from Backup

If git rollback fails:

```bash
# Copy from backup
cp .fix-backups/[timestamp]/* [destination]

# Verify files restored
diff .fix-backups/[timestamp]/file.py original/file.py
```

---

## Post-Rollback

After rollback:
1. Document why rollback was needed
2. Analyze what went wrong
3. Update fix plan if attempting again
4. Don't attempt same fix without plan changes

---

**Rollback Time**: [Estimated X minutes]  
**Risk Level**: None (safe operation)

---

**Created**: YYYY-MM-DD

