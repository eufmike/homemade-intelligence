# Skill: rate-confidence

Attach a calibrated confidence label to a single analytical assessment statement.

## Input

A single analytical assessment statement.

## Action

Attach exactly one label from the table below.
State the label, the source count, and a one-sentence rationale.

| Label | Definition |
| ----- | ---------- |
| **High** | Supported by ≥ 3 independent, ideologically distinct sources; no credible counter-evidence |
| **Medium** | Supported by ≥ 2 sources; counter-narratives exist but are not well-evidenced |
| **Low** | Single source or indirect inference; treat as hypothesis, not conclusion |

## Output

`Confidence: [High / Medium / Low] — [rationale].`
