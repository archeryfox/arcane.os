# ADR 005: Formatting Fix — Switch to MarkdownV2 with Escape Function

## Status
Accepted (Session: 2026-09-12 02:00+)

## Context
Bot crashed with `TelegramBadRequest: can't parse entities: Unsupported start tag "заклинание" at byte offset 58`

**Root cause:** Bot used `ParseMode.HTML` but SYSTEM_PROMPT told AI to output Markdown (`**bold**`, `*italic*`).

## Decision
**Switch to `ParseMode.MARKDOWN_V2` and add `escape_mdv2()` function:**

```python
MDV2_ESCAPE = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")

def escape_mdv2(text: str) -> str:
    return MDV2_ESCAPE.sub(r"\\\1", text)
```

**Update SYSTEM_PROMPT** to specify MarkdownV2 syntax:
- `*bold*` (single asterisk)
- `_italic_` (underscore)
- `` `code` `` (backtick)
- `~strikethrough~`
- `||spoiler||`
- Escape special chars: `_ * [ ] ( ) ~ ` > # + - = | { } . !`

## Alternatives Considered
- Keep HTML mode, update prompt to HTML tags (rejected — Markdown more natural for AI)
- Don't escape, trust AI (rejected — AI consistently outputs unescaped chars)

## Consequences

### Positive
- Proper formatting in Telegram
- AI outputs natural Markdown
- Single escape function handles all special chars

### Negative
- Must escape ALL bot messages too (initial bug: "Привет!" had unescaped `!`)
- AI sometimes forgets escaping rules

## Implementation Details
```python
# Bot creation
bot = Bot(token=..., default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

# In handlers: escape AI response before sending
await message.answer(escape_mdv2(ai_response))

# In SYSTEM_PROMPT: strict rules for AI
```

## Bug Fixed Later
Initial fix escaped bot's own messages too, breaking intentional markdown. Fixed in ADR 006.