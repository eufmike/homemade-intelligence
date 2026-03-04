# Project Instructions

## GitHub Copilot

**Goal**

- Stay current with the latest functions and project structure
- Learn the most efficient and concise workflow
- Use high-level instructions to drive full deployment
- Support architecture design; provide system design knowledge

## Claude Code

- Always suggest instructions compatible between Claude and Copilot
- Prefer declarative, intent-driven prompts over step-by-step commands
- Maintain consistency in naming conventions, file structure, and module boundaries
- Prioritize minimal, composable changes that are easy to review and revert

## Claude Project

**Goal**

- Serve as the central knowledge hub for project context, goals, and constraints
- Maintain up-to-date system design documentation within the project memory
- Bridge the gap between high-level architecture decisions and low-level implementation

**Workflow**

- Use structured markdown to capture decisions, rationale, and open questions
- Keep instructions concise — one clear intent per instruction block
- Version-track major instruction changes with a brief changelog note

**Architecture & Design**

- Document component boundaries and data flow before implementation begins
- Prefer explicit dependency declarations over implicit coupling
- Flag design trade-offs with pros/cons so decisions are auditable

**Cross-tool Compatibility**

- Write prompts and instructions that work across Claude, Copilot, and other AI tools
- Avoid tool-specific syntax unless strictly necessary; abstract it behind comments
- Shared vocabulary: use consistent domain terms across all tools and docs

## General Principles

- **Clarity over cleverness** — readable instructions outperform clever shortcuts
- **Incremental delivery** — aim for small, testable, deployable units
- **Single source of truth** — project instructions live here; tools reference this document
- **Review before merge** — AI-generated code must pass human review before integration
