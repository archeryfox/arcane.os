# ARCANA.OS

> Терминал доступа к скрытому слою реальности, где магия — это выполнение команд.

Telegram-бот для текстовой RPG с CLI-стилем взаимодействия. Игроки отправляют команды в стиле Linux-терминала для взаимодействия с игровым миром.

---

## Содержание

- [Возможности](#возможности)
- [Технологии](#технологии)
- [Быстрый старт](#быстрый-старт)
- [Команды](#команды)
- [Игровые механики](#игровые-механики)
- [Архитектура](#архитектура)
- [Развертывание](#развертывание)
- [Конфигурация](#конфигурация)
- [Логирование](#логирование)
- [Документация](#документация)

---

## Возможности

- **CLI-команды** — `SYN`, `CAST`, `SCAN`, `MODIFY`, `NULL`, `STATUS` в стиле терминала
- **AI Narrator** — GPT-модель описывает мир и реакцию в терминальном стиле
- **Game Engine** — детерминированные расчёты: резонанс, урон, мана, стабильность
- **Markdown форматирование** — AI-ответы с жирным, курсивом, кодом через Telegram HTML
- **Разговорная история** — бот помнит контекст диалога (до 20 сообщений per user)

## Технологии

| Компонент | Технология |
|---|---|
| Bot framework | aiogram 3.x |
| HTTP client | aiohttp |
| LLM | OpenRouter (`openrouter/free` / `openrouter/auto`) |
| Markdown конвертер | chatgpt-md-converter |
| Config | Pydantic Settings v2 + .env |
| Logging | logging + RotatingFileHandler |
| БД | MongoDB + Beanie (план) |
| State | Redis FSM (план) |
| Webhook | FastAPI (план) |

## Быстрый старт

### Локально

```bash
cd /var/home/kyle/Projects/arcane.os

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте .env с токенами
cp .env.example .env
# Отредактируйте .env
nano .env

# Запустите
python bot.py
```

### Docker

```bash
docker build -t arcana-os .
docker run --env-file .env arcana-os
```

### Docker Compose

```bash
docker compose -f docker-compose.dev.yaml up --build
```

## Команды

| Команда | Описание |
|---|---|
| `/start` | Приветствие и список команд |
| `/cast <заклинание>` | Каст заклинания (без ограничений) |
| `/reset` | Сбросить историю разговора |
| Свободный текст | Диалог с AI Narrator |

### Пример

```
Пользователь: /cast огненный шар

Бот:
> CAST.exe
> loading fire.protocol...
> OUTPUT: flame_projectile
> POWER: 35
> STABILITY: 91%
> STATUS: executed
```

## Игровые механики

Подробная спецификация: [`Идея.md`](Идея.md)

- **SYN** (`$syn fr8+lv6 @40 mt.mem`) — синтез: создаёт эффекты, артефакты, способности
- **Эмоции** (fr, lv, rg, gr, hp, ds, pr, vn) — источник энергии, 1–10
- **Катализаторы** (mt, gl, st, bm, mem, bl, cr) — материалы с уникальными свойствами
- **Резонанс** — формула: `power = (e1+e2) * catalyst * angle_efficiency`
- **CAST** — исполнение способности
- **SCAN** — анализ артефакта
- **NULL** — удаление концепции (опасно!)
- **STATUS** — статус персонажа
- **Ошибки** — часть игрового процесса (emotion conflict, critical failure)

## Архитектура

```
app/
├── main.py              # FastAPI + webhook + lifespan
├── config.py            # Pydantic Settings
├── database.py          # DB initialization
├── models/              # Domain entities (Beanie Documents)
│   ├── player.py
│   ├── artifact.py
│   └── history.py
├── services/            # Application services
│   └── openrouter.py    # LLM service
├── bot/                 # Telegram adapter
│   ├── dispatcher.py
│   ├── handlers/        # start, cast, conversation
│   └── polling.py       # Fallback
└── utils/
    └── logger.py        # setup_logger, format_ai_response

bot.py                   # Entry point (legacy polling)
logs/                    # .log files
adr-chat/                # 22 ADR
Идея.md                  # Game specification
```

## Развертывание

Подробнее: [`DEPLOY.md`](DEPLOY.md)

### Railway (бесплатный)
```bash
railway login
railway init
railway variables set TELEGRAM_BOT_TOKEN=...
railway variables set OPENROUTER_API_KEY=...
railway up
```

### Render
- Web Service из GitHub
- Build: `pip install -r requirements.txt`
- Start: `python bot.py`

### Fly.io
```bash
flyctl launch --no-deploy
flyctl secrets set TELEGRAM_BOT_TOKEN=xxx OPENROUTER_API_KEY=xxx
flyctl deploy
```

### VPS
- DigitalOcean ($4/mo) / Hetzner (€4/mo)
- systemd + Docker

## Конфигурация

Все настройки через `.env`:

```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=arcana_os
TELEGRAM_BOT_TOKEN=your_token
OPENROUTER_API_KEY=your_key
WEBHOOK_URL=https://domain.com/webhook
REDIS_URL=redis://localhost:6379/0
MODEL=openrouter/free
```

Файл `.env` в `.gitignore`. Пример: `.env.example`.

## Логирование

Логи пишутся в `logs/`:

| Файл | Уровень |
|---|---|
| `logs/arcana_os.log` | INFO+ |
| `logs/arcana_os_errors.log` | ERROR+ |

Ротация: 5 MB на файл, 5 бэкапов.

```python
from app.utils.logger import setup_logger
logger = setup_logger("arcana_os")
```

## Документация

| Ресурс | Описание |
|---|---|
| [`adr/`](adr/0001-project-transition.md) | Проектные ADR (актуальные) |
| [`adr-chat/`](adr-chat/0001-initial-bot-structure.md) | Исторические ADR (0001–0022) |
| [`Идея.md`](Идея.md) | Полная спецификация игры (12 секций) |
| [`DEPLOY.md`](DEPLOY.md) | Руководство по развёртыванию |
| [`ADR 013`](adr-chat/0013-architecture-refactor-fastapi-webhook.md) | Архитектура: FastAPI + webhook |
| [`ADR 014`](adr-chat/0014-game-engine-vs-narrator.md) | Game Engine vs AI Narrator |

---

> ARCANA.OS — не бот-рассказчик. Это терминал доступа к скрытому слою реальности, где магия — выполнение команд. Игроки не произносят заклинания. Они делают запросы. Мир отвечает.
