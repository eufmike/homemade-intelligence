# Skill: write-rumour-alert

Write the 謠言警示 (Rumour alert) section addressing active misinformation narratives in
Taiwan-facing media.

## Input

Active misinformation narratives circulating in Taiwan-facing media.

## Action

Address the top 1–3 active narratives.
For each narrative, state:

1. The false or unverified claim
1. Why it is false or unverified
1. The credible source that contradicts it
1. The recommended response for the target audience

Use the correct language and tone for the target audience:

| Audience | Language | Tone |
| -------- | -------- | ---- |
| `zh-tw` | Traditional Chinese (繁體中文) | Informative, balanced |
| `zh-tw-elder` | Traditional Chinese (simplified vocabulary) | Warm, respectful; include 🟢 / 🟡 / 🔴 traffic light indicators |

## Constraint

Required for `zh-tw` and `zh-tw-elder` audiences only.
For `english` audience, output:
`Not applicable — 謠言警示 is generated for Taiwan-audience reports only.`

## Output

The 謠言警示 section in the correct audience language and tone.
