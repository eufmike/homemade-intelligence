"""Orchestrates all pipeline stages for report generation."""

import json
import logging
from collections.abc import AsyncGenerator
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.agent.stage_analyze import analyze_blocking, analyze_stream
from backend.agent.stage_format import format_all_audiences
from backend.agent.stage_ingest import check_reuse_guard, retrieve_relevant_content
from backend.agent.stage_triangulate import triangulate_sources
from backend.agent.token_tracker import RunTokenTracker
from backend.database.models import Report
from backend.vector_store.chroma import upsert_report_summary

logger = logging.getLogger(__name__)


async def run_pipeline_stream(
    topic: str,
    domain: str,
    db: Session,
    manual_text: str = "",
    manual_title: str = "",
) -> AsyncGenerator[str, None]:
    """Run the full pipeline with SSE streaming of Stage 3 output.

    Yields SSE-formatted strings. The caller should forward these directly
    to the HTTP response.

    Args:
        topic: Analysis topic.
        domain: Report domain (geopolitics/markets/taiwan/energy/general).
        db: SQLAlchemy session.
        manual_text: Optional manually injected article text.
        manual_title: Title for manually injected text.

    Yields:
        SSE data strings.
    """
    tracker = RunTokenTracker()

    # --- Create report record in pending state ---
    report = Report(
        topic=topic,
        domain=domain,
        status="generating",
        created_at=datetime.now(timezone.utc),
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    yield _sse("status", {"stage": "start", "report_id": report.id})

    try:
        # --- Inject manual content if provided ---
        if manual_text:
            _inject_manual_content(manual_title or topic, manual_text, db)

        # --- Reuse guard ---
        should_warn, similarity = check_reuse_guard(topic)
        if should_warn:
            yield _sse("warning", {"message": f"Similar report exists (similarity={similarity:.2f}). Continuing."})

        # --- Stage 1: Retrieve ---
        yield _sse("status", {"stage": "ingest"})
        source_chunks, past_reports = retrieve_relevant_content(topic, db)

        # --- Stage 2: Triangulate ---
        yield _sse("status", {"stage": "triangulate"})
        bias_coverage, coverage_caveat, divergence_score = triangulate_sources(source_chunks)

        if coverage_caveat:
            yield _sse("warning", {"message": coverage_caveat})

        # --- Stage 3: Analyze (streaming) ---
        yield _sse("status", {"stage": "analyze"})
        analysis_chunks = []
        async for text in analyze_stream(
            topic, source_chunks, past_reports, bias_coverage, coverage_caveat, tracker
        ):
            analysis_chunks.append(text)
            yield _sse("token", {"text": text})

        content_en = "".join(analysis_chunks)

        # --- Stage 4: Format (concurrent) ---
        yield _sse("status", {"stage": "format"})
        content_zh_tw, content_zh_tw_elder = await format_all_audiences(content_en, topic, tracker)

        # --- Persist report ---
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

        # --- Embed summary in ChromaDB reports collection ---
        _embed_report_summary(report)

        tracker.log_summary()
        yield _sse("complete", {
            "report_id": report.id,
            "tokens_used": tracker.total_tokens_used,
            "tokens_cached": tracker.total_tokens_cached,
            "cost_usd": tracker.total_cost_usd,
        })

    except Exception as exc:
        logger.exception("Pipeline failed for topic='%s': %s", topic, exc)
        report.status = "failed"
        db.commit()
        yield _sse("error", {"message": str(exc)})


async def run_pipeline_blocking(
    topic: str,
    domain: str,
    db: Session,
    manual_text: str = "",
    manual_title: str = "",
) -> Report:
    """Run the full pipeline without streaming; returns completed Report.

    Args:
        topic: Analysis topic.
        domain: Report domain.
        db: SQLAlchemy session.
        manual_text: Optional manually injected article text.
        manual_title: Title for manually injected text.

    Returns:
        Completed Report ORM object.
    """
    tracker = RunTokenTracker()

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


def _inject_manual_content(title: str, body: str, db: Session) -> None:
    """Inject manually provided text into the ingestion pipeline."""
    try:
        from backend.ingestion.manual import inject_text

        inject_text(title=title, body=body, db=db)
    except Exception as exc:
        logger.warning("Manual inject failed: %s", exc)


def _embed_report_summary(report: Report) -> None:
    """Embed the first 800 chars of English content into ChromaDB reports collection."""
    try:
        if not report.content_en:
            return
        summary = report.content_en[:800]
        doc_id = f"report_{report.id}"
        upsert_report_summary(
            doc_id=doc_id,
            text=summary,
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
    """Format a Server-Sent Events message."""
    import json as _json

    return f"event: {event}\ndata: {_json.dumps(data)}\n\n"
