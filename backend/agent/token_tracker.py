"""Token usage logging and cost estimation."""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Pricing per 1M tokens (claude-sonnet-4-6 as of 2025, approximate)
# Input: $3.00/1M, Output: $15.00/1M, Cache-write: $3.75/1M, Cache-read: $0.30/1M
PRICE_INPUT_PER_1M = 3.00
PRICE_OUTPUT_PER_1M = 15.00
PRICE_CACHE_WRITE_PER_1M = 3.75
PRICE_CACHE_READ_PER_1M = 0.30


@dataclass
class StageUsage:
    stage: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_write_tokens: int = 0
    cache_read_tokens: int = 0

    @property
    def cost_usd(self) -> float:
        return (
            self.input_tokens * PRICE_INPUT_PER_1M / 1_000_000
            + self.output_tokens * PRICE_OUTPUT_PER_1M / 1_000_000
            + self.cache_write_tokens * PRICE_CACHE_WRITE_PER_1M / 1_000_000
            + self.cache_read_tokens * PRICE_CACHE_READ_PER_1M / 1_000_000
        )


@dataclass
class RunTokenTracker:
    """Accumulates token usage across all pipeline stages for a single report run."""

    stages: list[StageUsage] = field(default_factory=list)

    def record_usage(self, stage: str, usage) -> StageUsage:
        """Record token usage from an Anthropic API usage object.

        Args:
            stage: Stage name (e.g., 'analyze', 'format_zh_tw').
            usage: Anthropic usage object with input_tokens, output_tokens, etc.

        Returns:
            StageUsage dataclass.
        """
        su = StageUsage(
            stage=stage,
            input_tokens=getattr(usage, "input_tokens", 0),
            output_tokens=getattr(usage, "output_tokens", 0),
            cache_write_tokens=getattr(usage, "cache_creation_input_tokens", 0),
            cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0),
        )
        self.stages.append(su)
        logger.info(
            "[%s] in=%d out=%d cache_write=%d cache_read=%d cost=$%.4f",
            stage,
            su.input_tokens,
            su.output_tokens,
            su.cache_write_tokens,
            su.cache_read_tokens,
            su.cost_usd,
        )
        return su

    @property
    def total_tokens_used(self) -> int:
        return sum(s.input_tokens + s.output_tokens for s in self.stages)

    @property
    def total_tokens_cached(self) -> int:
        return sum(s.cache_read_tokens for s in self.stages)

    @property
    def total_cost_usd(self) -> float:
        return sum(s.cost_usd for s in self.stages)

    def log_summary(self) -> None:
        """Log a final cost summary."""
        logger.info(
            "Token summary: total=%d cached=%d cost=$%.4f",
            self.total_tokens_used,
            self.total_tokens_cached,
            self.total_cost_usd,
        )
