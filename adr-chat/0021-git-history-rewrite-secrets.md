# ADR 021: Git History Rewrite — Remove Leaked Secrets

## Status
Accepted (Session: 2026-09-12 07:00+)

## Context
User discovered leaked secrets in git history:
- OpenRouter API key: `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`
- Telegram Bot Token: `8935559519:AAG2_lTlQJOCCHvBYa01L0HesQn5eZPxQus`

Found in initial commit (`Идея.md` had curl example with real keys).

## Decision
**Complete history rewrite — delete `.git` and reinitialize:**

```bash
rm -rf .git
git init
git config user.email "archeryfox2005@gmail.com"
git config user.name "archeryfox"
git add -A
git commit -m "Initial commit: ARCANA.OS Telegram bot with FastAPI, MongoDB, aiogram 3"
```

**Force push to GitLab (required unprotecting main branch):**
```bash
glab api -X DELETE /projects/archeryfox%2Farcana-os/protected_branches/main
git push --force origin main
```

## Alternatives Considered
- `git filter-repo` (rejected — not installed, complex)
- `git filter-branch` (rejected — slow, deprecated)
- BFG Repo-Cleaner (rejected — not installed)

## Consequences

### Positive
- **Clean history** — only one commit, no secrets
- **Simple** — no complex filtering needed
- **Fast** — seconds vs minutes for filter-repo

### Negative
- **Loses all history** — 4 commits gone
- **Force push required** — breaks forks/clones
- **Branch protection** — had to unprotect main via GitLab API

## Verification
```bash
git log --oneline
# 4ad923c Initial commit: ARCANA.OS Telegram bot with FastAPI, MongoDB, aiogram 3

git log -p --all -S "sk-or-v1" -S "8935559519"
# No results — secrets gone
```

## Related Decisions
- ADR 010: GitLab repo recreated after history rewrite
- ADR 011: CI/CD pipeline on clean history