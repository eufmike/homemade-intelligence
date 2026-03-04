# Skill: select-sources

Select the source set for a report using the Intelligence Stack v2.0 layer structure.

## Input

- Topic description
- Active geopolitical or market events
- Target audience (`english` | `zh-tw` | `zh-tw-elder`)

## Action

Select sources from the Intelligence Stack v2.0 layer structure.
For each report the minimum coverage is:

| Layer | Required sources (minimum) |
| ----- | -------------------------- |
| Layer II — Western Anglophone news | ≥ 2 ideologically distinct outlets (e.g., Reuters + FT) |
| Layer III — Economics & Policy | ≥ 1 institutional source (IMF / BIS / OECD) |
| Layer IV — Energy & Commodities | ≥ 1 source if any Middle East, energy, or trade event is active |
| Layer V — Financial Markets | ≥ 2 leading indicators (VIX, CDS, PMI, BDTI, yield curve) |
| Layer VI — Non-Western Sources | ≥ 1 non-Anglophone outlet (e.g., Nikkei Asia, Al Jazeera, SCMP) |
| Layer VII — Early Warning Indexes | ≥ 2 quantitative signals |
| Layer VIII — Trump Behavior Stack | Required if any US executive action is a material risk factor |

## Output

A structured source list grouped by layer, ready as input for `audit-bias`.
