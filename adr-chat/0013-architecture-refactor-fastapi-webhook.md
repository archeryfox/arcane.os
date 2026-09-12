# ADR 013: Architecture Refactor — FastAPI Webhook + SQLite + Clean Structure

## Status
Accepted (Session: 2026-09-12 05:00+)

## Context
After reading Идея.md, user wanted full implementation. The single-file polling bot was replaced with:

**New Architecture:**
```
app/
├── main.py              # FastAPI + webhook + lifespan
├── config.py            # Pydantic Settings
├── database.py          # MongoDB + Beanie (Note: spec said SQLite)
├── models/
│   ├── player.py        # Player document
│   ├── artifact.py      # Artifact document
│   └── history.py       # History document
├── bot/
│   ├── instance.py      # Bot singleton
│   ├── dispatcher.py    # Router registration
│   ├── handlers/
│   │   ├── start.py     # /start, /help
│   │   ├── cast.py      # /cast with SYN parsing
│   │   └── conversation.py  # Free chat with AI
│   ├── menu.py          # Bot commands menu
│   └── polling.py       # Polling fallback
└── services/
    └── openrouter.py    # LLM service
```

**Key Changes:**
1. **Webhook** instead of polling (`/webhook` endpoint + BackgroundTasks)
2. **MongoDB + Beanie** instead of SQLite (spec said SQLite, but MongoDB chosen)
3. **Redis** for aiogram FSM storage
4. **Clean Architecture** separation (models, services, handlers)
5. **SYN command parser** per spec: `$syn fr8+lv6 @40 mt.mem`
6. **Deterministic Game Engine** in `cast.py` (calculations)
7. **AI Narrator** in `conversation.py` (flavor text)

## Decision
**Refactor to production-ready architecture per Идея.md with adaptations:**

| Spec | Implementation | Reason |
|---|---|---|
| SQLite | MongoDB + Beanie | Better for async, horizontal scaling |
| Polling | Webhook | Production standard, scales |
| Single file | Layered modules | Maintainability, testing |

## Consequences

### Positive
- Production-ready (webhook, health check, graceful shutdown)
- Horizontal scaling support (Redis FSM, multiple instances)
- Clean separation: Game Engine (deterministic) vs AI Narrator (generative)
- Extensible handler system

### Negative
- More complex than single-file bot
- MongoDB instead of spec's SQLite
- Requires Redis infrastructure

## Implementation Details
```python
# app/main.py - FastAPI with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await init_db()  # MongoDB
    dp = setup_dispatcher()   # Redis FSM
    await bot.set_webhook(WEBHOOK_URL)
    yield
    await bot.delete_webhook()
    client.close()

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_update, update, dp)
    return {"ok": True}
```

## Related Decisions
- ADR 008: Driven by Идея.md
- ADR 014: Game Engine vs AI Narrator separation
- ADR 015: SYN command implementation
- ADR 016: MongoDB + Beanie choice