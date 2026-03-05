"""Brier score computation and calibration analysis."""

import logging
from collections import defaultdict

from sqlalchemy.orm import Session

from backend.database.models import PredictionOutcome

logger = logging.getLogger(__name__)

OUTCOME_BINARY_MAP = {
    "correct": 1.0,
    "incorrect": 0.0,
    "partial": 0.5,
}


def outcome_to_binary(outcome: str) -> float:
    """Convert outcome string to binary float value.

    Args:
        outcome: One of 'correct', 'incorrect', 'partial'.

    Returns:
        1.0, 0.0, or 0.5.

    Raises:
        ValueError: If outcome is not recognized.
    """
    if outcome not in OUTCOME_BINARY_MAP:
        raise ValueError(f"Unknown outcome '{outcome}'. Must be one of {list(OUTCOME_BINARY_MAP)}")
    return OUTCOME_BINARY_MAP[outcome]


def compute_brier_score(forecast: float, outcome_binary: float) -> float:
    """Compute Brier score for a single prediction.

    Brier score = (forecast - outcome)^2. Range: 0.0 (perfect) to 1.0 (worst).

    Args:
        forecast: Probability forecast as decimal (0.0–1.0).
        outcome_binary: Actual outcome as 1.0, 0.0, or 0.5.

    Returns:
        Brier score float.
    """
    return (forecast - outcome_binary) ** 2


def compute_overall_brier(db: Session, domain: str | None = None) -> dict:
    """Compute overall Brier score statistics.

    Args:
        db: SQLAlchemy session.
        domain: Optional domain filter.

    Returns:
        Dict with keys: count, mean_brier, skill_score, domain.
    """
    from backend.database.models import Prediction

    q = db.query(PredictionOutcome).join(Prediction)
    if domain:
        q = q.filter(Prediction.domain == domain)

    outcomes = q.all()
    if not outcomes:
        return {"count": 0, "mean_brier": None, "skill_score": None, "domain": domain}

    scores = [o.brier_score for o in outcomes]
    mean_brier = sum(scores) / len(scores)

    # Brier skill score vs. climatological baseline (0.5 probability forecast)
    # Baseline Brier = (0.5 - mean_outcome)^2
    mean_outcome = sum(o.outcome_binary for o in outcomes) / len(outcomes)
    baseline_brier = (0.5 - mean_outcome) ** 2
    skill_score = 1.0 - (mean_brier / baseline_brier) if baseline_brier > 0 else None

    return {
        "count": len(scores),
        "mean_brier": round(mean_brier, 4),
        "skill_score": round(skill_score, 4) if skill_score is not None else None,
        "domain": domain,
    }


def compute_brier_by_domain(db: Session) -> list[dict]:
    """Compute Brier scores broken down by domain.

    Args:
        db: SQLAlchemy session.

    Returns:
        List of domain stat dicts.
    """
    from backend.database.models import Prediction

    rows = (
        db.query(PredictionOutcome, Prediction.domain)
        .join(Prediction)
        .all()
    )

    by_domain: dict[str, list[float]] = defaultdict(list)
    by_domain_outcomes: dict[str, list[float]] = defaultdict(list)

    for outcome_row, dom in rows:
        key = dom or "other"
        by_domain[key].append(outcome_row.brier_score)
        by_domain_outcomes[key].append(outcome_row.outcome_binary)

    results = []
    for dom, scores in by_domain.items():
        mean_brier = sum(scores) / len(scores)
        mean_outcome = sum(by_domain_outcomes[dom]) / len(by_domain_outcomes[dom])
        baseline_brier = (0.5 - mean_outcome) ** 2
        skill = 1.0 - (mean_brier / baseline_brier) if baseline_brier > 0 else None
        results.append({
            "domain": dom,
            "count": len(scores),
            "mean_brier": round(mean_brier, 4),
            "skill_score": round(skill, 4) if skill is not None else None,
        })

    return sorted(results, key=lambda x: x["mean_brier"])


def compute_calibration_curve(db: Session, n_bins: int = 10) -> list[dict]:
    """Compute calibration curve data (forecast bin vs. actual frequency).

    Args:
        db: SQLAlchemy session.
        n_bins: Number of probability bins.

    Returns:
        List of bin dicts: {bin_center, mean_forecast, actual_frequency, count}.
    """
    outcomes = db.query(PredictionOutcome).all()
    if not outcomes:
        return []

    bin_size = 1.0 / n_bins
    bins: dict[int, list] = defaultdict(list)

    for o in outcomes:
        bin_idx = min(int(o.forecast / bin_size), n_bins - 1)
        bins[bin_idx].append(o)

    result = []
    for i in range(n_bins):
        if i not in bins:
            continue
        bin_outcomes = bins[i]
        mean_forecast = sum(o.forecast for o in bin_outcomes) / len(bin_outcomes)
        actual_freq = sum(o.outcome_binary for o in bin_outcomes) / len(bin_outcomes)
        result.append({
            "bin_center": round((i + 0.5) * bin_size, 2),
            "mean_forecast": round(mean_forecast, 4),
            "actual_frequency": round(actual_freq, 4),
            "count": len(bin_outcomes),
        })

    return result
