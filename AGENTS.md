# AGENTS.md — Homemade Intelligence

> Shared AI agent instructions for Claude Code, GitHub Copilot, and other AI coding assistants.
> Tool-specific overrides live in `.github/copilot-instructions.md` and `.claude/instructions.md`.

## Quick Reference

- **Python 3.11+** — Pixi package manager (`pixi.toml`)
- **Ruff** for linting and formatting (`ruff.toml`) — line length 120, double quotes, space indent
- **pytest** for testing — `pixi run -e dev pytest tests/ -v`
- **Pre-commit** hooks — `pixi run -e dev pre-commit run --all-files`

## What This Project Is

A personal intelligence platform for geopolitical analysis and investment decisions. Three audience outputs:

1. **English** — Professional analytical reports with citations and confidence levels
2. **Traditional Chinese (繁體中文)** — Taiwan-standard terminology, balanced tone
3. **Elder-accessible (65+)** — Simplified vocabulary, traffic light risk indicators, LINE misinformation alerts

## Coding Rules

1. Type hints on all function signatures
2. Google-style docstrings on all public APIs
3. `pathlib.Path` over `os.path`
4. isort imports with `homemade_intelligence` as first-party
5. Tests in `tests/` mirroring `tools/` structure; use fixtures and parametrize
6. All code must pass `ruff check` and `ruff format --check`

## Domain Rules

1. Never treat a single source as authoritative — always triangulate
2. Track and label bias as an explicit variable
3. Every analysis includes at least one non-Anglophone source
4. Include confidence levels (High / Medium / Low) on key assessments
5. Include source citations for every factual claim
6. Check for coordinated inauthentic behavior (CIB) indicators
7. Never use Simplified Chinese (简体中文) for Taiwan audiences
8. Use Taiwan-standard political terms (e.g., 總統 not 領導人)

## Commit Convention

Imperative mood, optional category prefix, under 72 characters:

```text
feat: Add source triangulation module
fix: Correct VIX threshold in early warning config
docs: Update intelligence stack to v2.1
test: Add parametrized tests for report generator
```

## Key Files

- `references/knowledgebase/international-situation-intelligence-stack.md` — Source architecture v2.0
- `references/roadmap/roadmap.md` — Development roadmap
- `pixi.toml` — Package manager config
- `ruff.toml` — Linter and formatter config
- `Makefile` — Development shortcuts
