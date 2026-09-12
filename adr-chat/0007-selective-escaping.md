# ADR 007: Selective Escaping — Only AI Responses, Not Bot Messages

## Status
Accepted (Session: 2026-09-12 03:00+)

## Context
After ADR 005, bot's own messages (`/start`, `/spells`, `/cast`) were also passed through `escape_mdv2()`, breaking intentional markdown formatting (e.g., `*🔥 Огненный шар*` became literal asterisks).

## Decision
**Only escape AI responses, not bot's hardcoded messages:**

```python
# Bot messages — NO escaping (developer controls markdown)
await message.answer("*Привет!*")  # Renders as bold

# AI responses — ALWAYS escape (AI may forget rules)
await message.answer(escape_mdv2(ai_response))

# SYSTEM_PROMPT updated to enforce MarkdownV2 on AI
```

**Updated SYSTEM_PROMPT** with strict formatting rules:
> 2. Используй ТОЛЬКО Telegram MarkdownV2 форматирование:
>    *жирный* — одинарные звёздочки
>    _курсив_ — нижние подчёркивания
>    `код` — обратные кавычки
>    ~зачёркнуто~ — тильды
>    ||спойлер|| — двойные вертикальные черты
>    НЕ используй **жирный**, ## заголовки, - списки — это сломанный формат.
> 3. Экранируй спецсимволы: _ * [ ] ( ) ~ ` > # + - = | { } . !

## Alternatives Considered
- Escape everything, use HTML for bot messages (rejected — inconsistent)
- Don't escape AI, fix prompt only (rejected — AI still fails)

## Consequences

### Positive
- Bot markdown renders correctly
- AI forced to follow strict rules
- Clear separation of concerns

### Negative
- AI sometimes still outputs unescaped chars
- Must trust AI to follow prompt (imperfect)

## Implementation Details
```python
def escape_mdv2(text: str) -> str:
    return MDV2_ESCAPE.sub(r"\\\1", text)

# In handlers:
@router.message(Command("spells"))
async def cmd_spells(message: Message):
    # Bot's own markdown — no escape
    await message.answer("*Список заклинаний:*\n\n*🔥 Огненный шар* — 15 маны")

@router.message(F.text)
async def handle_message(message: Message):
    # AI response — escape
    response = await ask_openrouter(user_text)
    await message.answer(escape_mdv2(response))
```

## Related Decisions
- ADR 005: Initial MarkdownV2 switch
- ADR 006: SYSTEM_PROMPT with formatting rules