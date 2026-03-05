"""Source registry: load source definitions from rss_feeds.yaml and sync to DB."""

import logging
from pathlib import Path

import yaml
from sqlalchemy.orm import Session

from backend.database.models import Source

logger = logging.getLogger(__name__)

FEEDS_YAML = Path(__file__).parent.parent.parent / "sources" / "rss_feeds.yaml"


def load_feeds_yaml() -> list[dict]:
    """Load and return the list of feed definitions from rss_feeds.yaml."""
    if not FEEDS_YAML.exists():
        logger.warning("rss_feeds.yaml not found at %s", FEEDS_YAML)
        return []
    with FEEDS_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("feeds", [])


def sync_sources_to_db(db: Session) -> int:
    """Sync feed definitions from YAML into the sources table (upsert by feed_url).

    Args:
        db: SQLAlchemy session.

    Returns:
        Number of sources created or updated.
    """
    feeds = load_feeds_yaml()
    count = 0
    for feed in feeds:
        feed_url = feed.get("url", "")
        existing = db.query(Source).filter(Source.feed_url == feed_url).first()
        if existing:
            existing.name = feed.get("name", existing.name)
            existing.layer = feed.get("layer", existing.layer)
            existing.bias_label = feed.get("bias_label", existing.bias_label)
            existing.language = feed.get("language", existing.language)
            existing.is_active = feed.get("is_active", True)
        else:
            source = Source(
                name=feed.get("name", "Unknown"),
                feed_url=feed_url,
                source_type=feed.get("type", "rss"),
                layer=feed.get("layer", 1),
                bias_label=feed.get("bias_label", "center"),
                language=feed.get("language", "en"),
                is_active=feed.get("is_active", True),
            )
            db.add(source)
        count += 1

    db.commit()
    logger.info("Synced %d sources from rss_feeds.yaml", count)
    return count
