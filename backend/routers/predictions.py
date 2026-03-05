"""Prediction CRUD and resolution endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.predictions.crud import (
    create_prediction,
    get_prediction,
    list_predictions,
    resolve_prediction,
)
from backend.schemas.prediction import (
    CreatePredictionRequest,
    PredictionSummary,
    ResolvePredictionRequest,
)

router = APIRouter(prefix="/api/predictions", tags=["predictions"])
logger = logging.getLogger(__name__)


@router.post("", response_model=PredictionSummary)
def create(request: CreatePredictionRequest, db: Session = Depends(get_db)):
    """Create a new prediction."""
    return create_prediction(request, db)


@router.get("", response_model=list[PredictionSummary])
def list_all(
    domain: str | None = None,
    resolved: bool | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List predictions with optional domain and resolution filters."""
    return list_predictions(db, domain=domain, resolved=resolved, limit=limit, offset=offset)


@router.get("/{prediction_id}", response_model=PredictionSummary)
def get(prediction_id: int, db: Session = Depends(get_db)):
    """Get a single prediction."""
    prediction = get_prediction(prediction_id, db)
    if not prediction:
        raise HTTPException(status_code=404, detail=f"Prediction {prediction_id} not found")
    return prediction


@router.patch("/{prediction_id}/resolve", response_model=PredictionSummary)
def resolve(
    prediction_id: int,
    request: ResolvePredictionRequest,
    db: Session = Depends(get_db),
):
    """Resolve a prediction with an outcome and compute Brier score."""
    try:
        return resolve_prediction(prediction_id, request.outcome, request.resolution_notes, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
