# Skill: rate-risk

Score a named risk by likelihood and impact and return a single risk-matrix table row.

## Input

- Named risk
- Likelihood (`High` | `Medium` | `Low`)
- Impact (`High` | `Medium` | `Low`)

## Action

Apply the matrix below to assign a combined rating.

| Likelihood | Impact | Combined rating |
| ---------- | ------ | --------------- |
| High | High | 🔴 Critical |
| High | Medium | 🟠 Elevated |
| Medium | High | 🟠 Elevated |
| Medium | Medium | 🟡 Moderate |
| Low | Any | 🟢 Monitor |

## Output

One risk-matrix table row:

`| [Risk] | [Likelihood] | [Impact] | [Rating] | [Confidence] | [Source] |`
