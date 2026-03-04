# GitHub Copilot Instructions — Homemade Intelligence

> These instructions guide GitHub Copilot when working in this repository.

## Project Identity

**Homemade Intelligence** is a personal, bias-aware intelligence platform for geopolitical analysis and investment decision-making. It synthesizes information from diverse global sources and produces actionable analysis reports tailored to three audiences: English speakers, Mandarin-speaking Taiwanese citizens, and Taiwanese elders (65+).

This is **not** a news aggregator. It is a structured analytical system with triangulation methodology, bias tracking, and multi-audience report generation.

## Tech Stack

- **Language:** Python 3.11+
- **Package Manager:** [Pixi](https://pixi.sh/) (conda-forge based, see `pixi.toml`)
- **Linter & Formatter:** [Ruff](https://docs.astral.sh/ruff/) (see `ruff.toml`)
- **Testing:** pytest (run via `pixi run -e dev pytest tests/ -v`)
- **Pre-commit:** hooks defined in `.pre-commit-config.yaml`
- **CI:** GitHub Actions (`.github/workflows/ci.yml`)
- **Build shortcuts:** `Makefile` (`make dev`, `make lint`, `make test`, etc.)

## Coding Standards

- Follow Ruff configuration in `ruff.toml`: line length 120, double quotes, space indentation
- Use type hints on all function signatures
- Use `pathlib.Path` over `os.path` for file operations
- Imports: sorted by isort with `homemade_intelligence` as known first-party
- Docstrings: Google style, required on all public modules, classes, and functions
- All new Python code must pass `ruff check` and `ruff format --check`
- Tests: place in `tests/` mirroring `tools/` structure; use pytest fixtures and parametrize

## Project Architecture

```
homemade-intelligence/
├── references/           # Knowledge base, roadmap, and Claude project instructions
│   ├── knowledgebase/    # Intelligence Stack v2.0, analytical frameworks
│   └── roadmap/          # Development roadmap
├── sources/              # (planned) Source configuration and monitoring rules
├── reports/              # Generated intelligence reports
│   ├── en/               # English reports
│   ├── zh-tw/            # Traditional Chinese (general audience)
│   └── zh-tw-elder/      # Traditional Chinese (elder-accessible)
├── tools/                # Python automation scripts and utilities
└── tests/                # Test suite
```

## Domain Knowledge

### Core Analytical Principles

1. **Triangulation over trust** — No single source is authoritative. Cross-reference across ideologically and geographically distinct outlets.
2. **Bias as a variable** — Every source has a perspective. Track and label bias; don't pretend objectivity exists.
3. **Leading over lagging** — Prioritize leading indicators (VIX, CDS, PMI, tanker flows) over lagging confirmations (GDP, official statements).
4. **Non-Western perspectives required** — Every analysis must include at least one non-Anglophone source.
5. **Manipulation awareness** — Consider whether underlying information may be subject to coordinated manipulation.
6. **Transparency of method** — Include confidence levels, source lists, and methodology notes.

### Intelligence Source Architecture

The project uses a 10-layer source architecture (v2.0). See `references/knowledgebase/international-situation-intelligence-stack.md` for the full reference. Key layers:

- Layer I: Geopolitics & Strategic Affairs (think tanks, journals)
- Layer IV: Energy, Commodities & Chokepoint Intelligence (NEW in v2.0)
- Layer VII: Early Warning Indexes & Quantitative Dashboards
- Layer VIII: Trump Behavior Prediction Stack
- Layer IX: Social Media & AI Manipulation Analysis

### Key Analytical Frameworks

- **Compound Vulnerability Framework** — Scores target states across military, economic, and political dimensions
- **Behavioral Heuristics for Trump Decision Prediction** — 7 empirically observed patterns
- **Real-Time Manipulation Detection Framework** — 9-signal checklist for identifying CIB
- **Chokepoint Monitoring Quick-Reference** — 5 critical maritime chokepoints
- **Analytical Failure Mode Reference** — 7 documented failure modes to avoid

### Multi-Audience Report Generation

When generating or working on report content:

| Audience | Language | Tone | Key Features |
|----------|----------|------|--------------|
| **English speakers** | English | Professional, analytical | Full citations, confidence levels, methodology notes |
| **Taiwanese citizens** | Traditional Chinese (繁體中文) | Informative, balanced | Taiwan-standard terminology (e.g., 總統 not 領導人), note narrative divergences |
| **Taiwanese elders (65+)** | Traditional Chinese (simplified vocab) | Warm, respectful, never condescending | Traffic light risk indicators (🟢🟡🔴), LINE misinformation alerts (謠言警示), plain language |

### Taiwan-Specific Conventions

- Always use Traditional Chinese (繁體中文), never Simplified Chinese
- Use Taiwan-standard political terminology
- Taiwan strait safety is a first-class analytical domain, not a subtopic of US-China relations

## Commit Messages

- Use imperative mood: "Add Taiwan strait risk module" not "Added..."
- Prefix with category when helpful: `feat:`, `fix:`, `docs:`, `ci:`, `refactor:`, `test:`
- Keep subject line under 72 characters

## What NOT to Do

- Never commit API keys, secrets, or `.env` files
- Never use Simplified Chinese (简体中文) in Taiwan-audience reports
- Never treat any single source as authoritative — always triangulate
- Never generate analysis without source citations and confidence levels
- Never present opinion as fact in generated reports
