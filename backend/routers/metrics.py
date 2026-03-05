"""Performance metrics and calibration endpoints."""

from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import Prediction, PredictionOutcome
from backend.predictions.scoring import compute_brier_by_domain, compute_calibration_curve, compute_overall_brier

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/brier")
def brier_scores(domain: str | None = None, db: Session = Depends(get_db)):
    """Return Brier scores: overall and per-domain breakdown."""
    overall = compute_overall_brier(db, domain=domain)
    by_domain = compute_brier_by_domain(db) if not domain else []
    return {"overall": overall, "by_domain": by_domain}


@router.get("/calibration")
def calibration_curve(n_bins: int = 10, db: Session = Depends(get_db)):
    """Return calibration curve data for plotting."""
    return {"bins": compute_calibration_curve(db, n_bins=n_bins)}


@router.get("/accuracy-timeline")
def accuracy_timeline(
    granularity: str = "weekly",
    domain: str | None = None,
    db: Session = Depends(get_db),
):
    """Return rolling accuracy over time grouped by day or week.

    Args:
        granularity: 'daily' or 'weekly'.
        domain: Optional domain filter.
    """
    rows = (
        db.query(PredictionOutcome, Prediction.domain, Prediction.resolved_at)
        .join(Prediction)
        .filter(Prediction.resolved_at.isnot(None))
    )
    if domain:
        rows = rows.filter(Prediction.domain == domain)
    rows = rows.all()

    if not rows:
        return {"timeline": []}

    # Group by period
    buckets: dict[str, list[float]] = {}
    for outcome_row, dom, resolved_at in rows:
        if not resolved_at:
            continue
        if granularity == "daily":
            key = resolved_at.date().isoformat()
        else:
            # ISO week
            iso = resolved_at.isocalendar()
            key = f"{iso.year}-W{iso.week:02d}"

        buckets.setdefault(key, []).append(outcome_row.outcome_binary)

    timeline = []
    for period in sorted(buckets):
        values = buckets[period]
        accuracy = sum(1 for v in values if v >= 0.5) / len(values)
        mean_brier = sum((f - o) ** 2 for f, o in [(0.5, v) for v in values]) / len(values)
        timeline.append({
            "period": period,
            "count": len(values),
            "accuracy": round(accuracy, 4),
        })

    return {"timeline": timeline, "granularity": granularity}
