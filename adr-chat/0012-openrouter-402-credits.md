# ADR 012: OpenRouter 402 Error — Free Tier Requires Account Credits

## Status
Accepted (Session: 2026-09-12 03:45+)

## Context
Bot crashed with `OpenRouter error 402: Insufficient credits. This account never purchased credits.`

## Decision
**Document that "free" models on OpenRouter require:**
1. OpenRouter account
2. Payment method added (credit card)
3. Minimum $5 credits purchased
4. Then free models work via `openrouter/auto`

**Code handles 402 gracefully:**
```python
if resp.status != 200:
    error_text = await resp.text()
    logger.error(f"OpenRouter error {resp.status}: {error_text}")
    return "Ошибка при обращении к OpenRouter API"
```

**Alternative providers mentioned:**
- Together.ai
- Groq
- Local models (Ollama)

## Alternatives Considered
- Switch provider immediately (rejected — user wanted to try OpenRouter first)
- Add credits (user's responsibility)

## Consequences

### Positive
- Clear documentation of OpenRouter requirement
- Graceful error handling in bot
- Alternative providers listed

### Negative
- "Free" is misleading — requires payment method
- Blocks development until credits added
- User friction

## Implementation Details
- Bot returns Russian error message on 402
- Logs full error for debugging
- No crash on API failure

## Resolution
User added credits → bot worked with `openrouter/auto`

## Related Decisions
- ADR 004: Model selection `openrouter/auto`
- ADR 008: Идея.md says "Free LLM API" — OpenRouter qualifies with credits