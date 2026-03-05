"""Stage 3 — Base English analysis via Claude with streaming and prompt caching."""

import logging
from collections.abc import AsyncGenerator

import anthropic

from backend.agent.prompts import build_analysis_messages, build_system_blocks
from backend.agent.token_tracker import RunTokenTracker
from backend.config import settings

logger = logging.getLogger(__name__)


def get_anthropic_client() -> anthropic.Anthropic:
    """Return a configured Anthropic client."""
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def analyze_stream(
    topic: str,
    source_chunks: list[dict],
    past_reports: list[dict],
    bias_coverage: dict,
    coverage_caveat: str,
    tracker: RunTokenTracker,
) -> AsyncGenerator[str, None]:
    """Stream Stage 3 analysis tokens via SSE.

    Yields text delta strings. Call this from an SSE endpoint and forward each
    yielded string to the client.

    Args:
        topic: Analysis topic.
        source_chunks: Retrieved source content chunks.
        past_reports: Related past reports from ChromaDB.
        bias_coverage: Bias label -> source names mapping.
        coverage_caveat: Coverage warning string (empty if OK).
        tracker: Token usage tracker instance.

    Yields:
        Text delta strings from the streaming response.
    """
    client = get_anthropic_client()
    messages = build_analysis_messages(topic, source_chunks, past_reports, bias_coverage, coverage_caveat)
    system_blocks = build_system_blocks()

    full_text = []
    usage_obj = None

    with client.messages.stream(
        model=settings.anthropic_model,
        max_tokens=4096,
        system=system_blocks,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            full_text.append(text)
            yield text

        # Capture final usage after stream completes
        final_message = stream.get_final_message()
        usage_obj = final_message.usage

    if usage_obj:
        tracker.record_usage("analyze", usage_obj)

    logger.info("Stage 3 complete: %.0f chars generated", sum(len(t) for t in full_text))


async def analyze_blocking(
    topic: str,
    source_chunks: list[dict],
    past_reports: list[dict],
    bias_coverage: dict,
    coverage_caveat: str,
    tracker: RunTokenTracker,
) -> str:
    """Run Stage 3 analysis without streaming (collects full response).

    Args:
        topic: Analysis topic.
        source_chunks: Retrieved source content chunks.
        past_reports: Related past reports from ChromaDB.
        bias_coverage: Bias label -> source names mapping.
        coverage_caveat: Coverage warning string (empty if OK).
        tracker: Token usage tracker instance.

    Returns:
        Full English analysis markdown string.
    """
    chunks = []
    async for text in analyze_stream(topic, source_chunks, past_reports, bias_coverage, coverage_caveat, tracker):
        chunks.append(text)
    return "".join(chunks)
