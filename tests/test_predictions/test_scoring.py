"""Tests for Brier score computation and calibration."""

import pytest

from backend.predictions.scoring import (
    compute_brier_score,
    compute_calibration_curve,
    compute_overall_brier,
    outcome_to_binary,
)


@pytest.mark.parametrize("outcome,expected", [
    ("correct", 1.0),
    ("incorrect", 0.0),
    ("partial", 0.5),
])
def test_outcome_to_binary(outcome, expected):
    assert outcome_to_binary(outcome) == expected


def test_outcome_to_binary_invalid():
    with pytest.raises(ValueError, match="Unknown outcome"):
        outcome_to_binary("maybe")


@pytest.mark.parametrize("forecast,outcome,expected", [
    (1.0, 1.0, 0.0),      # perfect correct
    (0.0, 0.0, 0.0),      # perfect incorrect
    (0.5, 0.5, 0.0),      # midpoint partial
    (0.9, 0.0, 0.81),     # confident and wrong
    (0.7, 1.0, 0.09),     # 70% confident, correct
])
def test_compute_brier_score(forecast, outcome, expected):
    result = compute_brier_score(forecast, outcome)
    assert abs(result - expected) < 1e-9


def test_compute_overall_brier_empty(db):
    result = compute_overall_brier(db)
    assert result["count"] == 0
    assert result["mean_brier"] is None


def test_compute_overall_brier_with_data(db):
    from datetime import datetime, timezone

    from backend.database.models import Prediction, PredictionOutcome

    pred = Prediction(
        topic="Test",
        prediction_text="Will X happen?",
        confidence_pct=70,
        domain="geopolitics",
        created_at=datetime.now(timezone.utc),
        outcome="correct",
        resolved_at=datetime.now(timezone.utc),
    )
    db.add(pred)
    db.flush()

    outcome = PredictionOutcome(
        prediction_id=pred.id,
        forecast=0.7,
        outcome_binary=1.0,
        brier_score=compute_brier_score(0.7, 1.0),
    )
    db.add(outcome)
    db.flush()

    result = compute_overall_brier(db)
    assert result["count"] == 1
    assert abs(result["mean_brier"] - 0.09) < 1e-4


def test_compute_calibration_curve_empty(db):
    result = compute_calibration_curve(db)
    assert result == []


def test_compute_calibration_curve_with_data(db):
    from datetime import datetime, timezone

    from backend.database.models import Prediction, PredictionOutcome

    pred = Prediction(
        topic="Calibration Test",
        prediction_text="Some prediction.",
        confidence_pct=80,
        created_at=datetime.now(timezone.utc),
        outcome="correct",
        resolved_at=datetime.now(timezone.utc),
    )
    db.add(pred)
    db.flush()

    outcome = PredictionOutcome(
        prediction_id=pred.id,
        forecast=0.8,
        outcome_binary=1.0,
        brier_score=compute_brier_score(0.8, 1.0),
    )
    db.add(outcome)
    db.flush()

    result = compute_calibration_curve(db, n_bins=10)
    assert len(result) >= 1
    bucket = result[0]
    assert "bin_center" in bucket
    assert "mean_forecast" in bucket
    assert "actual_frequency" in bucket
    assert "count" in bucket
