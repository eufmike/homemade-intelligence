# AGENTS.md — Homemade Intelligence

Single source of truth for all AI coding assistants (Claude Code, GitHub Copilot, Codex CLI, Cursor).
Detailed instructions live in `.github/instructions/` and are auto-loaded by each tool.

## Instruction files

| File | Scope | Contents |
| ---- | ----- | -------- |
| `.github/instructions/project.instructions.md` | `**` | Project identity, role, tech stack, project structure, key files |
| `.github/instructions/coding.instructions.md` | `**` | Coding conventions, commit messages, hard constraints |
| `.github/instructions/domain.instructions.md` | `reports/**, tools/**, backend/**` | Analytical principles, source architecture, multi-audience rules, Taiwan Strait |
| `.github/instructions/markdown.instructions.md` | `**/*.md` | Markdown formatting rules |
| `.github/instructions/market-report.instrunction.md` | market reports | Pre-market and daily market report structure |

## Quick reference

```bash
# Run tests
pixi run -e dev pytest tests/ -v

# Lint + format
pixi run -e dev pre-commit run --all-files

# Dev server
pixi run serve
```

**Never:** commit `.env`, use `pip` directly, use Simplified Chinese for Taiwan-audience content.
