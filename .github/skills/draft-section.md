# Skill: draft-section

Write exactly one named section of the intelligence report. Do not write any other section.

## Input

- Section name (from the ordered list below)
- Audited source list (output of `audit-bias`)
- Raw intelligence material

## Action

Write the requested section only.
If a section is not applicable, output:
`Not applicable for this report period — reason: [reason].`

Sections must appear in this order in the final assembled report:

1. Report metadata — title, audience, date, analyst note, confidence summary
1. Abbreviations and key terms — output of `define-terms`; collect all definitions here
1. Executive summary — 3–5 sentences; one actionable takeaway per audience segment
1. Source collection and bias audit summary — output of `audit-bias`
1. Macroeconomic context — leading indicators, PMI, yield curve, EM stress signals
1. Geopolitical developments — structured by region; ≥ 1 non-Western framing required
1. Energy and commodity intelligence — required when a chokepoint or energy event is active;
   must include BDTI, WTI/Brent, and chokepoint status
1. Financial market signals — VIX, DXY, MOVE, CDS spreads, equity futures, bond markets
1. Trump behavior prediction — apply the 7 behavioral heuristics from Intelligence Stack
   Section VIII; cite Truth Social, Axios, and Politico as primary sources
1. Risk assessment matrix — tabular output of `rate-risk`
1. Action items — output of `write-action-items`
1. Dissenting views and alternative interpretations — ≥ 1 credible counter-narrative per
   major assessment
1. Manipulation and CIB check — output of `check-cib`
1. 謠言警示 (Rumour alert) — output of `write-rumour-alert`; required for `zh-tw` and
   `zh-tw-elder` audiences
1. Source list — output of `write-source-list`

## Output

The drafted section text only.
