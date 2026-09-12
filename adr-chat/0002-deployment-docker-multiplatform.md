# ADR 002: Deployment Strategy — Docker + Multi-Platform Guides

## Status
Accepted (Session: 2026-09-12 01:00+)

## Context
User asked: "размести его в облаке чтоб работал" (deploy to cloud so it works)

## Decision
**Provide Docker-based deployment with platform-specific guides:**
- Create `Dockerfile` (Python 3.11 slim, non-root user)
- Create `.dockerignore`
- Create `DEPLOY.md` with step-by-step for:
  1. **Railway.app** (easiest free, 500 hrs/mo)
  2. **Render** (free tier)
  3. **Fly.io** (free allowance)
  4. **VPS** (Hetzner/DigitalOcean + systemd)

## Alternatives Considered
- User didn't specify platform — provided options
- Railway recommended as "easiest free option"

## Consequences

### Positive
- Platform-agnostic Docker image
- Clear documentation for each target
- Free tier options available

### Negative
- User must choose and configure platform
- Free tiers have limitations (sleep, hours)

## Implementation Details
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot.py .
CMD ["python", "bot.py"]
```

```markdown
# DEPLOY.md - Railway example:
railway login
railway init
railway variables set TELEGRAM_BOT_TOKEN=...
railway variables set OPENROUTER_API_KEY=...
railway up
```

## Related Decisions
- ADR 008: GitLab CI/CD for automated deploy
- ADR 009: GitLab repo creation via glab