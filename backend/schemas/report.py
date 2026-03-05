"""Pydantic schemas for report endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class GenerateReportRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Analysis topic")
    domain: str = Field("general", description="geopolitics / markets / taiwan / energy / general")
    manual_text: str = Field("", description="Optional article text to inject before analysis")
    manual_title: str = Field("", description="Title for manually injected text")


class ReportSummary(BaseModel):
    id: int
    topic: str
    domain: str | None
    status: str
    bias_score: float | None
    confidence_overall: str | None
    tokens_used: int | None
    tokens_cached: int | None
    cost_usd: float | None
    created_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class ReportDetail(ReportSummary):
    content_en: str | None
    content_zh_tw: str | None
    content_zh_tw_elder: str | None
    source_ids_json: str | None
