# ADR 001: Project Transition — Chat Bot to Full RPG System

## Status
Accepted (2026-09-12)

## Context
`adr-chat/` contains 22 ADRs from the project's evolution (2026-09-12).
They document the transition from a simple Telegram chat bot to a full RPG system.

A new `adr/` folder is created for ongoing project-level decisions.

## Decision
- **`adr-chat/`** — preserved as historical record (MVP → refactor)
- **`adr/`** — new folder for current and future project decisions

## Planned ADRs in `adr/`
- Project structure (clean architecture finalization)
- Game Engine vs AI Narrator (implemented in `cast.py` / `conversation.py`)
- Database choice (MongoDB + Beanie)
- Conversation history management
- Deployment architecture
- Testing strategy

## Folder Purpose
This folder contains ADRs for the ARCANA.OS project as a whole — not just the chat interface, but the entire RPG system including game mechanics, commands, AI integration, and infrastructure.

## Related
- `adr-chat/` — historical ADRs (0001–0022)
- `Идея.md` — full game specification
- `README.md` — project overview
