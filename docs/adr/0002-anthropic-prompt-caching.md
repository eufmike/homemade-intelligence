# Anthropic Prompt Caching via cache_control Blocks

## Context and Problem Statement

Stage 3 (base analysis) sends a static system prompt of ~7,400 tokens on every report generation call. At full input token price ($3.00/1M), this alone costs ~$0.022 per report. The Anthropic API supports `cache_control: {"type": "ephemeral"}` content blocks which cache the prefix server-side for 5 minutes at a cache-read price of $0.30/1M — a 90% reduction. The intelligence stack system prompt (analytical frameworks, source architecture, output standards, multi-audience rules) is identical across all report generations.

## Decision Drivers

* Minimize API cost per report — target under $0.02 cached vs. ~$0.04 cold
* Keep the full analytical framework in the prompt — no quality compromise
* Maintain observability — log cache hit/miss per call

## Considered Options

* `cache_control: ephemeral` on the static system block (chosen)
* No caching — pay full input price every call
* Shorter system prompt — reduce token count at the cost of depth
* Fine-tuned model with baked-in framework

## Decision Outcome

Chosen option: **`cache_control: ephemeral` on the static system block**, because it achieves ~90% cost reduction on the largest token block with zero quality tradeoff and minimal implementation complexity.

The `INTELLIGENCE_STACK_SYSTEM` string is placed in a single content block with `cache_control: {"type": "ephemeral"}` as the first element of the system parameter. All dynamic content (topic, retrieved source chunks, bias coverage summary) goes in the user message — uncached and per-request. Stage 4 (audience formatting) uses a minimal per-audience system prompt with no re-injection of the full framework.

### Consequences

* Good, because cache-read tokens cost $0.30/1M vs. $3.00/1M — 90% reduction on the ~7,400-token static block.
* Good, because back-to-back reports within the 5-minute TTL window are nearly free on the system prompt.
* Good, because `usage.cache_read_input_tokens` is logged per stage via `RunTokenTracker` and stored on the `reports` table.
* Bad, because the cache TTL is 5 minutes — only effective for rapid sequential generations; cold-start cost applies after 5 minutes idle.
* Bad, because cache-write tokens cost $3.75/1M (slightly above normal input) on the first call in a window.
* Neutral, because the API requires structured content blocks (`list[dict]`) for the system parameter instead of a plain string.

## Pros and Cons of the Options

### cache_control: ephemeral on static block

* Good, because 90% cost reduction on largest token block with no quality change.
* Good, because zero additional infrastructure.
* Neutral, because requires content block structure rather than plain system string.

### No caching

* Good, because simpler implementation.
* Bad, because ~$0.04/report instead of ~$0.016 with cache hit — unnecessary cost over time.

### Shorter system prompt

* Good, because reduces cold-start cost.
* Bad, because the analytical frameworks (triangulation, CIB checklist, failure modes) are the core value — trimming them degrades output quality.

### Fine-tuned model

* Bad, because vastly more complex and expensive to produce.
* Bad, because not appropriate for a personal tool updated frequently.

## More Information

* `backend/agent/prompts.py` — `build_system_blocks()`, `INTELLIGENCE_STACK_SYSTEM`
* `backend/agent/token_tracker.py` — per-stage cost logging
* Anthropic prompt caching documentation
