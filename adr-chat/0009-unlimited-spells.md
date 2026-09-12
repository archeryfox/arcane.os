# ADR 009: Unlimited Spells — Remove Predefined Spell List

## Status
Accepted (Session: 2026-09-12 04:00+)

## Context
User said: "удали дефолтные заклинания из бота, сделай их неограниченными" (remove default spells, make them unlimited)

This aligns with Идея.md section 3: "ЗАКЛИНАНИЯ: НЕТ ПРЕДЕФИНИРОВАННОГО СПИСКА. Игрок придумывает любое название."

## Decision
**Remove `SPELLS` dict and `/spells` command entirely.**

**Update SYSTEM_PROMPT:**
> ЗАКЛИНАНИЯ: НЕТ ПРЕДЕФИНИРОВАННОГО СПИСКА. Игрок придумывает любое название. Ты генерируешь эффект, урон, стоимость маны на лету.

**Update `/cast` handler:**
- Accept any spell name: `/cast <anything>`
- LLM generates effect, damage, mana cost on the fly
- No validation against predefined list

## Alternatives Considered
- Keep some default spells as examples (rejected — contradicts spec)
- Hybrid: predefined + custom (rejected — user explicitly said "unlimited")

## Consequences

### Positive
- Full creative freedom for players
- Matches Идея.md specification exactly
- AI becomes co-creator of magic system

### Negative
- No balance guarantees (AI may give OP spells)
- Harder to test
- Mana costs inconsistent

## Implementation Details
```python
# REMOVED:
SPELLS = {...}
@router.message(Command("spells"))  # Deleted

# UPDATED SYSTEM_PROMPT:
"ЗАКЛИНАНИЯ: НЕТ ПРЕДЕФИНИРОВАННОГО СПИСКА..."

# UPDATED /cast handler:
@router.message(Command("cast"))
async def cmd_cast(message: Message):
    spell_name = args[1].strip()
    user_text = f"Кастую заклинание: {spell_name}. Опиши эффект, урон, стоимость маны."
    response = await ask_openrouter(user_text)
    await message.answer(response)
```

## Related Decisions
- ADR 003: Superseded (predefined spells)
- ADR 008: Driven by Идея.md spec
- ADR 014: Game Engine vs AI Narrator separation