# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Added

- AI instruction files for multi-agent compatibility:
  - `.github/copilot-instructions.md` — GitHub Copilot workspace instructions
  - `.claude/instructions.md` — Claude Code project instructions
  - `.claude/settings.json` — Claude Code permissions configuration
  - `AGENTS.md` — Shared agent instructions (cross-tool compatible)
- `.github/CODEOWNERS` — default reviewers for pull requests
- `.github/ISSUE_TEMPLATE/config.yml` — issue template chooser with Intelligence Stack link
- `.github/ISSUE_TEMPLATE/source_suggestion.md` — new template for intelligence source proposals
- VS Code setting `github.copilot.chat.codeGeneration.useInstructionFiles` enabled

### Changed

- Redesigned `.github/` directory structure aligned with README project goals
- Upgraded issue templates (bug report, feature request) with richer metadata
- Enhanced PR template with affected-area checkboxes and stronger checklist
- Improved `SECURITY.md` with security practices section
- Upgraded CI workflow: added concurrency control, AI instructions check job
- Updated Dependabot config with commit message prefixes and scheduled day
- CI workflow uses 2-space YAML indentation (standard)

### Previous

- Project foundation: README, intelligence source architecture, project structure
- Multi-audience report framework (English, Traditional Chinese, Elder-accessible)
- International Situation Intelligence Stack v2.0
- Prompt templates for pre-market analysis
- Project housekeeping: `.gitignore`, `LICENSE`, `pixi.toml`, EditorConfig, pre-commit, ruff
- GitHub CI workflow (lint + test via Pixi)
- Dependabot configuration for dependency updates
- Pull request template
- `Makefile` with convenience shortcuts (`make dev`, `make lint`, `make test`, etc.)
- `.python-version` file for pyenv compatibility
- `tests/` directory with placeholder smoke test
- `tools/__init__.py` Python package marker

---

*Maintained by Mike Shih*
