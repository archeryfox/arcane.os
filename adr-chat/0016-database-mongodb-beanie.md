# ADR 016: Database — MongoDB + Beanie ODM (vs Spec's SQLite)

## Status
Accepted (Session: 2026-09-12 05:45+)

## Context
Идея.md section 10 specifies SQLite:
```sql
players: id, name, level, mana, resonance
artifacts: id, owner, type, power, effects
history: command, result, timestamp
```

**Implementation chose MongoDB + Beanie instead.**

## Decision
**Use MongoDB 7 + Beanie ODM (async) instead of SQLite.**

### Models (Beanie Documents)
```python
# app/models/player.py
class Player(Document):
    telegram_id: int
    username: str | None
    level: int = 1
    xp: int = 0
    hp: int = 100
    max_hp: int = 100
    mana: int = 100
    max_mana: int = 100
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    charisma: int = 10
    resonance: float = 0.0
    mental_load: float = 0.0
    unstable_effects: int = 0
    gold: int = 0
    inventory: list[str] = []
    equipped: list[str] = []

# app/models/artifact.py
class Artifact(Document):
    owner_id: int
    name: str
    type: str
    power: float
    effects: list[str]
    emotions_used: dict[str, int]
    catalysts_used: list[str]
    resonance_angle: int | None

# app/models/history.py
class History(Document):
    player_id: int
    command: str
    command_type: str
    args: dict
    success: bool
    output: str
    mana_cost: int | None
    xp_gained: int | None
    artifacts_created: list[str]
```

## Alternatives Considered
- SQLite + aiosqlite (per spec)
- PostgreSQL + SQLAlchemy
- Redis only (rejected — not persistent)

## Consequences

### Positive
- **Async native** — Beanie uses Motor (async MongoDB driver)
- **Flexible schema** — Add fields without migrations (game evolving)
- **Rich queries** — Aggregation for analytics, leaderboards
- **Horizontal scaling** — Sharding by telegram_id when needed
- **Pydantic integration** — Models are Pydantic, validation built-in
- **Indexes** — Compound indexes on telegram_id, owner_id, player_id

### Negative
- Deviates from spec (SQLite)
- More infrastructure (MongoDB + Redis vs single SQLite file)
- Higher memory usage
- Overkill for current scale

## Rationale for Deviation
1. **Async requirement** — FastAPI + aiogram need async DB
2. **Schema evolution** — Game mechanics changing rapidly
3. **Production readiness** — MongoDB scales, SQLite doesn't
4. **Team familiarity** — Beanie + Motor well-known pattern

## Related Decisions
- ADR 013: Architecture refactor uses MongoDB
- ADR 015: SYN command stores artifacts in MongoDB
- ADR 002: Deployment includes MongoDB in docker-compose