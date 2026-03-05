-- =============================================================================
-- Migration 001: Initial schema
-- Applied automatically by create_all_tables() via SQLAlchemy ORM.
-- This file is kept as a human-readable reference of the full schema.
-- =============================================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    feed_url    TEXT,
    source_type TEXT,                    -- rss / gdelt / manual / api
    layer       INTEGER,                 -- intelligence stack layer 1-10
    bias_label  TEXT,                    -- center / left / right / state-affiliated / independent
    language    TEXT,                    -- ISO 639-1
    is_active   BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS ingested_content (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id    INTEGER REFERENCES sources(id),
    content_hash TEXT    UNIQUE NOT NULL,   -- SHA-256 of normalized title+body[:500]
    url          TEXT,
    title        TEXT,
    body         TEXT,
    published_at TIMESTAMP,
    ingested_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_manual    BOOLEAN   DEFAULT 0,
    chroma_doc_id TEXT                      -- ID in ChromaDB sources collection
);

CREATE TABLE IF NOT EXISTS reports (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    topic               TEXT    NOT NULL,
    domain              TEXT,              -- geopolitics / markets / taiwan / energy / general
    status              TEXT    DEFAULT 'pending',  -- pending / generating / complete / failed
    bias_score          REAL,              -- 0.0-1.0 narrative divergence
    confidence_overall  TEXT,              -- high / medium / low
    content_en          TEXT,
    content_zh_tw       TEXT,
    content_zh_tw_elder TEXT,
    source_ids_json     TEXT,              -- JSON array of ingested_content IDs used
    tokens_used         INTEGER DEFAULT 0,
    tokens_cached       INTEGER DEFAULT 0,
    cost_usd            REAL    DEFAULT 0.0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at        TIMESTAMP,
    chroma_doc_id       TEXT               -- ID in ChromaDB reports collection
);

CREATE TABLE IF NOT EXISTS predictions (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    topic                   TEXT    NOT NULL,
    prediction_text         TEXT    NOT NULL,
    confidence_pct          INTEGER,       -- 1-99
    domain                  TEXT,          -- geopolitics / markets / taiwan / energy / other
    deadline_date           DATE,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at             TIMESTAMP,
    outcome                 TEXT,          -- NULL / correct / incorrect / partial
    resolution_notes        TEXT,
    report_id               INTEGER REFERENCES reports(id),
    metaculus_question_id   TEXT,
    polymarket_market_id    TEXT,
    metaculus_community_pct REAL,
    polymarket_odds_pct     REAL
);

CREATE TABLE IF NOT EXISTS prediction_outcomes (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id  INTEGER NOT NULL REFERENCES predictions(id),
    scored_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forecast       REAL    NOT NULL,   -- confidence_pct / 100
    outcome_binary REAL    NOT NULL,   -- 1.0=correct / 0.0=incorrect / 0.5=partial
    brier_score    REAL    NOT NULL    -- (forecast - outcome_binary)^2
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_ingested_content_source ON ingested_content(source_id);
CREATE INDEX IF NOT EXISTS idx_ingested_content_hash   ON ingested_content(content_hash);
CREATE INDEX IF NOT EXISTS idx_reports_status          ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_domain          ON reports(domain);
CREATE INDEX IF NOT EXISTS idx_predictions_domain      ON predictions(domain);
CREATE INDEX IF NOT EXISTS idx_predictions_outcome     ON predictions(outcome);
CREATE INDEX IF NOT EXISTS idx_prediction_outcomes_pid ON prediction_outcomes(prediction_id);
