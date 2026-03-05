# Decouple Pipeline from HTTP via asyncio.Task + Queue

## Context and Problem Statement

The initial implementation ran the report generation pipeline inside the FastAPI SSE generator. When a client disconnected (browser tab close, curl timeout, network drop), Python garbage-collected the generator and killed the in-flight pipeline — leaving the `reports` row stuck in `generating` status with no content. A report takes 90–180 seconds across three LLM calls. Client disconnect during that window is a realistic scenario during normal use.

## Decision Drivers

* Reports must always reach `complete` or `failed` — no stuck `generating` rows
* The streaming UX (live tokens from Stage 3) must be preserved
* No additional infrastructure dependencies

## Considered Options

* asyncio.Task + asyncio.Queue per report (chosen)
* asyncio.shield() on the SSE generator coroutine
* FastAPI BackgroundTasks (fire-and-forget, no streaming)
* Celery + Redis for background workers
* Polling-only UI (no SSE token stream)

## Decision Outcome

Chosen option: **asyncio.Task + asyncio.Queue per report**, because it decouples pipeline execution from HTTP lifetime with zero additional dependencies and preserves the live streaming UX.

On `POST /api/reports/generate`: the endpoint creates the `Report` DB record, calls `launch_pipeline()` which registers a per-report `asyncio.Queue` in a global registry and starts the pipeline as an `asyncio.create_task`. The endpoint then streams events from the queue to the client. If the client disconnects, the SSE generator is abandoned — but the task continues writing to the queue, runs to completion, and cleans up.

`GET /api/reports/{id}/stream` reconnects to a running pipeline's queue if it is still in the registry, or falls back to DB polling if the pipeline has already finished.

### Consequences

* Good, because client disconnect no longer terminates in-flight LLM API calls.
* Good, because reports always transition to `complete` or `failed`.
* Good, because a second SSE connection can pick up live events from wherever the queue is.
* Bad, because the in-memory queue is lost on server restart — reports generating at restart remain `generating` in the DB. Mitigation: startup sweep resets orphaned rows to `failed` (to be implemented).
* Bad, because the queue is unbounded — a very long streaming response accumulates in memory until the reader drains it. Acceptable at single-user scale.
* Neutral, because each pipeline task creates its own `SessionLocal` DB session, independent of the request session.

## Pros and Cons of the Options

### asyncio.Task + asyncio.Queue

* Good, because pipeline survives client disconnect.
* Good, because live streaming is preserved.
* Good, because zero additional dependencies.
* Neutral, because requires global queue registry with cleanup.

### asyncio.shield()

* Bad, because `asyncio.shield()` prevents cancellation of the inner coroutine, but the SSE generator itself (the outer frame) is still abandoned when the client disconnects — the shielded task continues, but its output goes nowhere and the DB is never updated cleanly.

### FastAPI BackgroundTasks

* Good, because built-in to FastAPI, no queue management.
* Bad, because `BackgroundTasks` run after the response is sent — incompatible with SSE streaming where the response is the stream.

### Celery + Redis

* Bad, because requires Redis and a Celery worker process — violates zero-infrastructure constraint for a local personal tool.

### Polling-only UI

* Good, because eliminates streaming complexity entirely.
* Bad, because loses the live token-by-token UX that makes report generation feel responsive.

## More Information

* `backend/agent/pipeline.py` — `launch_pipeline()`, `_run_pipeline()`, `stream_queue()`, `_queues` registry
* `backend/routers/reports.py` — `generate_report()` endpoint
