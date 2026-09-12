# ADR 015: SYN Command — CLI Synthesis Parser per Spec

## Status
Accepted (Session: 2026-09-12 05:30+)

## Context
Идея.md section 3 defines SYN syntax:
```
$syn <emotion><power>+<emotion><power> @<angle> <catalyst>.<catalyst>

Example: $syn fear8+love6 @40 metal.memory
```

## Decision
**Implement SYN parser in `cast.py` matching spec exactly:**

### Parser (`parse_cast_args`)
```python
def parse_cast_args(args: str) -> dict:
    # $syn fr8+lv6 @40 mt.mem
    # → {"name": "", "effect": "damage", "target": "enemy",
    #     "materials": {"fr": 8, "lv": 6}, "angle": 40}
```

### Emotion Codes (from spec)
| Code | Name | RU |
|---|---|---|
| fr | fear | страх |
| lv | love | любовь |
| rg | rage | ярость |
| gr | grief | горе |
| hp | hope | надежда |
| ds | desire | желание |
| pr | pride | гордость |
| vn | vengeance | месть |

### Catalyst Codes (from spec)
| Code | Name | Properties |
|---|---|---|
| mt | metal | durability, structure |
| gl | glass | precision, fragility |
| st | stone | stability, weight |
| bm | bone | necrotic, memory |
| mem | memory | identity, emotion |
| bl | blood | life, sacrifice |
| cr | crystal | clarity, resonance |

### Calculation (Game Engine)
```python
power = (sum(emotions) * 2 + len(catalysts) * 5) * (1 - abs(angle-45)/90)
instability = max(0, (power - 50) / 10)
mana_cost = max(10, power / 2)
```

### Output Format (Terminal Style)
```
> SYNTHESIS.exe
> INPUT:
  fear: 8
  love: 6
  angle: 40°
  catalysts: metal, memory
> RESOLVING...
> OUTPUT: desperate_ward_blade
> TYPE: weapon
> POWER: 82%
> ATTRIBUTES: + protection, + emotional resonance
> LIMIT: low durability
> STATUS: complete
```

## Consequences

### Positive
- Exact spec compliance
- Extensible parser for new parameters
- Deterministic calculations
- Rich terminal output

### Negative
- Complex parser for edge cases
- Angle efficiency formula hardcoded
- Catalyst properties not yet used in calc

## Related Decisions
- ADR 014: Game Engine owns this logic
- ADR 013: Architecture supports CLI commands
- ADR 016: Artifact creation on high power