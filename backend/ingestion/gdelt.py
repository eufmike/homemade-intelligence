"""GDELT v2 keyword query ingestion."""

import logging
from datetime import datetime, timezone
from urllib.parse import quote_plus

import httpx
from sqlalchemy.orm import Session

from backend.database.models import IngestedContent, Source
from backend.ingestion.dedup import compute_content_hash, is_duplicate
from backend.vector_store.chroma import upsert_source_chunk

logger = logging.getLogger(__name__)

GDELT_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_SOURCE_NAME = "GDELT"


def _ensure_gdelt_source(db: Session) -> Source:
    """Get or create the synthetic GDELT source record."""
    source = db.query(Source).filter(Source.name == GDELT_SOURCE_NAME).first()
    if not source:
        source = Source(
            name=GDELT_SOURCE_NAME,
            source_type="gdelt",
            layer=2,
            bias_label="center",
            language="en",
            is_active=True,
        )
        db.add(source)
        db.commit()
        db.refresh(source)
    return source


def query_gdelt(keyword: str, max_records: int = 10, db: Session = None) -> int:
    """Query GDELT v2 API for recent articles matching a keyword.

    Args:
        keyword: Search keyword or phrase.
        max_records: Maximum articles to ingest.
        db: SQLAlchemy session.

    Returns:
        Number of new articles ingested.
    """
    if db is None:
        return 0

    params = {
        "query": keyword,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "timespan": "24h",
    }

    try:
        response = httpx.get(GDELT_API_URL, params=params, timeout=15.0)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        logger.warning("GDELT query failed for '%s': %s", keyword, exc)
        return 0

    articles = data.get("articles", [])
    if not articles:
        return 0

    source = _ensure_gdelt_source(db)
    new_count = 0

    for article in articles:
        title = article.get("title", "").strip()
        url = article.get("url", "")
        body = f"{title}. Source: {article.get('domain', '')}. Tone: {article.get('tone', 'N/A')}"

        content_hash = compute_content_hash(title, body)
        if is_duplicate(content_hash, db):
            continue

        doc_id = f"gdelt_{content_hash}"
        content = IngestedContent(
            source_id=source.id,
            content_hash=content_hash,
            url=url,
            title=title,
            body=body,
            published_at=datetime.now(timezone.utc),
            is_manual=False,
            chroma_doc_id=doc_id,
        )
        db.add(content)
        db.flush()

        upsert_source_chunk(
            doc_id=doc_id,
            text=f"{title}\n\n{body}",
            metadata={
                "source_id": source.id,
                "source_name": GDELT_SOURCE_NAME,
                "bias_label": "center",
                "language": "en",
                "layer": 2,
                "url": url,
                "ingested_content_id": content.id,
            },
        )
        new_count += 1

    db.commit()
    logger.info("GDELT '%s': ingested %d new articles", keyword, new_count)
    return new_count
