# Shared AI Coding Assistant Configuration: GitHub Copilot + Claude Code

**Last updated:** 2026-03-12
**Status:** Current — reflects ecosystem state as of early 2026

---

## The Problem

AI coding assistants have no persistent memory. Every session starts blank. Without configuration files, you repeat the same context every time — tech stack, conventions, project structure, deployment rules. Each tool reads a different file format, creating duplication risk when you use more than one assistant.

---

## The Ecosystem: Who Reads What

| Tool | Primary file | Also reads |
|---|---|---|
| Claude Code | `CLAUDE.md` | `AGENTS.md` |
| GitHub Copilot (agent) | `.github/copilot-instructions.md` | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/instructions/**.instructions.md` |
| OpenAI Codex CLI | `AGENTS.md` | walks directory tree |
| Cursor | `.cursor/rules/` | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` | `AGENTS.md` (with `includeDirectories` config) |
| Windsurf | `.windsurfrules` | — |

**Key insight (August 2025):** GitHub's Copilot Coding Agent added native `AGENTS.md` support, making it the most cross-compatible format. Claude Code also reads `AGENTS.md` as a fallback.

---

## Recommended Project Structure

The single-source-of-truth approach using `AGENTS.md` as the universal baseline:

```
project-root/
├── AGENTS.md                              # Universal baseline — all tools read this
├── CLAUDE.md                              # Claude-specific additions only (optional)
├── .github/
│   ├── copilot-instructions.md            # Copilot-specific additions only (optional)
│   ├── instructions/                      # Scoped instructions (Copilot, July 2025+)
│   │   ├── frontend.instructions.md       # applyTo: "src/frontend/**"
│   │   ├── backend.instructions.md        # applyTo: "backend/**"
│   │   └── testing.instructions.md        # applyTo: "tests/**"
│   ├── agents/                            # Agent definitions
│   └── prompts/                           # Slash command prompts
└── .claude/
    └── commands/ -> ../.github/prompts/   # Symlink to share prompts
```

### Minimal CLAUDE.md when using AGENTS.md

If `AGENTS.md` is your source of truth, `CLAUDE.md` can simply be:

```markdown
# Project Instructions

Follow the rules in ./AGENTS.md exactly. Additions specific to Claude Code only below.

## Claude-specific
- Use `pixi run` not bare `pip` or `python`
- Stream responses via SSE using existing pipeline.py patterns
```

---

## The Symlink Approach (Advanced)

Source: [Kesin11 on Zenn](https://zenn.dev/kesin11/articles/20251210_ai_agent_symlink?locale=en)

For teams using 3+ tools, maintain one canonical file and symlink others to it:

```bash
# Place canonical instructions in .github/copilot-instructions.md
# Then create symlinks for other tools:
ln -s ../.github/copilot-instructions.md CLAUDE.md
ln -s ../../.github/prompts .claude/commands
ln -s ../../.github/agents .claude/agents
```

Subdirectory-specific instructions:

```bash
# Place tool-specific instructions under .github/instructions/
# Symlink them where each tool expects to find them:
ln -s ../.github/instructions/frontend.instructions.md src/frontend/CLAUDE.md
ln -s ../.github/instructions/testing.instructions.md tests/CLAUDE.md
```

**Caveat:** Gemini CLI needs `includeDirectories` set in `.gemini/settings.json` since it does not auto-discover nested files.

---

## AGENTS.md: Recommended Template

Based on analysis of 2,500+ real repositories (GitHub Blog, 2025):

```markdown
# [Project Name] — Agent Instructions

## Project Overview
[One paragraph: what it does, tech stack with versions, key constraints]

## Commands
- Build: `npm run build`
- Test: `pytest -v tests/`
- Lint: `npm run lint`
- Dev server: `pixi run serve`

## Tech Stack
- Language: Python 3.11, TypeScript (strict)
- Framework: FastAPI 0.115, Next.js 16 (App Router)
- Database: SQLite + ChromaDB 1.x
- Package manager: pixi (use `pixi run`, never bare pip)

## Project Structure
```
backend/          FastAPI app, agent pipeline, DB models
frontend/         Next.js app, React components
tests/            pytest test suite (31 tests)
sources/          RSS feed config, data sources
docs/             Architecture decisions (MADRs)
```

## Coding Conventions
- Line length: 120 chars
- Quotes: double
- Docstrings: Google style
- No type: ignore without explanation

## Boundaries
- Always: run `pixi run -e dev pytest tests/ -v` before marking done
- Ask first: changes to DB schema, changes to streaming pipeline API
- Never: commit .env files, modify pixi.lock manually, use Python 3.14
```

---

## Six Essential AGENTS.md Sections (Priority Order)

1. **Commands** — exact executable commands with flags, placed early
2. **Tech stack** — versions included, prevents wrong assumptions
3. **Project structure** — explicit directory map with purpose of each
4. **Code style** — real code examples over abstract descriptions
5. **Git workflow** — commit conventions, branch naming
6. **Boundaries** — three-tier: "Always do" / "Ask first" / "Never do"

---

## Dos

- **Keep it under 150 lines.** Frontier LLMs reliably follow ~150–200 instructions; Claude Code's own system prompt consumes ~50, leaving ~100–150 for yours. Files over 500 lines have most content silently ignored.
- **Use exact commands.** Write `npm test -- --coverage` not "run the tests."
- **Show real code examples** for style conventions, not prose descriptions.
- **Be specific about versions.** "FastAPI 0.115" not just "FastAPI."
- **Map the file tree explicitly.** Agents do not intuit directory purpose.
- **Use the three-tier boundary system.** Always / Ask first / Never.
- **Version-control it.** Update `AGENTS.md` in the same PR as any stack change.
- **Start task-specific agents narrow.** A `@test-agent` that only writes tests and never modifies source is more reliable than a general helper.
- **Nest AGENTS.md for monorepos.** Each package can have its own; the nearest file takes precedence.

---

## Don'ts

- **Don't duplicate content across files.** One source of truth in `AGENTS.md`; tool-specific files add only what is genuinely tool-specific.
- **Don't include code style rules delegable to linters.** Indentation, trailing commas, import order — these belong in `ruff.toml`, `.eslintrc`, Prettier. They waste your instruction budget.
- **Don't use vague platitudes.** "Write clean code," "follow best practices," "be helpful" consume tokens with zero specificity.
- **Don't paste full API docs.** Link to `docs/` or an external URL instead.
- **Don't include things the agent can discover by reading the codebase.** Research on 2,500+ repos found that discoverable info actively degrades performance.
- **Don't use task-specific instructions in the persistent config.** One-off guidance belongs in the prompt, not the config file.
- **Don't let it go stale.** A wrong instruction is worse than no instruction.
- **Don't auto-generate the file.** Manually authored files addressing real problems consistently outperform generated ones.
- **Don't exceed 300 lines for CLAUDE.md.** Claude Code reads it every session; size directly impacts latency and cost.

---

## GitHub Copilot: Scoped Instructions (July 2025+)

Copilot supports glob-targeted instructions via frontmatter. Place files in `.github/instructions/`:

```markdown
---
applyTo: "src/frontend/**"
---

# Frontend Instructions
- Use React functional components only
- State management: Zustand (not Redux)
- Styling: Tailwind CSS utility classes
```

This lets you maintain different rules for TypeScript vs Python, frontend vs backend, without cluttering a single file.

---

## Claude Code Hierarchy

Claude Code reads files in this order, merging all that apply:

1. `~/.claude/CLAUDE.md` — personal global instructions
2. `./CLAUDE.md` — project root (committed to git)
3. Subdirectory `CLAUDE.md` files — scoped to specific directories
4. `./AGENTS.md` — fallback if no CLAUDE.md

All layers are additive. The most specific file wins on conflicts.

---

## Claude Code + GitHub Integration (2026)

As of February 2026, Claude (Anthropic) and Codex (OpenAI) are available as first-class coding agents inside GitHub Copilot for Business and Pro subscribers. They run on GitHub's shared platform with:

- Unified governance and audit logs
- Shared context across sessions
- No additional subscription — included with Copilot

`AGENTS.md` is the recommended standard for multi-agent workflows combining Copilot Coding Agent and Claude Code Agent.

---

## Sources

- [CLAUDE.md, AGENTS.md, and Every AI Config File Explained — DeployHQ](https://www.deployhq.com/blog/ai-coding-config-files-guide)
- [How to write a great agents.md: Lessons from 2,500+ repositories — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Copilot coding agent now supports AGENTS.md — GitHub Changelog](https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/)
- [Tips for Coexisting GitHub Copilot Settings with Claude Code — Zenn/Kesin11](https://zenn.dev/kesin11/articles/20251210_ai_agent_symlink?locale=en)
- [Using Claude Code with GitHub Copilot: A Guide — Anders Sveen / Medium](https://anderssv.medium.com/using-claude-code-with-github-copilot-a-guide-42904ea6dce0)
- [Claude and Codex now available for Copilot Business & Pro — GitHub Changelog](https://github.blog/changelog/2026-02-26-claude-and-codex-now-available-for-copilot-business-pro-users/)
- [Use custom instructions in VS Code — VS Code Docs](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [GitHub Copilot Custom Instructions Complete Guide — SmartScope](https://smartscope.blog/en/generative-ai/github-copilot/github-copilot-custom-instructions-guide/)
- [AGENTS.md official site](https://agents.md/)
- [AGENTS.md GitHub repository](https://github.com/agentsmd/agents.md)
