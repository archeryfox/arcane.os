# ADR 003: Spell System — 4 Predefined Spells with Dice Rolling

## Status
Accepted (Session: 2026-09-12 01:15+) → **Later Superseded by ADR 007**

## Context
User asked: "напиши базовое заклинание" (write basic spell)

## Decision
**Add 4 predefined spells with dice-based damage:**
| Spell | Mana | Damage/Effect |
|-------|------|---------------|
| 🔥 Огненный шар | 15 | 2d6+3 fire |
| ✨ Магическая стрела | 5 | 1d4+1 force (never misses) |
| 💚 Исцеление | 10 | 2d4+2 HP |
| 🛡 Щит веры | 8 | +2 AC for 1 round |

**Implementation:**
- `SPELLS` dict in bot.py
- `/spells` command lists all
- `/cast <spell>` rolls dice, applies mana cost
- `roll_dice(notation)` utility for NdN+M parsing

## Alternatives Considered
- None discussed — user asked for "basic spell", I provided 4

## Consequences

### Positive
- Immediate playable content
- Clear structure for spell system
- Dice notation extensible

### Negative
- Hardcoded spells limit creativity
- Contradicts "no predefined spells" in Идея.md

## Implementation Details
```python
SPELLS = {
    "огненный шар": {"mana": 15, "damage": "2d6+3", "type": "fire", ...},
    ...
}

@dp.message(Command("cast"))
async def cmd_cast(message: Message):
    # Parse spell name, roll dice, return formatted result
```

## Superseded By
ADR 007: Unlimited Spells — Remove predefined spells, let LLM generate on the fly