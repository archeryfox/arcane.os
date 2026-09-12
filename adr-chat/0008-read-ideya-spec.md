# ADR 008: Read Идея.md — Full Specification as Source of Truth

## Status
Accepted (Session: 2026-09-12 03:30+)

## Context
User said: "прочти файл Идея" (read the Идея file) — twice, emphasizing it's the specification.

## Decision
**Read `Идея.md` and implement the complete ARCANA.OS system per spec:**

The file contains 12 sections defining:
1. **Concept**: CLI-style magical OS, players send commands like `$syn fr8+lv6 @40 mt.mem`
2. **Terminal style**: All responses as `> COMMAND`, `> PROCESSING...`, `> OUTPUT:`, `> STATUS:`
3. **Commands**: SYN (synthesis), CAST, SCAN, MOD, NULL, STATUS
4. **Emotions**: 8 emotions (fr, lv, rg, gr, hp, ds, pr, vn) range 1-10
5. **Catalysts**: 7 materials (mt, gl, st, bm, mem, bl, cr) with properties
6. **Resonance formula**: power = (e1+e2) * catalyst_compat * angle_efficiency
7. **Other commands**: CAST, SCAN, MOD, NULL, STATUS with terminal format
8. **Errors**: Part of gameplay (emotion conflict, critical failure)
9. **AI Role separation**: Game Engine (calculations) vs AI Narrator (flavor)
10. **Storage**: SQLite with players, artifacts, history tables
11. **Tech**: Python, aiogram, SQLite, JSON/YAML, Free LLM API
12. **Core idea**: "Terminal access to hidden reality layer where magic is command execution"

## Alternatives Considered
- Continue with simple chat bot (rejected — user wants full spec implementation)

## Consequences

### Positive
- Complete alignment with user vision
- Rich game mechanics from spec
- Clear architecture: Engine vs Narrator separation

### Negative
- Significant rewrite from current simple bot
- Need SQLite, parsing, calculation engine
- More complex than MVP

## Implementation Plan (from spec)
1. Replace polling with webhook (FastAPI)
2. Add SQLite with models (Player, Artifact, History)
3. Implement SYN parser: `$syn <emotion><power>+<emotion><power> @<angle> <catalyst>.<catalyst>`
4. Implement calculation engine (deterministic)
5. Implement AI Narrator (terminal format)
6. Add commands: CAST, SCAN, MOD, NULL, STATUS
7. Add error handling per spec

## Related Decisions
- ADR 009: Unlimited spells (remove predefined)
- ADR 011: Webhook + FastAPI architecture
- ADR 012: SQLite with models