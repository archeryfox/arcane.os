# ADR 001: Initial Project Structure — Single File Bot with aiogram 3

## Status
Accepted (Session: 2026-09-12 00:43)

## Context
User asked to create a Telegram bot on Python with aiogram 3 that:
- Receives messages from Telegram
- Sends text to OpenRouter API
- Returns model response to user
- Uses TELEGRAM_BOT_TOKEN and OPENROUTER_API_KEY from environment
- Creates .env for local secrets, adds to .gitignore
- Creates requirements.txt
- Installs dependencies and verifies startup

## Decision
**Create single-file bot.py with:**
- aiogram 3.x polling bot
- aiohttp for OpenRouter API calls
- python-dotenv for .env loading
- System prompt with basic RPG rules
- /start and /cast commands
- Free model routing via `openrouter/auto`

## Alternatives Considered
None discussed — user gave explicit requirements.

## Consequences

### Positive
- Minimal viable bot in one file
- Fast iteration, easy to understand
- Direct control over prompt engineering

### Negative
- No separation of concerns
- Hard to test
- All logic in one file

## Implementation Details
```python
# bot.py - single file with:
# - Bot + Dispatcher setup
# - SYSTEM_PROMPT constant
# - ask_openrouter() function
# - /start, /cast handlers
# - Dice rolling utility
# - Polling main()
```

## Related Decisions
- ADR 002: Free model selection
- ADR 003: MarkdownV2 formatting fix
- ADR 004: SYSTEM_PROMPT for game rules