# SQLite + ChromaDB for Structured and Vector Storage

## Context and Problem Statement

The platform needs two types of storage: (1) structured relational data — reports, predictions, sources, Brier scores — and (2) semantic vector search to retrieve the most relevant source chunks for a given topic without dumping the full ingested corpus into every LLM call. This is a single-user tool running locally on a MacBook. There is no requirement for multi-user access or cloud deployment.

## Decision Drivers

* Zero-infrastructure constraint — no server processes to manage
* Semantic retrieval must reduce LLM input tokens significantly vs. full-corpus injection
* Embeddings must run locally at zero marginal cost
* Data must remain on-device

## Considered Options

* SQLite + ChromaDB (local persistent)
* PostgreSQL + pgvector
* Hosted vector DB (Pinecone, Weaviate Cloud)
* Plain JSON files

## Decision Outcome

Chosen option: **SQLite + ChromaDB**, because they both run in-process with no server daemon, meet all decision drivers, and are trivially replaceable if requirements change.

SQLite is accessed via SQLAlchemy ORM (`sqlite:///./data/homemade_intelligence.db`) with WAL mode enabled. ChromaDB runs as a `PersistentClient` at `./data/chroma/` with two collections: `sources` (ingested article chunks, top-15 retrieved per query) and `reports` (summaries for continuity and the reuse guard).

### Consequences

* Good, because zero infrastructure — no Postgres, Redis, or Docker required.
* Good, because WAL mode enables concurrent reads during background RSS ingestion without blocking.
* Good, because ChromaDB's `all-MiniLM-L6-v2` embedding model runs entirely locally (zero API cost per query).
* Good, because cosine similarity retrieval reduces LLM context by ~40,000–80,000 tokens per call vs. full-corpus injection.
* Bad, because SQLite has write serialization — only one writer at a time. Acceptable for single-user, but a blocker for concurrent multi-user.
* Bad, because ChromaDB's persistence format has broken across major versions — mitigated by pinning `>=1.0.0`.
* Neutral, because migration to PostgreSQL is a SQLAlchemy dialect swap if multi-user is ever needed.

## Pros and Cons of the Options

### SQLite + ChromaDB

* Good, because fully local, no cost, no network dependency.
* Good, because SQLAlchemy ORM means dialect swap is one line.
* Bad, because single-writer SQLite limits write throughput.

### PostgreSQL + pgvector

* Good, because handles concurrent writes and large datasets.
* Bad, because requires running a server process — violates zero-infrastructure constraint.
* Bad, because pgvector embedding quality is lower than ChromaDB's dedicated embedding models.

### Hosted vector DB (Pinecone, Weaviate Cloud)

* Good, because managed scalability.
* Bad, because data leaves the device — unacceptable for personal intelligence tool.
* Bad, because monthly cost.

### Plain JSON files

* Bad, because no query capability, no deduplication index, no vector search.

## More Information

* `backend/database/connection.py`
* `backend/vector_store/chroma.py`
* `backend/database/migrations/001_initial_schema.sql`
