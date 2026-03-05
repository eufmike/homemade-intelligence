"""Pydantic schemas for prediction endpoints."""

from datetime import date, datetime

from pydantic import BaseModel, Field


class CreatePredictionRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200)
    prediction_text: str = Field(..., min_length=10)
    confidence_pct: int = Field(..., ge=1, le=99, description="Confidence 1-99%")
    domain: str = Field("other", description="geopolitics / markets / taiwan / energy / other")
    deadline_date: date | None = None
    report_id: int | None = None
    metaculus_question_id: str | None = None
    polymarket_market_id: str | None = None
    metaculus_community_pct: float | None = Field(None, ge=0, le=100)
    polymarket_odds_pct: float | None = Field(None, ge=0, le=100)


class ResolvePredictionRequest(BaseModel):
    outcome: str = Field(..., description="correct / incorrect / partial")
    resolution_notes: str = Field("", description="Optional resolution context")


class PredictionSummary(BaseModel):
    id: int
    topic: str
    prediction_text: str
    confidence_pct: int | None
    domain: str | None
    deadline_date: date | None
    created_at: datetime | None
    resolved_at: datetime | None
    outcome: str | None
    metaculus_community_pct: float | None
    polymarket_odds_pct: float | None

    model_config = {"from_attributes": True}


class PredictionOutcomeResponse(BaseModel):
    id: int
    prediction_id: int
    scored_at: datetime | None
    forecast: float
    outcome_binary: float
    brier_score: float

    model_config = {"from_attributes": True}
