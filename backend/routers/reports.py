"""Report generation and retrieval endpoints."""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.agent.pipeline import run_pipeline_stream
from backend.database.connection import get_db
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

    Returns a Server-Sent Events stream. Events:
    - status: pipeline stage updates
    - token: streaming analysis text
    - warning: coverage or reuse warnings
    - complete: final stats
    - error: pipeline failure
    """

    async def event_generator():
        async for chunk in run_pipeline_stream(
            topic=request.topic,
            domain=request.domain,
            db=db,
            manual_text=request.manual_text,
            manual_title=request.manual_title,
        ):
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
    reports = q.order_by(Report.created_at.desc()).offset(offset).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ReportDetail)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a single report with all audience versions."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    return report


@router.get("/{report_id}/stream")
async def stream_report(report_id: int, db: Session = Depends(get_db)):
    """SSE endpoint for an in-progress report (polls status until complete)."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")

    async def poll_generator():
        import json

        for _ in range(120):  # max 10 minutes at 5s intervals
            db.refresh(report)
            yield f"event: status\ndata: {json.dumps({'status': report.status, 'report_id': report_id})}\n\n"
            if report.status in ("complete", "failed"):
                break
            await asyncio.sleep(5)

    return StreamingResponse(poll_generator(), media_type="text/event-stream")
