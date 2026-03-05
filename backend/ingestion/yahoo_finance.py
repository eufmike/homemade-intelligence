"""Yahoo Finance data ingestion via yfinance."""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.database.models import IngestedContent, Source
from backend.ingestion.dedup import compute_content_hash, is_duplicate
from backend.vector_store.chroma import upsert_source_chunk

logger = logging.getLogger(__name__)

YFINANCE_SOURCE_NAME = "Yahoo Finance"

MARKET_TICKERS = {
    "^VIX": "VIX Volatility Index",
    "^GSPC": "S&P 500",
    "GC=F": "Gold Futures",
    "CL=F": "Crude Oil (WTI) Futures",
    "^TNX": "10-Year Treasury Yield",
    "DX-Y.NYB": "US Dollar Index (DXY)",
}


def _ensure_yfinance_source(db: Session) -> Source:
    source = db.query(Source).filter(Source.name == YFINANCE_SOURCE_NAME).first()
    if not source:
        source = Source(
            name=YFINANCE_SOURCE_NAME,
            source_type="api",
            layer=7,
            bias_label="center",
            language="en",
            is_active=True,
        )
        db.add(source)
        db.commit()
        db.refresh(source)
    return source


def ingest_market_snapshot(db: Session) -> int:
    """Fetch current market data for key tickers and store as content.

    Args:
        db: SQLAlchemy session.

    Returns:
        Number of new data points ingested.
    """
    try:
        import yfinance as yf
    except ImportError:
        logger.warning("yfinance not installed; skipping market snapshot")
        return 0

    source = _ensure_yfinance_source(db)
    new_count = 0
    now = datetime.now(timezone.utc)

    for ticker_sym, ticker_name in MARKET_TICKERS.items():
        try:
            ticker = yf.Ticker(ticker_sym)
            info = ticker.fast_info
            price = getattr(info, "last_price", None) or getattr(info, "regularMarketPrice", None)
            if price is None:
                continue

            title = f"{ticker_name} ({ticker_sym}): {price:.2f}"
            body = f"Market data snapshot at {now.isoformat()}. {ticker_name} ({ticker_sym}) = {price:.4f}."

            content_hash = compute_content_hash(title, body[:500])
            if is_duplicate(content_hash, db):
                continue

            doc_id = f"yfinance_{content_hash}"
            content = IngestedContent(
                source_id=source.id,
                content_hash=content_hash,
                url=f"https://finance.yahoo.com/quote/{ticker_sym}",
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
                    "source_name": YFINANCE_SOURCE_NAME,
                    "bias_label": "center",
                    "language": "en",
                    "layer": 7,
                    "url": content.url,
                    "ingested_content_id": content.id,
                    "ticker": ticker_sym,
                },
            )
            new_count += 1

        except Exception as exc:
            logger.warning("Failed to fetch %s: %s", ticker_sym, exc)

    db.commit()
    logger.info("Yahoo Finance: ingested %d market data points", new_count)
    return new_count
