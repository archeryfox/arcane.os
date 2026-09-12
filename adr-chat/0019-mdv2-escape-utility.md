# ADR 019: MarkdownV2 Escape Utility — Shared Across Handlers

## Status
Accepted (Session: 2026-09-12 06:30+)

## Context
Both bot's hardcoded messages and AI responses need MarkdownV2 escaping, but with different strategies (ADR 007).

## Decision
**Create shared utility in `app/utils/logger.py`:**

```python
# app/utils/logger.py
import re

MDV2_ESCAPE = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")

def escape_mdv2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    return MDV2_ESCAPE.sub(r"\\\1", text)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # ... setup
    return logger
```

**Usage in handlers:**
```python
# app/bot/handlers/start.py
from app.utils.logger import escape_mdv2, setup_logger

async def safe_answer(message: Message, text: str) -> None:
    try:
        await message.answer(escape_mdv2(text))
    except Exception:
        logger.exception("Failed to send message")
        await message.answer("> ERROR: failed to format response")
```

**Strategy per ADR 007:**
- Bot messages: `escape_mdv2()` applied (developer controls markdown)
- AI responses: `escape_mdv2()` applied (trust but verify)

## Alternatives Considered
- Escape in each handler (rejected — DRY)
- Global middleware (rejected — different strategies needed)
- Don't escape AI (rejected — AI fails often)

## Consequences

### Positive
- Single escape function, consistent behavior
- Reusable across all handlers
- Safe fallback on send failure

### Negative
- Double-escaping risk if caller already escaped
- Must remember to import utility

## Regex Details
Escapes all MarkdownV2 special chars per Telegram spec:
`_ * [ ] ( ) ~ ` > # + - = | { } . !`

Note: `-` must be escaped in character class (`\-`) or placed at end.

## Related Decisions
- ADR 005: Initial MarkdownV2 switch
- ADR 007: Selective escaping strategy
- ADR 014: Both Game Engine and AI Narrator use terminal format