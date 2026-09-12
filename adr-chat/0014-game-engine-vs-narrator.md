# ADR 014: Game Engine vs AI Narrator — Separation of Concerns

## Status
Accepted (Session: 2026-09-12 05:15+)

## Context
Идея.md section 9 explicitly requires:
> **Game Engine:** calculations, balance, probabilities, characteristics
> **AI Narrator:** beautiful descriptions, atmosphere, terminal style

**Current code mixed both in handlers.**

## Decision
**Enforce strict separation in new architecture:**

### Game Engine (Deterministic, in `cast.py`)
- `parse_cast_args()` — parse `$syn` syntax
- `calculate_power()` — resonance formula: `(e1+e2) * catalyst * angle`
- `generate_effect()` — template-based descriptions
- Player state mutations (mana, XP, mental_load)
- Artifact creation (power > 60)
- History logging

### AI Narrator (Generative, in `conversation.py` + `openrouter.py`)
- Free-form chat only
- Receives player context + user message
- Returns terminal-style flavor text
- NO calculations, NO state changes

## Implementation
```python
# cast.py — GAME ENGINE
def calculate_power(parsed, player):
    total_emotion = sum(emotions.values())
    catalyst_bonus = len(emotions) * 5
    angle_eff = 1.0 - abs(angle - 45) / 90.0
    power = (total_emotion * 2 + catalyst_bonus) * angle_eff
    instability = max(0, (power - 50) / 10)
    mana_cost = max(10, int(power / 2))
    return {"power": power, "instability": instability, "mana_cost": mana_cost}

# conversation.py — AI NARRATOR
SYSTEM_PROMPT = """Ты — ARCANA.OS, древняя магическая операционная система.
СТИЛЬ: Терминал/CLI. Все ответы в формате:
> COMMAND
> PROCESSING...
> OUTPUT: [result]
> STATUS: success/error
"""

async def handle_message(message):
    # Only chat, no game mechanics
    response = await ask_openrouter(full_prompt, SYSTEM_PROMPT)
    await save_history(...)
    await message.answer(escape_mdv2(response))
```

## Consequences

### Positive
- Deterministic game balance (no AI hallucination in mechanics)
- AI focuses on narrative quality
- Testable game logic without LLM
- Matches Идея.md architecture exactly

### Negative
- Two code paths for similar output format
- Must keep terminal style consistent in both

## Related Decisions
- ADR 013: Architecture refactor enables this separation
- ADR 015: SYN command uses Game Engine
- ADR 006: SYSTEM_PROMPT for AI Narrator