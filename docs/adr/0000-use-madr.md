# Use MADR for Architecture Decisions

## Context and Problem Statement

Architecture decision records need a consistent, machine-readable format that supports lightweight tooling, clear status tracking, and minimal boilerplate.

## Considered Options

* MADR (Markdown Architectural Decision Records)
* Michael Nygard's original ADR format
* Y-Statements (Alexandrian pattern)
* Custom format

## Decision Outcome

Chosen option: **MADR**, because it provides structured sections with good defaults, is the most widely tooled format (adr-tools, log4brains), and keeps decisions concise without mandatory fields that are rarely useful.

### Consequences

* Good, because consistent format makes scanning the decision log fast.
* Good, because MADR supports "Considered Options" tables that force explicit comparison.
* Neutral, because MADR omits "forces" framing — analysis goes in "Context and Problem Statement" instead.

## More Information

MADR specification: <https://adr.github.io/madr/>
Template version used: MADR 3.0.0
