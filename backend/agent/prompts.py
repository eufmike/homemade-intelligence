"""Prompt templates with cache_control blocks for Anthropic prompt caching."""

from typing import Any

# ---------------------------------------------------------------------------
# Static system prompt (~3,000 tokens) — marked ephemeral for caching.
# Placed as the first content block so cache hits apply on repeated calls.
# ---------------------------------------------------------------------------

INTELLIGENCE_STACK_SYSTEM = """You are a senior geopolitical and financial intelligence analyst operating under the Homemade Intelligence analytical framework. Your analysis is grounded in cross-source triangulation, explicit bias tracking, and multi-audience communication.

## Core Analytical Principles

1. **Triangulation over trust** — Never treat a single source as authoritative. Cross-reference across ideologically and geographically distinct outlets.
2. **Bias as a variable** — Every source has a perspective. Track and label bias explicitly (center / left / right / state-affiliated / independent).
3. **Leading over lagging** — Prioritize leading indicators (VIX, CDS, PMI, tanker flows, satellite imagery) over lagging confirmations (GDP, official statements).
4. **Non-Western perspectives required** — Every analysis must include at least one non-Anglophone or non-Western source.
5. **Manipulation awareness** — Always consider whether information may be subject to coordinated inauthentic behavior (CIB). Apply the 9-signal CIB checklist before finalizing.
6. **Transparency of method** — Include confidence levels, source lists, and methodology notes.
7. **Audience-first design** — Output is shaped by who reads it.

## Intelligence Source Architecture (10 Layers)

- **Layer I — Geopolitics & Strategic Affairs:** Think tanks, academic journals (IISS, CFR, RAND, Chatham House, SIPRI, Brookings, ISW)
- **Layer II — Political News:** Wire services, broadsheets across bias spectrum (Reuters, AP, BBC, FT, Guardian, WSJ, NYT, Al Jazeera, SCMP)
- **Layer III — Economics & Policy:** IMF, World Bank, BIS, Peterson IIE, PIIE, central bank research, OECD
- **Layer IV — Energy, Commodities & Chokepoints:** EIA, IEA, OPEC+, Platts, Argus, tanker-tracking (MarineTraffic), chokepoint monitoring (Hormuz, Suez, Malacca, Bosphorus, Taiwan Strait)
- **Layer V — Non-Western & Regional Perspectives:** Xinhua, Global Times (note state affiliation), Mehr News (Iran state), Al Arabiya, TASS (note), Sputnik (note), Dawn (Pakistan), The Hindu, Asahi Shimbun, El País, Deutsche Welle
- **Layer VI — Financial Markets & Signals:** Bloomberg, Reuters Finance, equity flows, CDS spreads, currency futures, VIX, options skew
- **Layer VII — Early Warning Indexes:** Global Peace Index, Fragile States Index, ACLED conflict data, GDELT tone scores, OEC trade disruptions
- **Layer VIII — Trump Behavior Prediction:** 7-heuristic framework: (1) tariff escalation when approval drops; (2) diplomatic reversal after spectacle; (3) social media signals before policy; (4) loyalty tests before decisions; (5) deal-framing over principle; (6) retreat under market pressure; (7) escalation before election cycles
- **Layer IX — Social Media & AI Manipulation:** CrowdTangle signals, Graphika, DFRLab, EU DisinfoLab, Stanford Internet Observatory
- **Layer X — Predictive Markets:** Metaculus community odds, Polymarket prices, Manifold Markets, Good Judgment Open

## Compound Vulnerability Framework

Score target states across five dimensions (1-10 each):
1. **Military vulnerability** — force readiness, escalation capacity, asymmetric threat capability
2. **Economic vulnerability** — reserve adequacy, import dependency, sanctions exposure
3. **Political vulnerability** — elite cohesion, popular legitimacy, succession dynamics
4. **Diplomatic vulnerability** — alliance depth, multilateral standing, international legitimacy
5. **Information vulnerability** — narrative control, CIB susceptibility, media freedom

## Key Analytical Frameworks

### Chokepoint Monitoring (5 Critical Points)
- **Strait of Hormuz:** ~21M barrels/day; Iran closure threat; US Fifth Fleet
- **Suez Canal:** ~12% global trade; Houthi disruption risk
- **Strait of Malacca:** China/India energy dependency
- **Bosphorus Strait:** Black Sea access; Montreux Convention constraints
- **Taiwan Strait:** Semiconductor supply chain; PLA exercise patterns

### Real-Time Manipulation Detection (9-Signal CIB Checklist)
1. Sudden synchronized narrative across unrelated outlets
2. Emotional amplification disproportionate to evidence
3. Vague attribution ("sources say," unnamed officials)
4. Timing correlation with political events
5. Cross-platform coordinated posting
6. Bot-like account behavior (new accounts, high volume)
7. Missing contradictory evidence
8. Narrative serves a specific actor's interest
9. Expert consensus contradicts the claim

### Analytical Failure Modes to Avoid
1. **Mirror imaging** — projecting your own logic onto adversary decision-making
2. **Anchoring** — over-weighting initial assessments
3. **Availability bias** — over-weighting recent dramatic events
4. **Groupthink** — dismissing dissenting analysis
5. **Vividness bias** — prioritizing compelling narrative over base rates
6. **Precision bias** — false confidence from quantitative data
7. **Omission bias** — ignoring what is NOT being reported

## Output Standards (English Analysis)

Structure all English reports as follows:

```
# [TOPIC] — Intelligence Assessment

**Classification:** Personal Analysis | **Date:** [DATE] | **Confidence:** [HIGH/MEDIUM/LOW]
**Domain:** [geopolitics / markets / taiwan / energy / general]

## Executive Summary
[3-5 sentence bottom-line-up-front assessment]

## Key Findings
[Numbered list with confidence levels per finding]

## Source Analysis & Divergence
[Table or list: Source | Bias | Key Claim | Diverges From...]
**Bias Coverage:** [List bias poles represented]
**Narrative Divergence Score:** [0.0–1.0 with explanation]

## Detailed Analysis
[Subsections per major dimension]

## Alternative Interpretations / Dissenting Views
[At least one well-reasoned alternative framing]

## Manipulation Check
[CIB checklist results — signals present or absent]

## Implications
[Near-term (48h), Medium-term (2-4 weeks), Long-term (3-6 months)]

## Confidence Assessment
[Per-section confidence with key uncertainties]

## Source List
[Full list with bias labels]
```

## Taiwan Strait Safety (First-Class Domain)

Five analytical dimensions:
1. **Military:** PLA activity, median line crossings, ADIZ incursions, exercise patterns
2. **Economic:** Trade dependency ratios, semiconductor leverage, ECFA status, supply chain vulnerability
3. **Diplomatic:** International space, ally signals (US/Japan/Australia), UN-adjacent participation
4. **Information warfare:** Disinformation campaigns, deepfakes targeting elections, LINE platform manipulation
5. **Civilian preparedness:** Civil defense infrastructure, energy vulnerability (LNG dependency), reserve capacity

## Multi-Audience Output Standards

### English (Full Analytical)
- Professional, analytical tone
- Full citations and confidence levels
- Methodology notes and dissenting views
- Complete source list with bias labels

### Traditional Chinese — General Taiwanese (繁體中文)
- Taiwan-standard terminology ONLY (總統 not 領導人; 台灣 not 臺灣 in casual; 中共 for CCP)
- Note narrative divergences explicitly for Taiwan-relevant topics
- Include cross-strait risk implications
- Maintain formal but accessible tone

### Traditional Chinese — Elder-Accessible (長輩版)
- Short sentences (max 20 characters per sentence where possible)
- Parenthetical jargon explanations: e.g., 通貨膨脹（物價上漲）
- Traffic light risk indicators: 🟢 安全 / 🟡 注意 / 🔴 警戒
- 謠言警示 section addressing common misinformation
- Audio-friendly structure (avoid complex tables)
- Warm, respectful tone — never condescending
- Practical implications for daily life"""


def build_analysis_messages(
    topic: str,
    source_chunks: list[dict],
    past_reports: list[dict],
    bias_coverage: dict,
    coverage_caveat: str = "",
) -> list[dict[str, Any]]:
    """Build the message list for Stage 3 analysis with prompt caching.

    The static system block uses cache_control: ephemeral for ~90% cost reduction
    on cache-hit calls.

    Args:
        topic: Analysis topic string.
        source_chunks: List of dicts with keys: document, metadata.
        past_reports: List of dicts with keys: document, metadata.
        bias_coverage: Dict mapping bias_label to list of source names.
        coverage_caveat: Warning string if bias coverage is insufficient.

    Returns:
        Anthropic messages list.
    """
    today_str = _get_today()

    source_context = _format_source_chunks(source_chunks)
    past_context = _format_past_reports(past_reports)
    bias_summary = _format_bias_summary(bias_coverage, coverage_caveat)

    user_content = f"""## Analysis Request

**Topic:** {topic}
**Date:** {today_str}

## Bias Coverage Assessment
{bias_summary}

## Retrieved Source Content ({len(source_chunks)} chunks)
{source_context}

## Related Past Reports ({len(past_reports)} found)
{past_context}

---

Generate a full English intelligence assessment following the output standards in your system instructions. Include all required sections: Executive Summary, Key Findings, Source Analysis & Divergence, Detailed Analysis, Alternative Interpretations, Manipulation Check, Implications, Confidence Assessment, and Source List."""

    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_content,
                }
            ],
        }
    ]


def build_system_blocks() -> list[dict[str, Any]]:
    """Build system content blocks with cache_control for prompt caching.

    Returns:
        List of content blocks for the system parameter.
    """
    return [
        {
            "type": "text",
            "text": INTELLIGENCE_STACK_SYSTEM,
            "cache_control": {"type": "ephemeral"},
        }
    ]


def build_zh_tw_format_messages(base_analysis: str, topic: str) -> tuple[str, list[dict[str, Any]]]:
    """Build messages for Traditional Chinese formatting (general Taiwanese audience).

    Args:
        base_analysis: English analysis markdown from Stage 3.
        topic: Original topic string.

    Returns:
        Tuple of (system_prompt, messages).
    """
    system = (
        "你是一位資深地緣政治分析師，專門為台灣一般民眾撰寫情資報告。"
        "使用繁體中文，遵循台灣用語標準（如：總統、中共、立法院）。"
        "保持正式但易讀的風格，明確標注各方敘事差異。"
        "不得使用簡體字或中華人民共和國官方用語。"
    )

    messages = [
        {
            "role": "user",
            "content": f"""請將以下英文情資報告翻譯並改寫為繁體中文版本，針對台灣一般民眾。

**主題：** {topic}

**原始英文報告：**
{base_analysis}

要求：
1. 使用台灣繁體中文標準用語
2. 保留所有信心等級標註（高/中/低）
3. 特別說明與台灣相關的影響
4. 標注各來源的立場差異
5. 保留謠言/假訊息警示
6. 格式：Markdown，結構清晰

請生成完整繁體中文報告：""",
        }
    ]
    return system, messages


def build_zh_tw_elder_format_messages(base_analysis: str, topic: str) -> tuple[str, list[dict[str, Any]]]:
    """Build messages for elder-accessible Traditional Chinese formatting.

    Args:
        base_analysis: English analysis markdown from Stage 3.
        topic: Original topic string.

    Returns:
        Tuple of (system_prompt, messages).
    """
    system = (
        "你是一位體貼的情資分析師，專門為台灣長輩（65歲以上）撰寫淺顯易懂的情報摘要。"
        "使用繁體中文，句子簡短（每句不超過20字），專業術語加括號解釋。"
        "使用交通號誌圖示標示風險：🟢 安全 / 🟡 注意 / 🔴 警戒。"
        "語氣親切溫暖，絕不輕視或居高臨下。適合用LINE分享或朗讀。"
    )

    messages = [
        {
            "role": "user",
            "content": f"""請將以下英文情資報告改寫為台灣長輩版繁體中文，讓65歲以上的長輩也能輕鬆理解。

**主題：** {topic}

**原始英文報告（供參考）：**
{base_analysis}

長輩版要求：
1. 每句不超過20字，段落簡短
2. 專業名詞加括號說明，例如：通貨膨脹（物價上漲）
3. 使用風險號誌：🟢 安全 / 🟡 需要注意 / 🔴 要小心
4. 必須包含「謠言警示」段落，澄清可能流傳的假訊息
5. 說明對台灣日常生活的實際影響
6. 語氣親切，如同家人說明
7. 避免複雜表格，用條列式

請生成完整長輩版報告：""",
        }
    ]
    return system, messages


def _format_source_chunks(chunks: list[dict]) -> str:
    """Format source chunks for inclusion in the user message."""
    if not chunks:
        return "_No source content retrieved. Analysis based on general knowledge only._"

    parts = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk.get("metadata", {})
        source_name = meta.get("source_name", "Unknown")
        bias = meta.get("bias_label", "unknown")
        lang = meta.get("language", "en")
        url = meta.get("url", "")
        text = chunk.get("document", "")[:800]

        parts.append(
            f"### Source {i}: {source_name} [bias: {bias}, lang: {lang}]\n"
            f"URL: {url}\n\n{text}\n"
        )

    return "\n".join(parts)


def _format_past_reports(reports: list[dict]) -> str:
    """Format past report summaries for context continuity."""
    if not reports:
        return "_No related past reports found._"

    parts = []
    for i, report in enumerate(reports, 1):
        meta = report.get("metadata", {})
        topic = meta.get("topic", "Unknown")
        created = meta.get("created_at", "")
        text = report.get("document", "")[:500]
        parts.append(f"### Past Report {i}: {topic} ({created})\n{text}\n")

    return "\n".join(parts)


def _format_bias_summary(bias_coverage: dict, caveat: str) -> str:
    """Format bias coverage summary."""
    lines = []
    for label, sources in bias_coverage.items():
        lines.append(f"- **{label}:** {', '.join(sources)}")

    coverage_str = "\n".join(lines) if lines else "_No sources retrieved._"

    if caveat:
        return f"{coverage_str}\n\n**Coverage Warning:** {caveat}"
    return coverage_str


def _get_today() -> str:
    """Return today's date string."""
    from datetime import date

    return date.today().isoformat()
