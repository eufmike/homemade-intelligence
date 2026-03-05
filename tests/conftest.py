"""Shared pytest fixtures: in-memory SQLite + mock Chroma."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.connection import Base


@pytest.fixture(scope="session")
def engine():
    """In-memory SQLite engine for testing."""
    _engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=_engine)
    yield _engine
    _engine.dispose()


@pytest.fixture
def db(engine):
    """Per-test database session that rolls back after each test."""
    from backend.database import models  # noqa: F401 — ensures models are registered

    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def mock_chroma(monkeypatch):
    """Replace all ChromaDB calls with no-ops during tests."""
    monkeypatch.setattr("backend.vector_store.chroma.upsert_source_chunk", lambda **kw: None)
    monkeypatch.setattr("backend.vector_store.chroma.upsert_report_summary", lambda **kw: None)
    monkeypatch.setattr("backend.vector_store.chroma.query_sources", lambda *a, **kw: [])
    monkeypatch.setattr("backend.vector_store.chroma.query_reports", lambda *a, **kw: [])
