# Skill: write-file

Assemble all completed report sections into a final Markdown file and save it to the correct
`reports/` sub-folder.

## Input

- All completed report sections (in order)
- Target audience (`english` | `zh-tw` | `zh-tw-elder`)
- Topic slug (lowercase, hyphen-separated, e.g., `premarket-iran-hormuz`)
- Date (`YYYY-MM-DD`)

## Action

Write the file to the correct sub-folder:

| Audience | Output path |
| -------- | ----------- |
| `english` | `reports/en/YYYY-MM-DD-[slug].md` |
| `zh-tw` | `reports/zh-tw/YYYY-MM-DD-[slug].md` |
| `zh-tw-elder` | `reports/zh-tw-elder/YYYY-MM-DD-[slug].md` |

The file must open with this front-matter block:

```markdown
---
date: YYYY-MM-DD
audience: "[english | zh-tw | zh-tw-elder]"
topic: "[topic slug]"
confidence_summary: "[High / Medium / Low] — [one sentence rationale]"
intelligence_stack_version: "2.0"
---
```

## Output

The complete, saved Markdown report file.
