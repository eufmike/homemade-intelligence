"""Stage 2 — Bias coverage check and narrative divergence scoring."""

import logging

logger = logging.getLogger(__name__)

# Minimum requirements for unbiased analysis
MIN_NON_ANGLOPHONE_SOURCES = 1
ANGLOPHONE_LANGUAGES = {"en"}
REQUIRED_BIAS_POLES = 2  # At least 2 distinct bias labels


def triangulate_sources(source_chunks: list[dict]) -> tuple[dict, str, float]:
    """Categorize sources by bias and enforce minimum coverage requirements.

    Args:
        source_chunks: List of ChromaDB result dicts (each with metadata).

    Returns:
        Tuple of:
        - bias_coverage: dict mapping bias_label -> list of source names
        - coverage_caveat: warning string if requirements not met (empty if OK)
        - divergence_score: float 0.0-1.0 measuring narrative divergence
    """
    bias_coverage: dict[str, list[str]] = {}
    non_anglophone_count = 0
    seen_sources: set[str] = set()

    for chunk in source_chunks:
        meta = chunk.get("metadata", {})
        source_name = meta.get("source_name", "Unknown")
        bias_label = meta.get("bias_label", "unknown")
        language = meta.get("language", "en")

        if source_name not in seen_sources:
            seen_sources.add(source_name)
            if language not in ANGLOPHONE_LANGUAGES:
                non_anglophone_count += 1
            if bias_label not in bias_coverage:
                bias_coverage[bias_label] = []
            if source_name not in bias_coverage[bias_label]:
                bias_coverage[bias_label].append(source_name)

    # Build coverage caveat
    caveats = []
    if non_anglophone_count < MIN_NON_ANGLOPHONE_SOURCES:
        caveats.append(
            f"Analysis lacks non-Anglophone sources (found {non_anglophone_count}, "
            f"minimum {MIN_NON_ANGLOPHONE_SOURCES}). Perspective may be Western-centric."
        )

    meaningful_poles = [
        label for label in bias_coverage
        if label not in ("unknown", "center") and bias_coverage[label]
    ]
    has_left = any(l in ("left",) for l in meaningful_poles)
    has_right = any(l in ("right",) for l in meaningful_poles)
    has_state = any(l in ("state-affiliated",) for l in meaningful_poles)

    pole_count = sum([has_left, has_right, has_state])
    if pole_count < REQUIRED_BIAS_POLES and len(bias_coverage) < REQUIRED_BIAS_POLES:
        caveats.append(
            "Insufficient bias diversity — only one ideological pole represented. "
            "Divergence score may be artificially low."
        )

    coverage_caveat = " | ".join(caveats)

    # Compute narrative divergence score
    divergence_score = _compute_divergence_score(bias_coverage, source_chunks)

    logger.info(
        "Stage 2 triangulation: %d unique sources, %d bias poles, divergence=%.2f",
        len(seen_sources),
        len(bias_coverage),
        divergence_score,
    )

    return bias_coverage, coverage_caveat, divergence_score


def _compute_divergence_score(bias_coverage: dict, source_chunks: list[dict]) -> float:
    """Estimate narrative divergence score based on bias pole diversity.

    Score heuristic:
    - 0 bias poles or 1 source: 0.0
    - 2 poles (e.g., left + right): 0.4 base
    - 3+ poles (e.g., left + right + state-affiliated): 0.6 base
    - Bonus for non-Western sources: +0.1
    - Bonus for state-affiliated vs independent: +0.15
    - Cap at 1.0

    This is a structural proxy; true divergence requires semantic analysis by the LLM.

    Args:
        bias_coverage: Bias label -> list of source names.
        source_chunks: Raw source chunks for additional signals.

    Returns:
        Float divergence score 0.0-1.0.
    """
    if not bias_coverage or sum(len(v) for v in bias_coverage.values()) <= 1:
        return 0.0

    pole_labels = set(bias_coverage.keys())
    score = 0.0

    has_left = "left" in pole_labels
    has_right = "right" in pole_labels
    has_state = "state-affiliated" in pole_labels
    has_independent = "independent" in pole_labels

    if has_left and has_right:
        score += 0.4
    elif len(pole_labels) >= 2:
        score += 0.2

    if has_state:
        score += 0.15
    if has_independent and has_state:
        score += 0.1

    # Non-Anglophone bonus
    non_anglophone = sum(
        1 for c in source_chunks
        if c.get("metadata", {}).get("language", "en") not in ANGLOPHONE_LANGUAGES
    )
    if non_anglophone >= 1:
        score += 0.1
    if non_anglophone >= 3:
        score += 0.1

    # Multiple sources across more than 2 layers
    layers = {c.get("metadata", {}).get("layer", 0) for c in source_chunks}
    if len(layers) >= 3:
        score += 0.1

    return min(score, 1.0)
