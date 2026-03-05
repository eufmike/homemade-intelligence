"""Tests for content deduplication."""

import pytest

from backend.ingestion.dedup import compute_content_hash, is_duplicate


def test_compute_content_hash_is_deterministic():
    h1 = compute_content_hash("Iran Closes Hormuz", "Oil prices surge as...")
    h2 = compute_content_hash("Iran Closes Hormuz", "Oil prices surge as...")
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex digest


def test_compute_content_hash_different_inputs_differ():
    h1 = compute_content_hash("Title A", "Body A")
    h2 = compute_content_hash("Title B", "Body B")
    assert h1 != h2


def test_compute_content_hash_normalizes_case():
    h1 = compute_content_hash("TITLE", "BODY")
    h2 = compute_content_hash("title", "body")
    assert h1 == h2


def test_compute_content_hash_truncates_body_at_500():
    long_body = "x" * 1000
    short_body = "x" * 500
    h1 = compute_content_hash("title", long_body)
    h2 = compute_content_hash("title", short_body)
    assert h1 == h2


def test_is_duplicate_returns_false_for_new_content(db):
    assert is_duplicate("aabbccddeeff" * 5, db) is False


def test_is_duplicate_returns_true_after_insert(db):
    from datetime import datetime, timezone

    from backend.database.models import IngestedContent

    content_hash = compute_content_hash("Test Article", "Test body content here.")
    content = IngestedContent(
        content_hash=content_hash,
        title="Test Article",
        body="Test body content here.",
        ingested_at=datetime.now(timezone.utc),
        is_manual=True,
    )
    db.add(content)
    db.flush()

    assert is_duplicate(content_hash, db) is True


@pytest.mark.parametrize("title,body", [
    ("", "some body"),
    ("some title", ""),
    ("  leading spaces  ", "  body  "),
])
def test_compute_content_hash_handles_edge_cases(title, body):
    result = compute_content_hash(title, body)
    assert isinstance(result, str)
    assert len(result) == 64
