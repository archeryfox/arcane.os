# ADR 010: GitLab Repository — Create via glab CLI with SSH

## Status
Accepted (Session: 2026-09-12 04:30+)

## Context
User asked: "выложи на gitlab" (push to GitLab)

## Decision
**Use `glab` CLI to create repo and push via SSH:**

```bash
# Create repo
glab repo create arcana-os --private --description "ARCANA.OS Telegram bot"

# Configure SSH for gitlab.com
# ~/.ssh/config:
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_ed25519
    IdentitiesOnly yes

# Push
git remote set-url origin git@gitlab.com:archeryfox/arcana-os.git
git push -u origin main
```

## Alternatives Considered
- HTTPS with token (tried first, failed with credential helper issues)
- Manual web UI creation + git remote add (rejected — user has glab)

## Consequences

### Positive
- Automated repo creation
- SSH authentication (no token in URL)
- Private repo by default

### Negative
- Requires SSH key registered on GitLab
- glab auth needed
- SSH config needed for custom key path

## Issues Encountered & Resolved
1. **glab auth** → `glab auth login` (already done)
2. **Repo creation** → `glab repo create` worked
3. **HTTPS push** → Failed (credential helper confusion)
4. **SSH key** → Custom key `gitlab_ed25519` not in default location
5. **SSH config** → Added `~/.ssh/config` with `IdentityFile`
6. **Key not registered** → Added via `glab ssh-key add`
7. **Git user config** → Set `user.email` and `user.name` for commits

## Final Result
- Repo: https://gitlab.com/archeryfox/arcana-os
- SSH push working
- `.gitignore` excludes `.env`, `venv/`, `__pycache__/`

## Related Decisions
- ADR 011: GitLab CI/CD pipeline
- ADR 002: Deployment guides reference this repo