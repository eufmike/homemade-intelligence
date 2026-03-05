"""Orchestrates all pipeline stages for report generation.

Architecture: the pipeline runs as an asyncio.Task (decoupled from HTTP).
Events are written to a per-report asyncio.Queue. The SSE endpoint reads
from the queue and forwards to the client. Client disconnect does NOT kill
the pipeline — it runs to completion regardless.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone

from backend.agent.stage_analyze import analyze_blocking, analyze_stream
from backend.agent.stage_format import format_all_audiences
from backend.agent.stage_ingest import check_reuse_guard, retrieve_relevant_content
from backend.agent.stage_triangulate import triangulate_sources
from backend.agent.token_tracker import RunTokenTracker
from backend.database.models import Report
from backend.vector_store.chroma import upsert_report_summary

logger = logging.getLogger(__name__)

# Global registry: report_id -> asyncio.Queue of SSE event strings
# Entries are cleaned up when the pipeline task completes.
_queues: dict[int, asyncio.Queue] = {}

_SENTINEL = object()  # signals end-of-stream to queue readers


def get_event_queue(report_id: int) -> asyncio.Queue | None:
    """Return the active event queue for a report, or None if not running."""
    return _queues.get(report_id)


async def launch_pipeline(
    report_id: int,
    topic: str,
    domain: str,
    manual_text: str = "",
    manual_title: str = "",
) -> asyncio.Task:
    """Launch the pipeline as an independent background task.

    Creates a queue for the report_id and starts the task. The queue
    lives until the task writes the sentinel and the reader drains it.

    Args:
        report_id: Pre-created report DB id (status='generating').
        topic: Analysis topic.
        domain: Report domain.
        manual_text: Optional manually injected article text.
        manual_title: Title for manually injected text.

    Returns:
        The running asyncio.Task.
    """
    queue: asyncio.Queue = asyncio.Queue()
    _queues[report_id] = queue

    task = asyncio.create_task(
        _run_pipeline(report_id, topic, domain, manual_text, manual_title, queue),
        name=f"pipeline-report-{report_id}",
    )
    return task


async def _run_pipeline(
    report_id: int,
    topic: str,
    domain: str,
    manual_text: str,
    manual_title: str,
    queue: asyncio.Queue,
) -> None:
    """Core pipeline logic. Runs independently of any HTTP connection.

    Writes SSE-formatted strings to queue. Puts _SENTINEL when done.
    Always updates the report DB record to 'complete' or 'failed'.
    """
    from backend.database.connection import SessionLocal

    tracker = RunTokenTracker()

    async def emit(event: str, data: dict) -> None:
        await queue.put(_sse(event, data))

    with SessionLocal() as db:
        report = db.get(Report, report_id)
        if not report:
            logger.error("Pipeline: report %d not found", report_id)
            await queue.put(_SENTINEL)
            _queues.pop(report_id, None)
            return

        try:
            await emit("status", {"stage": "start", "report_id": report_id})

            if manual_text:
                _inject_manual_content(manual_title or topic, manual_text, db)

            should_warn, similarity = check_reuse_guard(topic)
            if should_warn:
                await emit("warning", {"message": f"Similar report exists (similarity={similarity:.2f}). Continuing."})

            await emit("status", {"stage": "ingest"})
            source_chunks, past_reports = retrieve_relevant_content(topic, db)

            await emit("status", {"stage": "triangulate"})
            bias_coverage, coverage_caveat, divergence_score = triangulate_sources(source_chunks)
            if coverage_caveat:
                await emit("warning", {"message": coverage_caveat})

            await emit("status", {"stage": "analyze"})
            analysis_chunks: list[str] = []
            async for text in analyze_stream(
                topic, source_chunks, past_reports, bias_coverage, coverage_caveat, tracker
            ):
                analysis_chunks.append(text)
                await emit("token", {"text": text})

            content_en = "".join(analysis_chunks)

            await emit("status", {"stage": "format"})
            content_zh_tw, content_zh_tw_elder = await format_all_audiences(content_en, topic, tracker)

            source_ids = [c.get("metadata", {}).get("ingested_content_id") for c in source_chunks]
            source_ids = [s for s in source_ids if s]

            report.status = "complete"
            report.bias_score = divergence_score
            report.content_en = content_en
            report.content_zh_tw = content_zh_tw
            report.content_zh_tw_elder = content_zh_tw_elder
            report.source_ids_json = json.dumps(source_ids)
            report.tokens_used = tracker.total_tokens_used
            report.tokens_cached = tracker.total_tokens_cached
            report.cost_usd = tracker.total_cost_usd
            report.completed_at = datetime.now(timezone.utc)
            db.commit()

            _embed_report_summary(report)
            tracker.log_summary()

            await emit("complete", {
                "report_id": report_id,
                "tokens_used": tracker.total_tokens_used,
                "tokens_cached": tracker.total_tokens_cached,
                "cost_usd": tracker.total_cost_usd,
            })

        except Exception as exc:
            logger.exception("Pipeline failed for report %d: %s", report_id, exc)
            report.status = "failed"
            db.commit()
            await emit("error", {"message": str(exc)})

        finally:
            await queue.put(_SENTINEL)
            _queues.pop(report_id, None)


async def stream_queue(report_id: int, queue: asyncio.Queue):
    """Async generator that yields SSE strings from the queue until sentinel.

    Safe to abandon — the pipeline task continues independently.

    Args:
        report_id: Report ID (for logging).
        queue: The event queue for this pipeline run.

    Yields:
        SSE-formatted strings.
    """
    while True:
        item = await queue.get()
        if item is _SENTINEL:
            # Put it back so a second reader (reconnect) also gets it
            await queue.put(_SENTINEL)
            break
        yield item


async def run_pipeline_blocking(
    topic: str,
    domain: str,
    manual_text: str = "",
    manual_title: str = "",
) -> Report:
    """Run the full pipeline and return the completed Report (no streaming).

    Creates its own DB session. Used by tests and CLI.

    Args:
        topic: Analysis topic.
        domain: Report domain.
        manual_text: Optional manually injected article text.
        manual_title: Title for manually injected text.

    Returns:
        Completed Report ORM object.
    """
    from backend.database.connection import SessionLocal

    tracker = RunTokenTracker()

    with SessionLocal() as db:
        report = Report(
            topic=topic,
            domain=domain,
            status="generating",
            created_at=datetime.now(timezone.utc),
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        try:
            if manual_text:
                _inject_manual_content(manual_title or topic, manual_text, db)

            source_chunks, past_reports = retrieve_relevant_content(topic, db)
            bias_coverage, coverage_caveat, divergence_score = triangulate_sources(source_chunks)

            content_en = await analyze_blocking(
                topic, source_chunks, past_reports, bias_coverage, coverage_caveat, tracker
            )
            content_zh_tw, content_zh_tw_elder = await format_all_audiences(content_en, topic, tracker)

            source_ids = [c.get("metadata", {}).get("ingested_content_id") for c in source_chunks]
            source_ids = [s for s in source_ids if s]

            report.status = "complete"
            report.bias_score = divergence_score
            report.content_en = content_en
            report.content_zh_tw = content_zh_tw
            report.content_zh_tw_elder = content_zh_tw_elder
            report.source_ids_json = json.dumps(source_ids)
            report.tokens_used = tracker.total_tokens_used
            report.tokens_cached = tracker.total_tokens_cached
            report.cost_usd = tracker.total_cost_usd
            report.completed_at = datetime.now(timezone.utc)
            db.commit()

            _embed_report_summary(report)
            tracker.log_summary()

        except Exception as exc:
            logger.exception("Blocking pipeline failed: %s", exc)
            report.status = "failed"
            db.commit()
            raise

        return report


def _inject_manual_content(title: str, body: str, db) -> None:
    try:
        from backend.ingestion.manual import inject_text
        inject_text(title=title, body=body, db=db)
    except Exception as exc:
        logger.warning("Manual inject failed: %s", exc)


def _embed_report_summary(report: Report) -> None:
    try:
        if not report.content_en:
            return
        doc_id = f"report_{report.id}"
        upsert_report_summary(
            doc_id=doc_id,
            text=report.content_en[:800],
            metadata={
                "report_id": report.id,
                "topic": report.topic,
                "domain": report.domain or "",
                "created_at": report.created_at.isoformat() if report.created_at else "",
                "bias_score": report.bias_score or 0.0,
            },
        )
        report.chroma_doc_id = doc_id
    except Exception as exc:
        logger.warning("ChromaDB report embedding failed: %s", exc)


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
