# ADR 017: State Management — Redis for aiogram FSM Storage

## Status
Accepted (Session: 2026-09-12 06:00+)

## Context
aiogram 3.x requires FSM storage for multi-step conversations. With webhook + multiple instances, need shared storage.

## Decision
**Use Redis 7 + `RedisStorage` from aiogram:**

```python
# app/bot/dispatcher.py
from aiogram.fsm.storage.redis import RedisStorage

def setup_dispatcher() -> Dispatcher:
    storage = RedisStorage.from_url(settings.REDIS_URL)
    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)
    dp.include_router(cast.router)
    dp.include_router(conversation.router)
    return dp
```

**Config:** `REDIS_URL: str = "redis://localhost:6379/0"`

**Docker Compose:**
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  command: redis-server --appendonly yes
```

## Alternatives Considered
- `MemoryStorage` (rejected — not shared across instances)
- MongoDB for FSM (rejected — no native aiogram support, slower)
- In-memory with sticky sessions (rejected — doesn't scale)

## Consequences

### Positive
- **Shared state** across multiple bot instances
- **TTL support** — auto-expires stale FSM data (default 24h)
- **Pub/Sub** available for future cross-instance messaging
- **Atomic operations** via Lua scripts if needed
- **Production standard** for aiogram 3.x

### Negative
- Extra infrastructure (Redis container)
- Network hop for state access
- Not as durable as MongoDB (AOF/RDB vs WAL)

## Design Decision: FSM for Conversations Only
- **Game state** (HP, mana, inventory) → MongoDB (persistent, authoritative)
- **Conversation state** (multi-step wizard) → Redis (ephemeral, per-session)
- **Do NOT store game mechanics in FSM** — prevents inconsistencies

## Related Decisions
- ADR 013: Webhook architecture needs shared FSM
- ADR 016: MongoDB for persistent game state
- ADR 002: Docker Compose includes Redis