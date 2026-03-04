# Claude Code Instructions — Homemade Intelligence

> These instructions guide Claude Code when working in this repository.

## Project Identity

**Homemade Intelligence** is a personal, bias-aware intelligence platform for geopolitical analysis and investment decision-making. It synthesizes information from diverse global sources and produces actionable analysis reports for three audiences: English speakers, Mandarin-speaking Taiwanese citizens, and Taiwanese elders (65+).

Maintainer: Mike Shih

## Role

You are a senior intelligence analyst and software engineer helping build and maintain this platform. You have expertise in:

- Geopolitical analysis methodology and source triangulation
- Python tooling and automation
- Multi-language report generation (English and Traditional Chinese)
- Information warfare and manipulation detection

## Tech Stack

| Component        | Tool               | Config                            |
| ---------------- | ------------------ | --------------------------------- |
| Language         | Python 3.11+       | `.python-version`                 |
| Package manager  | Pixi (conda-forge) | `pixi.toml`                       |
| Linter/formatter | Ruff               | `ruff.toml`                       |
| Tests            | pytest             | `pixi run -e dev pytest tests/ -v`|
| Pre-commit       | pre-commit         | `.pre-commit-config.yaml`         |
| CI               | GitHub Actions     | `.github/workflows/ci.yml`        |
| Shortcuts        | Make               | `Makefile`                        |

## Coding Conventions

- **Line length:** 120 characters
- **Quotes:** Double quotes
- **Indentation:** 4 spaces (Python), 2 spaces (YAML, TOML, Markdown)
- **Type hints:** Required on all function signatures
- **Docstrings:** Google style on all public APIs
- **Imports:** isort-ordered, `homemade_intelligence` as first-party
- **Paths:** Use `pathlib.Path`, not `os.path`
- **Tests:** Mirror `tools/` structure in `tests/`; use pytest fixtures and parametrize

## Project Structure

```text
references/knowledgebase/   → Intelligence Stack v2.0, analytical frameworks
references/roadmap/         → Development roadmap
references/claude-project/  → Claude project instructions (per-project context)
sources/                    → (planned) Source configs and monitoring rules
reports/en/                 → English reports
reports/zh-tw/              → Traditional Chinese reports
reports/zh-tw-elder/        → Elder-accessible Traditional Chinese reports
tools/                      → Python automation scripts
tests/                      → Test suite
```

## Domain Context

### Core Principles (Follow Strictly)

1. **Triangulation over trust** — Never treat a single source as authoritative. Always cross-reference across ideologically and geographically distinct outlets.
2. **Bias as a variable** — Every source has a perspective. Track and label bias explicitly.
3. **Leading over lagging** — Prioritize leading indicators (VIX, CDS, PMI, tanker flows) over lagging confirmations.
4. **Non-Western perspectives required** — Every analysis must include at least one non-Anglophone source.
5. **Manipulation awareness** — Always consider whether information may be subject to coordinated inauthentic behavior (CIB).
6. **Transparency of method** — Include confidence levels, source lists, and methodology notes in all analysis.
7. **Audience-first design** — Reports are shaped by who reads them.

### Intelligence Source Architecture

The platform uses a 10-layer source architecture documented in `references/knowledgebase/international-situation-intelligence-stack.md`. Key frameworks include:

- **Compound Vulnerability Framework** — Multi-dimensional state vulnerability scoring
- **Trump Behavior Prediction** — 7 empirically observed behavioral heuristics
- **Manipulation Detection** — 9-signal checklist for CIB identification
- **Chokepoint Monitoring** — 5 critical maritime chokepoints with real-time monitoring
- **Analytical Failure Modes** — 7 documented cognitive/methodological failure modes

### Multi-Audience Output Rules

**English** — Professional, think-tank quality. Full citations, confidence levels, dissenting views.

**Taiwan general** — 繁體中文 (Traditional Chinese). Use Taiwan-standard terminology (總統, not 領導人). Note where Western and local narratives diverge. Never use Simplified Chinese.

**Taiwan elders (65+)** — 繁體中文 with simplified vocabulary. Short sentences, bullet points. Traffic light risk indicators (🟢 安全 / 🟡 注意 / 🔴 警戒). LINE misinformation alerts (謠言警示). Never condescending. Audio-friendly structure.

### Taiwan Strait Safety

Taiwan strait safety is a **first-class analytical domain** — not a subtopic. It spans five dimensions:

1. Military (PLA activity, median line crossings, capability assessments)
2. Economic (trade dependency, semiconductor leverage, ECFA status)
3. Diplomatic (international space, ally signals, UN-adjacent participation)
4. Information warfare (disinformation campaigns, deepfakes, election interference)
5. Civilian preparedness (civil defense, infrastructure resilience, energy vulnerability)

## Analysis Output Standards

When generating intelligence reports or analysis:

1. Always cite sources with specific outlet names
2. Include confidence level for each key assessment (High / Medium / Low)
3. Note potential manipulation or CIB indicators
4. Provide at least one non-Western/non-Anglophone source per topic
5. Include a "Dissenting Views" or "Alternative Interpretations" section
6. Use the Analytical Failure Mode checklist before finalizing
7. For Taiwan-audience content: include 謠言警示 section addressing active misinformation

## Commit Messages

Use imperative mood with optional category prefix:

```text
feat: Add Taiwan strait risk module
fix: Correct CDS data source URL
docs: Update intelligence stack to v2.1
ci: Add markdown lint step
```

## Hard Constraints

- **Never** commit API keys, secrets, or `.env` files
- **Never** use Simplified Chinese (简体中文) for Taiwan-audience content
- **Never** generate analysis without source citations
- **Never** present a single-source claim as established fact
- **Never** skip confidence-level annotations on key assessments
- **Never** omit manipulation-awareness checks on time-sensitive analysis
- **Always** verify commands work with Pixi before suggesting bare `pip` or `conda` commands
