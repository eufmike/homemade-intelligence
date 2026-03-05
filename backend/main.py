"""FastAPI application entrypoint."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database.connection import create_all_tables
from backend.routers import ingestion, metrics, predictions, reports

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    # Startup
    logger.info("Starting Homemade Intelligence API")
    create_all_tables()

    # Sync source definitions from YAML
    try:
        from backend.database.connection import SessionLocal
        from backend.sources.registry import sync_sources_to_db

        with SessionLocal() as db:
            count = sync_sources_to_db(db)
            logger.info("Synced %d sources from YAML", count)
    except Exception as exc:
        logger.warning("Source sync failed (non-fatal): %s", exc)

    # Start background scheduler
    try:
        from backend.ingestion.scheduler import start_scheduler

        start_scheduler()
    except Exception as exc:
        logger.warning("Scheduler start failed (non-fatal): %s", exc)

    yield

    # Shutdown
    try:
        from backend.ingestion.scheduler import stop_scheduler

        stop_scheduler()
    except Exception:
        pass
    logger.info("Homemade Intelligence API shut down")


app = FastAPI(
    title="Homemade Intelligence API",
    description="Personal bias-aware geopolitical intelligence platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router)
app.include_router(predictions.router)
app.include_router(ingestion.router)
app.include_router(metrics.router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}
