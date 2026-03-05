"""Tests for agent pipeline stages with mocked Anthropic client."""

import pytest

from backend.agent.stage_triangulate import triangulate_sources


def _make_chunk(source_name: str, bias_label: str, language: str = "en", layer: int = 2) -> dict:
    return {
        "id": f"doc_{source_name}",
        "document": f"Sample content from {source_name}.",
        "metadata": {
            "source_name": source_name,
            "bias_label": bias_label,
            "language": language,
            "layer": layer,
            "url": f"https://example.com/{source_name}",
            "ingested_content_id": 1,
        },
        "distance": 0.1,
    }


class TestTriangulate:
    def test_empty_chunks_returns_zero_divergence(self):
        bias_coverage, caveat, score = triangulate_sources([])
        assert score == 0.0
        assert "non-Anglophone" in caveat or caveat == "" or "Anglophone" in caveat

    def test_single_source_low_divergence(self):
        chunks = [_make_chunk("Reuters", "center")]
        bias_coverage, caveat, score = triangulate_sources(chunks)
        assert score < 0.4

    def test_left_right_sources_higher_divergence(self):
        chunks = [
            _make_chunk("Guardian", "left"),
            _make_chunk("Fox News", "right"),
        ]
        bias_coverage, caveat, score = triangulate_sources(chunks)
        assert score >= 0.4

    def test_non_anglophone_bonus(self):
        chunks = [
            _make_chunk("Guardian", "left", language="en"),
            _make_chunk("Global Times", "state-affiliated", language="zh"),
        ]
        _, _, score = triangulate_sources(chunks)
        assert score > 0.0

    def test_missing_non_anglophone_triggers_caveat(self):
        chunks = [
            _make_chunk("Reuters", "center", language="en"),
            _make_chunk("Guardian", "left", language="en"),
        ]
        _, caveat, _ = triangulate_sources(chunks)
        assert "non-Anglophone" in caveat or "Anglophone" in caveat

    def test_bias_coverage_groups_correctly(self):
        chunks = [
            _make_chunk("Reuters", "center"),
            _make_chunk("AP", "center"),
            _make_chunk("Guardian", "left"),
        ]
        bias_coverage, _, _ = triangulate_sources(chunks)
        assert "center" in bias_coverage
        assert len(bias_coverage["center"]) == 2
        assert "left" in bias_coverage

    def test_full_diversity_near_max_score(self):
        chunks = [
            _make_chunk("Guardian", "left", language="en", layer=2),
            _make_chunk("Breitbart", "right", language="en", layer=2),
            _make_chunk("TASS", "state-affiliated", language="ru", layer=5),
            _make_chunk("RFA", "independent", language="en", layer=5),
            _make_chunk("EIA", "center", language="en", layer=4),
        ]
        _, _, score = triangulate_sources(chunks)
        assert score >= 0.5


class TestStageIngest:
    def test_check_reuse_guard_no_past_reports(self):
        from backend.agent.stage_ingest import check_reuse_guard

        should_warn, similarity = check_reuse_guard("Some new topic")
        assert should_warn is False
        assert similarity == 0.0
