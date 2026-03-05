"""CRUD operations for predictions."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.database.models import Prediction, PredictionOutcome
from backend.predictions.scoring import compute_brier_score, outcome_to_binary
from backend.schemas.prediction import CreatePredictionRequest


def create_prediction(request: CreatePredictionRequest, db: Session) -> Prediction:
    """Create a new prediction record.

    Args:
        request: Validated creation request.
        db: SQLAlchemy session.

    Returns:
        Created Prediction ORM object.
    """
    prediction = Prediction(
        topic=request.topic,
        prediction_text=request.prediction_text,
        confidence_pct=request.confidence_pct,
        domain=request.domain,
        deadline_date=request.deadline_date,
        report_id=request.report_id,
        metaculus_question_id=request.metaculus_question_id,
        polymarket_market_id=request.polymarket_market_id,
        metaculus_community_pct=request.metaculus_community_pct,
        polymarket_odds_pct=request.polymarket_odds_pct,
        created_at=datetime.now(timezone.utc),
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def resolve_prediction(prediction_id: int, outcome: str, notes: str, db: Session) -> Prediction:
    """Resolve a prediction and record its Brier score.

    Args:
        prediction_id: ID of the prediction to resolve.
        outcome: One of 'correct', 'incorrect', 'partial'.
        notes: Resolution context notes.
        db: SQLAlchemy session.

    Returns:
        Updated Prediction ORM object.

    Raises:
        ValueError: If prediction not found or already resolved.
    """
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise ValueError(f"Prediction {prediction_id} not found")
    if prediction.outcome is not None:
        raise ValueError(f"Prediction {prediction_id} is already resolved")

    prediction.outcome = outcome
    prediction.resolution_notes = notes
    prediction.resolved_at = datetime.now(timezone.utc)

    forecast = prediction.confidence_pct / 100.0
    outcome_binary = outcome_to_binary(outcome)
    brier = compute_brier_score(forecast, outcome_binary)

    outcome_record = PredictionOutcome(
        prediction_id=prediction.id,
        scored_at=datetime.now(timezone.utc),
        forecast=forecast,
        outcome_binary=outcome_binary,
        brier_score=brier,
    )
    db.add(outcome_record)
    db.commit()
    db.refresh(prediction)
    return prediction


def list_predictions(
    db: Session,
    domain: str | None = None,
    resolved: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Prediction]:
    """List predictions with optional filters.

    Args:
        db: SQLAlchemy session.
        domain: Filter by domain.
        resolved: True=resolved only, False=unresolved only, None=all.
        limit: Max results.
        offset: Pagination offset.

    Returns:
        List of Prediction ORM objects.
    """
    q = db.query(Prediction)
    if domain:
        q = q.filter(Prediction.domain == domain)
    if resolved is True:
        q = q.filter(Prediction.outcome.isnot(None))
    elif resolved is False:
        q = q.filter(Prediction.outcome.is_(None))
    return q.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()


def get_prediction(prediction_id: int, db: Session) -> Prediction | None:
    """Get a single prediction by ID."""
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()
