# Market report instruction

Instructions for generating pre-market and daily market analysis reports.
These rules are synthesised from three reference projects and the project's own analytical standards:

- **OpenBB Terminal** (62.5k ★) — data-layer taxonomy and market-overview structure
  — <https://github.com/OpenBB-finance/OpenBB>
- **quant-trading** (9.3k ★) — indicator selection and signal-verification discipline
  — <https://github.com/je-suis-tm/quant-trading>
- **algorithmic-trading-python** (2.8k ★) — quantitative momentum and value framing
  — <https://github.com/nickmccullum/algorithmic-trading-python>

---

## Core principles

Every report must satisfy all five conditions before being finalised:

1. **Source diversity** — cite at least three independent sources spanning different asset classes,
   geographies, or analytical approaches. No single-source claim is presented as fact.
2. **Leading over lagging** — lead with actionable signals (VIX, CDS spreads, futures premiums,
   PMI flash estimates, tanker flows) before confirming with lagging data (GDP, earnings revisions).
3. **Bias audit** — explicitly state the ideological or commercial orientation of each source and
   flag any potential conflicts of interest.
4. **Confidence labelling** — tag every key assessment as **High / Medium / Low** confidence.
5. **Action items** — close every section with concrete, time-boxed action items or watch levels.

---

## Report structure

Follow this section order exactly. Omit a section only if genuinely no data is available;
state the omission explicitly rather than silently skipping it.

### 1. Situation summary

One paragraph (≤ 120 words). Answer: *What is the single most important development
since the last session, and why does it matter to markets today?*

### 2. Source inventory

List every source consulted before writing the report. For each source, provide:

| Field | Requirement |
| ----- | ----------- |
| Name | Full outlet or data provider name |
| Type | Primary data / news / analysis / government |
| Bias / orientation | e.g. pro-market, state-affiliated, sell-side |
| Reason included | One sentence justifying its relevance |
| Confidence weight | High / Medium / Low |

Perform a bias audit on the collection as a whole:

- Are both risk-on and risk-off perspectives represented?
- Is at least one non-Anglophone source included?
- Is at least one non-Western market perspective included?
- Are sell-side and independent voices balanced?

State the audit result explicitly: **Bias audit: PASS / FAIL — [brief note]**.

### 3. Macro environment

Cover each sub-topic with: current reading → direction → implication → confidence level.

#### Interest rates and central bank policy

- Fed funds futures implied rate path (next two meetings)
- 2-year / 10-year Treasury yield spread (direction and interpretation)
- Key central bank communication since last session

#### Inflation and growth signals

- Latest PMI flash estimates (manufacturing and services, US + key trading partners)
- CPI / PCE revision expectations if applicable
- Credit default swap (CDS) spreads on sovereign and high-yield indices

#### Currency and liquidity

- DXY direction and key levels
- CNH / JPY moves as Asia risk proxies
- Overnight repo and SOFR fixings (anomalies only)

### 4. Equity and futures pre-market

- S&P 500 e-mini futures: premium / discount to fair value, overnight range
- Nasdaq-100 and Russell 2000 futures relative performance
- Key sector ETF pre-market moves (> ±0.5 %) with stated catalyst
- VIX level, direction, and term structure shape (contango / backwardation)
- Put/call ratio (if available for the session)

### 5. Commodities and energy

- WTI and Brent crude: price, overnight move, key driver
- Natural gas (Henry Hub): price and seasonal context
- Gold and silver: risk-on / risk-off read
- Relevant agricultural or industrial metal moves if geopolitically significant
  (connect to chokepoint or supply-chain intelligence from the project's Layer IV sources)

### 6. Geopolitical risk overlay

Cross-reference market signals against the project's intelligence stack:

- Taiwan Strait risk level (🟢 / 🟡 / 🔴) with one-sentence justification
- Active conflict or sanctions developments affecting commodity flows
- Chokepoint status (Strait of Hormuz, Bab-el-Mandeb, Malacca, Taiwan Strait, Panama Canal)
- Manipulation or coordinated inauthentic behaviour (CIB) alerts on market-moving narratives

### 7. Key events today

Ordered table of scheduled events:

| Time (ET) | Event | Expected | Previous | Market impact |
| --------- | ----- | -------- | -------- | ------------- |
| … | … | … | … | High / Medium / Low |

Include: Fed speakers, data releases, earnings (market-cap > $50 bn), geopolitical deadlines.

### 8. Scenarios and action items

State two or three scenarios for today's session:

**Base case** (confidence: ___):
Describe the most probable outcome. List 2–3 specific watch levels or triggers.

**Risk case — upside** (confidence: ___):
What would need to happen. Specific instrument or level.

**Risk case — downside** (confidence: ___):
What would need to happen. Specific instrument or level.

Each scenario must end with a bulleted list of **action items**:

- Action items are specific (instrument, direction, level, time horizon).
- Use imperative mood: *Monitor X for a break above Y before Z.*
- Flag items that depend on unconfirmed information with ⚠️.

### 9. Reliability assessment

Rate the overall report on three dimensions:

| Dimension | Rating (1–5) | Notes |
| --------- | ------------ | ----- |
| Source diversity | … | |
| Data freshness (hours since last data point) | … | |
| Analytical independence from consensus | … | |

State any known data gaps or unverified claims.

### 10. Abbreviations

Define every abbreviation on first use within the report body.
Append a consolidated glossary here for quick reference.

---

## Style and formatting rules

- **Tone**: professional, analytical, direct. No hedging language such as *it seems* or *might possibly*.
  State confidence levels explicitly instead.
- **Numbers**: use commas for thousands (`1,234`); use `%` not `pct`; round to 2 decimal places.
- **Tables**: use the Markdown table format defined in `markdown.instructions.md`.
- **Inline emphasis**: bold (`**`) for key levels and signal words; no italics for data.
- **Citations**: inline after the claim — `(Source: Bloomberg, 2026-03-03)`.
- **No bare URLs** in the report body; use descriptive link text or cite inline.
- **Section length**: aim for 80–150 words per numbered section; the full report should be
  readable in under 10 minutes.
- **Abbreviations**: spell out on first use, then use the short form consistently.

---

## Quality checklist

Run this checklist before finalising any report:

- [ ] Source inventory complete with bias audit result
- [ ] At least one non-Anglophone source cited
- [ ] Every key assessment carries a confidence label
- [ ] VIX and CDS spreads addressed
- [ ] Geopolitical risk overlay completed
- [ ] Each scenario ends with specific, time-boxed action items
- [ ] Abbreviations glossary appended
- [ ] Reliability assessment filled in
- [ ] No single-source claims presented as fact
- [ ] Report fits within a 10-minute read

---

## Disclaimer

This report is for analytical and research purposes only.
It does not constitute financial advice. All market data and geopolitical assessments
carry inherent uncertainty. Confidence levels reflect analytical judgement, not guarantees.
