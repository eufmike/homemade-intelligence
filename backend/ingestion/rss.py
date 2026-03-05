"""RSS/Atom feed poller using feedparser."""

import logging
from datetime import datetime, timezone

import feedparser
from sqlalchemy.orm import Session

from backend.database.models import IngestedContent, Source
from backend.ingestion.dedup import compute_content_hash, is_duplicate
from backend.vector_store.chroma import upsert_source_chunk

logger = logging.getLogger(__name__)


def _parse_published(entry: dict) -> datetime | None:
    """Extract published datetime from a feedparser entry."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return None


def _entry_body(entry: dict) -> str:
    """Extract best available body text from a feedparser entry."""
    if "summary" in entry:
        return entry.summary
    if "content" in entry and entry.content:
        return entry.content[0].get("value", "")
    return ""


def poll_source(source: Source, db: Session) -> int:
    """Poll a single RSS source and store new articles.

    Args:
        source: Source ORM object with feed_url.
        db: SQLAlchemy session.

    Returns:
        Number of new articles ingested.
    """
    if not source.feed_url:
        return 0

    try:
        feed = feedparser.parse(source.feed_url)
    except Exception as exc:
        logger.warning("Failed to parse feed %s: %s", source.feed_url, exc)
        return 0

    new_count = 0
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        body = _entry_body(entry)
        if not title and not body:
            continue

        content_hash = compute_content_hash(title, body)
        if is_duplicate(content_hash, db):
            continue

        url = entry.get("link", "")
        published_at = _parse_published(entry)

        chunk_text = f"{title}\n\n{body}"[:2000]
        doc_id = f"source_{content_hash}"

        content = IngestedContent(
            source_id=source.id,
            content_hash=content_hash,
            url=url,
            title=title,
            body=body,
            published_at=published_at,
            is_manual=False,
            chroma_doc_id=doc_id,
        )
        db.add(content)
        db.flush()

        upsert_source_chunk(
            doc_id=doc_id,
            text=chunk_text,
            metadata={
                "source_id": source.id,
                "source_name": source.name,
                "bias_label": source.bias_label or "unknown",
                "language": source.language or "en",
                "layer": source.layer or 0,
                "url": url,
                "ingested_content_id": content.id,
            },
        )
        new_count += 1

    db.commit()
    logger.info("Source '%s': ingested %d new articles", source.name, new_count)
    return new_count


def poll_all_active_sources(db: Session) -> dict[str, int]:
    """Poll all active RSS sources.

    Args:
        db: SQLAlchemy session.

    Returns:
        Dict mapping source name to new article count.
    """
    sources = db.query(Source).filter(Source.is_active == True, Source.source_type == "rss").all()  # noqa: E712
    return {s.name: poll_source(s, db) for s in sources}
