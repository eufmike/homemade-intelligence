"""Manual text and URL injection into the ingestion pipeline."""

import logging
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from backend.database.models import IngestedContent
from backend.ingestion.dedup import compute_content_hash, is_duplicate
from backend.vector_store.chroma import upsert_source_chunk

logger = logging.getLogger(__name__)


def inject_text(
    title: str,
    body: str,
    url: str = "",
    source_id: int | None = None,
    db: Session = None,
) -> IngestedContent | None:
    """Inject raw article text into the pipeline.

    Args:
        title: Article title.
        body: Article body text.
        url: Optional source URL.
        source_id: Optional source FK.
        db: SQLAlchemy session.

    Returns:
        IngestedContent ORM object if new, None if duplicate.
    """
    content_hash = compute_content_hash(title, body)
    if is_duplicate(content_hash, db):
        logger.info("Manual inject: duplicate skipped (hash=%s)", content_hash[:12])
        return None

    doc_id = f"manual_{content_hash}"
    content = IngestedContent(
        source_id=source_id,
        content_hash=content_hash,
        url=url,
        title=title,
        body=body,
        published_at=datetime.now(timezone.utc),
        is_manual=True,
        chroma_doc_id=doc_id,
    )
    db.add(content)
    db.flush()

    chunk_text = f"{title}\n\n{body}"[:2000]
    upsert_source_chunk(
        doc_id=doc_id,
        text=chunk_text,
        metadata={
            "source_id": source_id or 0,
            "source_name": "Manual Inject",
            "bias_label": "unknown",
            "language": "en",
            "layer": 0,
            "url": url,
            "ingested_content_id": content.id,
        },
    )

    db.commit()
    logger.info("Manual inject: stored '%s' (id=%d)", title[:60], content.id)
    return content


def inject_url(url: str, source_id: int | None = None, db: Session = None) -> IngestedContent | None:
    """Fetch a URL, extract text with trafilatura, and inject.

    Args:
        url: Web page URL to fetch and extract.
        source_id: Optional source FK.
        db: SQLAlchemy session.

    Returns:
        IngestedContent ORM object if new, None if duplicate or fetch failed.
    """
    try:
        import trafilatura

        response = httpx.get(url, timeout=20.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        extracted = trafilatura.extract(response.text, include_comments=False, include_tables=False)
        if not extracted:
            logger.warning("URL inject: trafilatura returned no content for %s", url)
            return None

        # Use first line as title if no better source
        lines = extracted.strip().splitlines()
        title = lines[0][:200] if lines else url
        body = extracted

    except Exception as exc:
        logger.warning("URL inject failed for %s: %s", url, exc)
        return None

    return inject_text(title=title, body=body, url=url, source_id=source_id, db=db)
