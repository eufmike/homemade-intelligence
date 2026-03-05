"""SQLite engine and session factory."""

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.config import settings


def _get_engine():
    db_url = settings.database_url
    # Ensure data directory exists for SQLite
    if db_url.startswith("sqlite:///"):
        db_path = Path(db_url.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})

    # Enable WAL mode and foreign keys for SQLite
    if "sqlite" in db_url:

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = _get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency: yields a database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables() -> None:
    """Create all ORM-defined tables (idempotent)."""
    from backend.database import models  # noqa: F401  # registers models

    Base.metadata.create_all(bind=engine)
