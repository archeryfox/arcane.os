# ADR 006: SYSTEM_PROMPT Injection — Game Rules in Every LLM Request

## Status
Accepted (Session: 2026-09-12 02:30+)

## Context
User asked: "как мне в него загрузить свои игровые правила при каждом запросе?" (how to load my game rules into every request?)

## Decision
**Add `SYSTEM_PROMPT` constant prepended to every OpenRouter call:**

```python
SYSTEM_PROMPT = """Ты — Мастер ARCANA.OS, текстовый RPG-бот в Telegram.
МИР: Фэнтези-сеттинг с магией, монстрами и подземельями.
ПЕРСОНАЖ ИГРОКА: У игрока есть характеристики (Сила, Ловкость, Интеллект, Харизма), HP, мана, инвентарь, золото.
ЗАКЛИНАНИЯ: НЕТ ПРЕДЕФИНИРОВАННОГО СПИСКА. Игрок придумывает любое название. Ты генерируешь эффект, урон, стоимость маны на лету.
ПРАВИЛА:
1. Отвечай в ролевом стиле, 2-4 предложения. На русском!
2. Используй ТОЛЬКО Telegram MarkdownV2 форматирование...
"""

async def ask_openrouter(text: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        ...
    }
```

## Alternatives Considered
- Per-user system prompts (rejected — single prompt for MVP)
- Separate prompt file (rejected — keep in code for version control)

## Consequences

### Positive
- Consistent game world across all interactions
- Easy to update rules in one place
- AI always has context

### Negative
- Token usage increases (system prompt sent every request)
- Prompt engineering needed for quality

## Implementation Details
- `SYSTEM_PROMPT` defined as module-level constant
- Injected as first message with `role: "system"`
- Contains: world, character, spells, GM rules, formatting rules

## Related Decisions
- ADR 005: MarkdownV2 formatting rules in prompt
- ADR 011: Идея.md as full specification source