"""SHA-256 content deduplication for ingested articles."""

import hashlib


def compute_content_hash(title: str, body: str) -> str:
    """Compute SHA-256 hash over normalized title + first 500 chars of body.

    Args:
        title: Article title.
        body: Article body text.

    Returns:
        Hex digest string (64 chars).
    """
    normalized = f"{title.strip().lower()}|{body.strip()[:500].lower()}"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def is_duplicate(content_hash: str, db) -> bool:
    """Check if a content hash already exists in the database.

    Args:
        content_hash: SHA-256 hex digest.
        db: SQLAlchemy session.

    Returns:
        True if duplicate, False if new.
    """
    from backend.database.models import IngestedContent

    return db.query(IngestedContent).filter(IngestedContent.content_hash == content_hash).first() is not None
