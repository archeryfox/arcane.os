# ADR 022: Project Structure — Clean Architecture with Layered Modules

## Status
Accepted (Session: 2026-09-12 07:15+)

## Context
Architecture refactor (ADR 013) established this structure:

```
ARCANA.OS/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI composition root
│   ├── config.py            # Pydantic Settings
│   ├── database.py          # MongoDB + Beanie init
│   ├── models/              # Domain entities (pure Python)
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── artifact.py
│   │   └── history.py
│   ├── services/            # Application services (use cases)
│   │   ├── __init__.py
│   │   └── openrouter.py    # LLM port implementation
│   ├── bot/                 # Telegram adapter (framework-specific)
│   │   ├── __init__.py
│   │   ├── instance.py      # Bot singleton
│   │   ├── dispatcher.py    # Router registration
│   │   ├── handlers/        # Command/message handlers
│   │   │   ├── __init__.py
│   │   │   ├── start.py     # /start, /help
│   │   │   ├── cast.py      # /cast + SYN parser (Game Engine)
│   │   │   └── conversation.py  # Free chat (AI Narrator)
│   │   ├── menu.py          # Bot commands menu
│   │   └── polling.py       # Polling fallback
│   └── utils/               # Shared utilities
│       ├── __init__.py
│       └── logger.py        # escape_mdv2, setup_logger
├── bot.py                   # Legacy polling entry (kept for compat)
├── docker-compose.yaml
├── docker-compose.dev.yaml
├── docker-compose.prod.yaml
├── Dockerfile
├── .gitlab-ci.yml
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── DEPLOY.md
├── README.md
└── Идея.md                  # Original spec (Russian)
```

## Dependency Rule (Clean Architecture)
```
Outer → Inner (never reverse)
┌─────────────────────────────────────┐
│ Interfaces (Telegram, HTTP, LLM)   │  ← app/bot/, app/main.py
├─────────────────────────────────────┤
│ Application Services (Use Cases)   │  ← app/services/
├─────────────────────────────────────┤
│ Domain Models (Entities)           │  ← app/models/
├─────────────────────────────────────┤
│ Infrastructure (DB, Config, Log)   │  ← config.py, database.py, utils/
└─────────────────────────────────────┘
```

## Consequences

### Positive
- **Testable** — Services use ports, mock in unit tests
- **Swappable** — Change Telegram, LLM, DB without touching domain
- **Maintainable** — Clear boundaries, single responsibility
- **Onboarding** — Obvious where to add features

### Negative
- **More files** — Boilerplate for small features
- **Indirection** — Handler → Service → Model hops
- **Over-engineering risk** — Resist premature abstractions

## Current vs Target

| Layer | Current | Target |
|---|---|---|
| Models | ✅ Beanie Documents | ✅ Pure domain logic |
| Services | ⚠️ `openrouter.py` only | Extract `GameService`, `ArtifactService` |
| Handlers | ⚠️ Logic in handlers | Thin adapters → services |
| Composition | ⚠️ Implicit | Explicit in `main.py` lifespan |

## Refactoring Plan (Incremental)
1. Extract `GameService` from `cast.py` calculation logic
2. Extract `ArtifactService` from artifact creation
3. Introduce `LLMPort` protocol for `OpenRouterAdapter`
4. Wire services in `main.py` lifespan, inject via `app.state`
5. Add unit tests for services with mocked ports

## Related Decisions
- ADR 013: Architecture refactor created this structure
- ADR 014: Game Engine vs AI Narrator separation
- ADR 018: Config in composition root