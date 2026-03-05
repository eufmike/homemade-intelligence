"""Report generation and retrieval endpoints."""

import asyncio
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.agent.pipeline import get_event_queue, launch_pipeline, stream_queue
from backend.database.connection import SessionLocal, get_db
from backend.database.models import Report
from backend.schemas.report import GenerateReportRequest, ReportDetail, ReportSummary

router = APIRouter(prefix="/api/reports", tags=["reports"])
logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_report(
    request: GenerateReportRequest,
    db: Session = Depends(get_db),
):
    """Start report generation and stream SSE output.

    Creates the report record, launches the pipeline as an independent
    background task (survives client disconnect), and streams events
    from the task's queue until completion.

    Events:
    - status: pipeline stage updates
    - token: streaming analysis text
    - warning: coverage or reuse warnings
    - complete: final stats
    - error: pipeline failure
    """
    # Create the report record upfront so we can return its ID in the first event
    report = Report(
        topic=request.topic,
        domain=request.domain,
        status="generating",
        created_at=datetime.now(timezone.utc),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    report_id = report.id

    # Launch pipeline as independent background task
    await launch_pipeline(
        report_id=report_id,
        topic=request.topic,
        domain=request.domain,
        manual_text=request.manual_text,
        manual_title=request.manual_title,
    )

    queue = get_event_queue(report_id)

    async def event_generator():
        if queue is None:
            yield "event: error\ndata: {\"message\": \"Pipeline failed to start\"}\n\n"
            return
        async for chunk in stream_queue(report_id, queue):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("", response_model=list[ReportSummary])
def list_reports(
    domain: str | None = None,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List reports with optional domain and status filters."""
    q = db.query(Report)
    if domain:
        q = q.filter(Report.domain == domain)
    if status:
        q = q.filter(Report.status == status)
    return q.order_by(Report.created_at.desc()).offset(offset).limit(limit).all()


@router.get("/{report_id}", response_model=ReportDetail)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a single report with all audience versions."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    return report


@router.get("/{report_id}/stream")
async def stream_report(report_id: int, db: Session = Depends(get_db)):
    """SSE for an in-progress report: forwards from queue if running, else polls DB."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")

    queue = get_event_queue(report_id)

    async def generator():
        import json

        # If pipeline is still running, forward from its queue
        if queue is not None:
            async for chunk in stream_queue(report_id, queue):
                yield chunk
            return

        # Otherwise poll DB for status
        with SessionLocal() as poll_db:
            rep = poll_db.get(Report, report_id)
            for _ in range(120):
                if rep:
                    poll_db.refresh(rep)
                    yield f"event: status\ndata: {json.dumps({'status': rep.status, 'report_id': report_id})}\n\n"
                    if rep.status in ("complete", "failed"):
                        break
                await asyncio.sleep(5)

    return StreamingResponse(generator(), media_type="text/event-stream")
