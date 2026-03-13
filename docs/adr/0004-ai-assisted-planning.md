# AI-assisted planning with two-track, multi-year roadmap

## Context and Problem Statement

The platform has a development runway measured in years, not sprints. Two fundamentally different types of work run in parallel: (1) **code development** — building features, pipelines, and infrastructure with concrete deliverables and testable acceptance criteria; and (2) **exploratory research** — geopolitical methodology, source discovery, and analytical framework development, which is hypothesis-driven and open-ended by nature.

Planning these two tracks with the same cadence and format produces one of two failure modes: research work gets forced into sprint tickets it does not fit, or code work drifts without milestones. Neither track, on its own, tells the whole story of the platform's direction.

The question is: how should multi-year planning be structured so that an AI agent can participate usefully — generating plans, reviewing progress, flagging drift, and proposing priorities — without losing track of long horizons or conflating the two work types?

## Decision Drivers

- Multi-year horizon demands structured checkpoints and annual re-anchoring, not just a rolling backlog
- Code development and exploratory research have incompatible rhythms and output types — forcing them into a single format degrades both
- AI agents need machine-readable, consistently structured plans to provide useful planning assistance across sessions (agents have no persistent memory)
- Plans must be diff-able in git so changes are auditable and LLM-generated revisions are reviewable
- Planning files should be loadable as context by the same skills and prompts used for analysis

## Considered Options

- Single unified roadmap (one backlog, one cadence, all work types mixed)
- Two separate track plans with independent structure and cadence
- Three-tier hierarchy: multi-year vision → annual OKRs → quarterly sprints, applied uniformly to both tracks

## Decision Outcome

Chosen option: **two-track planning with a shared multi-year vision layer**, because the two work types require different structure below the vision level, but a shared top-level anchor prevents the tracks from diverging into unrelated projects.

### Planning structure

```text
references/roadmap/
├── vision.md                    ← shared multi-year direction (reviewed annually)
├── code-development/
│   ├── roadmap.md               ← rolling quarterly plan; measurable deliverables
│   └── YYYY-QN-sprint.md        ← per-sprint detail (optional)
└── exploratory-research/
    ├── roadmap.md               ← active hypotheses, open questions, reading lists
    └── YYYY-theme.md            ← per-theme research log (optional)
```

### Track definitions

**Code development track**

- Unit of planning: quarterly milestone
- Output type: shippable software (features, pipelines, tooling, tests)
- Acceptance criteria: required — each item must have a testable definition of done
- AI agent role: generate implementation plans from roadmap items, sequence tasks, identify blockers, draft tickets
- Review cadence: quarterly review + annual re-prioritization against vision

**Exploratory research track**

- Unit of planning: named hypothesis or research theme, with a target horizon (months to a year) but no fixed deadline
- Output type: written analysis, new source recommendations, methodology updates, framework revisions — not software
- Acceptance criteria: optional — a theme may be closed with a null result; that is a valid outcome
- AI agent role: surface relevant sources from the Intelligence Stack, draft research outlines, identify contradicting evidence, suggest follow-on questions
- Review cadence: monthly hypothesis check-in + annual theme retrospective against vision

### AI agent participation

Planning sessions load the following context before any plan generation or review:

```text
references/roadmap/vision.md
references/roadmap/code-development/roadmap.md   (for code sessions)
references/roadmap/exploratory-research/roadmap.md  (for research sessions)
AGENTS.md
.github/instructions/domain.instructions.md
```

A planning prompt (`/plan`) should be added to `.github/prompts/` that loads the relevant track and asks the agent to: (1) identify items overdue or stalled, (2) propose the next three priorities, (3) flag any items that belong on the other track.

### Consequences

- Good, because the two-track structure makes the AI agent's planning context precise — it loads only what is relevant to the session type.
- Good, because quarterly milestones in the code track are testable, making AI-generated sprint plans verifiable against `tests/`.
- Good, because open-ended research themes are not penalized for not shipping code — the agent evaluates them on evidence quality, not velocity.
- Good, because all plans are Markdown in git — LLM revisions are reviewable as diffs and the history is auditable.
- Bad, because maintaining two roadmaps requires discipline to keep `vision.md` as the anchor; without that, the tracks drift.
- Neutral, because the planning prompt does not yet exist — it is a near-term code development task.

## Pros and Cons of the Options

### Single unified roadmap

- Good, because simple — one file to update.
- Bad, because research themes written as sprint tickets either have fake deadlines or stay perpetually "in progress."
- Bad, because code milestones written as open hypotheses lose their acceptance criteria and become unverifiable.

### Two-track plans with shared vision (chosen)

- Good, because each track uses the format that fits its work type.
- Good, because the shared vision layer keeps the platform coherent across years.
- Neutral, because two roadmaps require two review rhythms — slightly more overhead.

### Three-tier hierarchy applied uniformly

- Good, because OKR-style structure is well-understood.
- Bad, because research does not produce key results on a quarterly cadence — the format produces false precision.
- Bad, because forcing code work into the same OKR framing as research dilutes accountability for shipping.

## More Information

- `references/roadmap/` — roadmap directory (to be restructured per this ADR)
- `references/roadmap/vision.md` — to be created as the first implementation step
- `docs/adr/0000-use-madr.md` — MADR format decision
- `docs/adr/adr-template.md` — blank template for new ADRs
- Related: the planning prompt (`/plan`) is a code development task to be added to `.github/prompts/`
