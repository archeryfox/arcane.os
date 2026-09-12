# ADR 004: Model Selection — Free Models Only via openrouter/auto

## Status
Accepted (Session: 2026-09-12 01:30+)

## Context
User asked: "сделай по дефолту бесплатные модели" (make free models default)

## Decision
**Change default model to `openrouter/auto`** — OpenRouter automatically routes to available free models.

**Document free models in code:**
```python
FREE_MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-2-9b-it:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]
MODEL = "openrouter/auto"
```

## Alternatives Considered
- Direct model selection (rejected — user wanted free default)
- Specific free model (rejected — auto is more resilient)

## Consequences

### Positive
- Zero cost for development
- Automatic fallback between free models
- No model management needed

### Negative
- Free models have rate limits
- Quality varies between models
- Requires OpenRouter account with payment method (even for free tier)

## Implementation Details
- `openrouter/auto` picks best available free model
- `:free` suffix ensures no charge
- Listed `FREE_MODELS` for reference/debugging

## Related Decisions
- ADR 010: OpenRouter 402 error → need credits on account