"""Stage 4 — Audience formatting: TC general + TC elder (concurrent calls)."""

import asyncio
import logging

import anthropic

from backend.agent.prompts import build_zh_tw_elder_format_messages, build_zh_tw_format_messages
from backend.agent.token_tracker import RunTokenTracker
from backend.config import settings

logger = logging.getLogger(__name__)


def get_anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def _format_single(
    system: str,
    messages: list[dict],
    stage_name: str,
    tracker: RunTokenTracker,
) -> str:
    """Run a single formatting call (blocking in executor to avoid blocking event loop).

    Args:
        system: System prompt string.
        messages: Message list.
        stage_name: Stage identifier for tracker.
        tracker: Token usage tracker.

    Returns:
        Formatted markdown string.
    """
    client = get_anthropic_client()

    def _call() -> str:
        response = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=3000,
            system=system,
            messages=messages,
        )
        tracker.record_usage(stage_name, response.usage)
        return response.content[0].text

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _call)


async def format_all_audiences(
    base_analysis: str,
    topic: str,
    tracker: RunTokenTracker,
) -> tuple[str, str]:
    """Concurrently format for TC general and TC elder audiences.

    Args:
        base_analysis: English analysis from Stage 3.
        topic: Original topic string.
        tracker: Token usage tracker.

    Returns:
        Tuple of (content_zh_tw, content_zh_tw_elder).
    """
    zh_tw_system, zh_tw_messages = build_zh_tw_format_messages(base_analysis, topic)
    elder_system, elder_messages = build_zh_tw_elder_format_messages(base_analysis, topic)

    logger.info("Stage 4: launching concurrent TC format calls")

    zh_tw_content, elder_content = await asyncio.gather(
        _format_single(zh_tw_system, zh_tw_messages, "format_zh_tw", tracker),
        _format_single(elder_system, elder_messages, "format_zh_tw_elder", tracker),
    )

    logger.info("Stage 4 complete: zh_tw=%d chars, elder=%d chars", len(zh_tw_content), len(elder_content))
    return zh_tw_content, elder_content
