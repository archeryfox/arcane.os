# ADR 018: Configuration — Pydantic Settings with .env

## Status
Accepted (Session: 2026-09-12 06:15+)

## Context
Need centralized, type-safe configuration for:
- MongoDB URI, database name
- Telegram bot token, webhook URL, secret token
- Redis URL
- OpenRouter API key, model
- Log level

## Decision
**Use Pydantic Settings v2 (`pydantic-settings`):**

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core
    MONGO_URI: str = ""
    MONGO_DB_NAME: str = "arcana_os"
    TELEGRAM_BOT_TOKEN: str = ""
    WEBHOOK_URL: str = ""
    TELEGRAM_WEBHOOK_SECRET_TOKEN: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    LOG_LEVEL: str = "INFO"

    # LLM
    OPENROUTER_API_KEY: str = ""
    MODEL: str = "openrouter/free"

    @property
    def webhook_configured(self) -> bool:
        return bool(self.WEBHOOK_URL and self.TELEGRAM_BOT_TOKEN)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

settings = Settings()
```

**.env.example (committed):**
```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=arcana_os
TELEGRAM_BOT_TOKEN=your_token
WEBHOOK_URL=https://domain.com/webhook
TELEGRAM_WEBHOOK_SECRET_TOKEN=generate_with_openssl_rand_hex_32
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
OPENROUTER_API_KEY=your_key
MODEL=openrouter/free
```

**.env (gitignored):**
```bash
MONGO_URI=mongodb://mongo:27017
TELEGRAM_BOT_TOKEN=8935559519:AAG2_lTlQJOCCHvBYa01L0HesQn5eZPxQus
WEBHOOK_URL=https://arcana.example.com/webhook
TELEGRAM_WEBHOOK_SECRET_TOKEN=a1b2c3d4...
OPENROUTER_API_KEY=sk-or-v1-...
```

## Alternatives Considered
- `python-dotenv` + `os.getenv` (rejected — no validation, no types)
- `dynaconf` (rejected — overkill)
- JSON/YAML config files (rejected — secrets in files)

## Consequences

### Positive
- **Type safety** — `MONGO_URI: str` validated at startup
- **Validation** — Computed properties, custom validators possible
- **IDE support** — Autocomplete, jump to definition
- **Testing** — Override via `Settings(_env_file="test.env")`
- **12-factor compliant** — Env vars, .env for local only
- **Single source of truth** — All config in one class

### Negative
- Extra dependency (`pydantic-settings`)
- Startup validation cost (negligible)

## Security
- `.env` in `.gitignore` — never committed
- `.env.example` documents required variables
- Secrets via env vars in production (GitLab CI variables, Railway, etc.)
- Webhook secret token validates Telegram origin

## Related Decisions
- ADR 013: FastAPI app uses `settings` singleton
- ADR 016: MongoDB URI from settings
- ADR 017: Redis URL from settings
- ADR 002: Deployment guides reference .env