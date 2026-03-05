"""FRED (Federal Reserve Economic Data) ingestion via fredapi."""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.config import settings
from backend.database.models import IngestedContent, Source
from backend.ingestion.dedup import compute_content_hash, is_duplicate
from backend.vector_store.chroma import upsert_source_chunk

logger = logging.getLogger(__name__)

FRED_SOURCE_NAME = "FRED (Federal Reserve)"

FRED_SERIES = {
    "CPIAUCSL": "US CPI (All Urban Consumers, SA)",
    "UNRATE": "US Unemployment Rate",
    "FEDFUNDS": "Federal Funds Rate",
    "T10Y2Y": "10-Year minus 2-Year Treasury Spread (Yield Curve)",
    "DCOILWTICO": "WTI Crude Oil Price",
    "DEXUSEU": "USD/EUR Exchange Rate",
}


def _ensure_fred_source(db: Session) -> Source:
    source = db.query(Source).filter(Source.name == FRED_SOURCE_NAME).first()
    if not source:
        source = Source(
            name=FRED_SOURCE_NAME,
            source_type="api",
            layer=3,
            bias_label="center",
            language="en",
            is_active=True,
        )
        db.add(source)
        db.commit()
        db.refresh(source)
    return source


def ingest_fred_indicators(db: Session) -> int:
    """Fetch latest FRED series values and store as content.

    Args:
        db: SQLAlchemy session.

    Returns:
        Number of new indicators ingested.
    """
    if not settings.fred_api_key:
        logger.info("FRED_API_KEY not set; skipping FRED ingestion")
        return 0

    try:
        from fredapi import Fred
    except ImportError:
        logger.warning("fredapi not installed; skipping FRED ingestion")
        return 0

    fred = Fred(api_key=settings.fred_api_key)
    source = _ensure_fred_source(db)
    new_count = 0
    now = datetime.now(timezone.utc)

    for series_id, description in FRED_SERIES.items():
        try:
            series = fred.get_series(series_id, observation_start="2025-01-01")
            if series.empty:
                continue
            latest_val = series.iloc[-1]
            latest_date = series.index[-1].strftime("%Y-%m-%d")

            title = f"FRED {series_id}: {description} = {latest_val:.4f} ({latest_date})"
            body = (
                f"FRED economic indicator '{description}' (series ID: {series_id}). "
                f"Latest value: {latest_val:.4f} as of {latest_date}. "
                f"Retrieved: {now.isoformat()}."
            )

            content_hash = compute_content_hash(title, body[:500])
            if is_duplicate(content_hash, db):
                continue

            doc_id = f"fred_{content_hash}"
            content = IngestedContent(
                source_id=source.id,
                content_hash=content_hash,
                url=f"https://fred.stlouisfed.org/series/{series_id}",
                title=title,
                body=body,
                published_at=now,
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
                    "source_name": FRED_SOURCE_NAME,
                    "bias_label": "center",
                    "language": "en",
                    "layer": 3,
                    "url": content.url,
                    "ingested_content_id": content.id,
                    "series_id": series_id,
                },
            )
            new_count += 1

        except Exception as exc:
            logger.warning("FRED series %s failed: %s", series_id, exc)

    db.commit()
    logger.info("FRED: ingested %d new indicator values", new_count)
    return new_count
