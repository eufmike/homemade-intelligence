# Skill: audit-bias

Audit a candidate source list for ideological balance, geographic diversity, and analytical
failure modes before any drafting begins.

## Input

Source list produced by `select-sources`.

## Action

Answer every question below.
For each "No", either add the missing source or record a named gap under **Source gaps** in
the report.

- [ ] Does the collection span ≥ 2 distinct ideological perspectives?
- [ ] Is ≥ 1 non-Anglophone, non-Western source included?
- [ ] Are leading indicators (VIX, CDS, PMI, tanker flows) represented alongside lagging ones?
- [ ] Have all six Analytical Failure Modes been checked?
  - Anglophone epistemic capture
  - Negotiation optimism bias
  - Monocausal attribution
  - Recency bias
  - Confirmation bias
  - Energy market blindspot
- [ ] Are state-media sources (RT, Xinhua, Global Times) used only as narrative trackers,
      never as factual claims?
- [ ] Are all sources present in Intelligence Stack v2.0, or explicitly flagged if unlisted?

## Output

A pass/fail audit result with gap notes, ready to include as the **Source collection and bias
audit summary** section of the report.
