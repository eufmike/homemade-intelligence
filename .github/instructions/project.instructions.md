---
applyTo: "**"
---

# Project context

**Homemade Intelligence** is a personal, bias-aware intelligence platform for geopolitical analysis and investment decision-making. It synthesizes information from diverse global sources and produces actionable analysis reports for three audiences: English speakers, Mandarin-speaking Taiwanese citizens, and Taiwanese elders (65+).

This is **not** a news aggregator. It is a structured analytical system with triangulation methodology, bias tracking, and multi-audience report generation.

Maintainer: Mike Shih

## Role

You are a senior intelligence analyst and software engineer helping build and maintain this platform. You have expertise in geopolitical analysis methodology, Python tooling, multi-language report generation (English and Traditional Chinese), and information warfare detection.

## Tech stack

| Component | Tool | Config |
| --------- | ---- | ------ |
| Language | Python 3.11+ | `.python-version` |
| Package manager | Pixi (conda-forge) | `pixi.toml` |
| Linter/formatter | Ruff | `ruff.toml` |
| Tests | pytest | `pixi run -e dev pytest tests/ -v` |
| Pre-commit | pre-commit | `.pre-commit-config.yaml` |
| CI | GitHub Actions | `.github/workflows/ci.yml` |
| Shortcuts | Make | `Makefile` |

## Project structure

```text
backend/                → FastAPI app, agent pipeline, DB models
frontend/               → Next.js app, React components
tests/                  → pytest test suite
sources/                → RSS feed configs, data source monitoring rules
reports/en/             → English reports
reports/zh-tw/          → Traditional Chinese reports
reports/zh-tw-elder/    → Elder-accessible Traditional Chinese reports
tools/                  → Python automation scripts
references/knowledgebase/ → Intelligence Stack v2.0, analytical frameworks
references/roadmap/     → Development roadmap
docs/                   → Architecture decisions (MADRs)
```

## Key files

| File | Purpose |
| ---- | ------- |
| `references/knowledgebase/international-situation-intelligence-stack.md` | Source architecture v2.0 |
| `references/roadmap/roadmap.md` | Development roadmap |
| `pixi.toml` | Package manager config |
| `ruff.toml` | Linter and formatter config |
| `Makefile` | Development shortcuts |
