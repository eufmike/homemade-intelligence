"""ChromaDB client with two collections: sources and reports."""

import logging
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb import Collection

from backend.config import settings

logger = logging.getLogger(__name__)

SOURCES_COLLECTION = "sources"
REPORTS_COLLECTION = "reports"


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.ClientAPI:
    """Return a persistent ChromaDB client (singleton)."""
    persist_dir = Path(settings.chroma_persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist_dir))
    logger.info("ChromaDB client initialized at %s", persist_dir)
    return client


def get_sources_collection() -> Collection:
    """Return the sources collection, creating if it doesn't exist."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=SOURCES_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def get_reports_collection() -> Collection:
    """Return the reports collection, creating if it doesn't exist."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=REPORTS_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_source_chunk(
    doc_id: str,
    text: str,
    metadata: dict,
) -> None:
    """Upsert a single content chunk into the sources collection."""
    col = get_sources_collection()
    col.upsert(ids=[doc_id], documents=[text], metadatas=[metadata])


def upsert_report_summary(
    doc_id: str,
    text: str,
    metadata: dict,
) -> None:
    """Upsert a report summary into the reports collection."""
    col = get_reports_collection()
    col.upsert(ids=[doc_id], documents=[text], metadatas=[metadata])


def query_sources(query_text: str, n_results: int = 15) -> list[dict]:
    """Semantic search over the sources collection.

    Returns:
        List of dicts with keys: id, document, metadata, distance.
    """
    col = get_sources_collection()
    count = col.count()
    if count == 0:
        return []
    n_results = min(n_results, count)
    results = col.query(query_texts=[query_text], n_results=n_results)
    return _flatten_results(results)


def query_reports(query_text: str, n_results: int = 3) -> list[dict]:
    """Semantic search over the reports collection.

    Returns:
        List of dicts with keys: id, document, metadata, distance.
    """
    col = get_reports_collection()
    count = col.count()
    if count == 0:
        return []
    n_results = min(n_results, count)
    results = col.query(query_texts=[query_text], n_results=n_results)
    return _flatten_results(results)


def _flatten_results(results: dict) -> list[dict]:
    """Flatten ChromaDB query result structure into a list of dicts."""
    ids = results.get("ids", [[]])[0]
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]
    return [
        {"id": i, "document": d, "metadata": m, "distance": dist}
        for i, d, m, dist in zip(ids, docs, metas, dists)
    ]
