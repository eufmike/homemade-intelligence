---
applyTo: "**/*.md"
---

# Markdown Formatting Instructions

Write all Markdown files with clarity, consistency, and portability in mind.
These rules are synthesized from three authoritative references:

- **Google Markdown Style Guide** — <https://google.github.io/styleguide/docguide/style.html>
- **Ciro Santilli's Markdown Style Guide** — <https://cirosantilli.com/markdown-style-guide/>
- **DavidAnson markdownlint rules** — <https://github.com/DavidAnson/markdownlint>

---

## Document Structure

- Begin every file with a single `# H1` title that matches or closely reflects the filename.
- Follow the title with a 1–3 sentence introduction summarising the document's purpose.
- Use `## H2` for top-level sections; never skip heading levels (H1 → H3 is invalid).
- End the file with a single trailing newline character; no blank lines at the end.
- Organise long documents as: `# Title` → introduction → `## Topic` sections → `## See also`.

```markdown
# Document Title

Short introduction paragraph.

## First Topic

Content here.

## See also

- <https://link-to-more-info>
```

---

## Headings

- Use ATX style (`#` prefix) exclusively — never Setext (`===` / `---` underlines).
- Include exactly one space between the `#` characters and the heading text.
- Do **not** add a closing `#` sequence: `# Good` not `# Good #`.
- Do **not** add leading spaces before `#`.
- Surround every heading with one blank line above and below (except at the very top of the file).
- Do **not** add trailing punctuation (`:` or `.`) to headings.
- Do **not** duplicate heading text within the same document — anchor IDs must be unique.
- Use sentence case for headings: capitalise only the first word and proper nouns.
- Keep headings short; write a fuller sentence as the first paragraph under the heading.

```markdown
<!-- Good -->
## Analytical failure modes

<!-- Bad -->
## Analytical Failure Modes:
##Analytical failure modes
```

---

## Line Length and Wrapping

- Target a **120-character** line limit (matches the project's `ruff.toml` convention).
- Exceptions where long lines are acceptable without breaking:
  - URLs and hyperlinks
  - Table rows
  - Fenced code blocks
- Wrap long prose at a natural sentence or clause boundary, not mid-word.
- Never add trailing whitespace. Use a trailing backslash `\` for an intentional hard line-break (rare).

---

## Paragraphs and Blank Lines

- Separate paragraphs with exactly one blank line.
- Do **not** use two or more consecutive blank lines anywhere outside of code blocks.
- Use a single space after sentence-ending punctuation (`.`, `?`, `!`).

---

## Lists

### Unordered lists

- Use the hyphen `-` marker for all unordered list items (not `*` or `+`).
- Add one space after the `-` marker.
- Do **not** add extra indentation before the first level of a list.
- Surround lists with one blank line above and below.
- If every item is a single line, do **not** add blank lines between items.
- If any item spans multiple lines or has sub-paragraphs, add blank lines between **all** items.
- Indent nested lists by 2 spaces.

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

### Ordered lists

- Use `1.` for every item in a long or changeable ordered list (lazy numbering).
- Use sequential numbers (`1.`, `2.`, `3.`) only for short, stable lists.
- Add one space after the `.` marker.

```markdown
1. First step
1. Second step
1. Third step
```

### List item punctuation

- Omit a trailing period when items are sentence fragments that continue a lead-in sentence.
- Add a trailing period when an item starts with an uppercase letter or contains multiple sentences.

---

## Code

### Inline code

- Use backticks for: commands, file paths, field names, version numbers, and technical terms meant to be read literally.
- Do **not** add spaces inside backtick spans: `` `good` `` not `` ` bad ` ``.

### Fenced code blocks

- Use fenced code blocks (triple backticks) for all multi-line code — never indented code blocks.
- Always declare the language immediately after the opening fence.
- Surround fenced blocks with one blank line above and below.
- Do **not** prefix shell commands with `$` unless you are also showing the command's output.

````markdown
```python
def analyse(source: str) -> str:
    return source.strip()
```
````

---

## Emphasis

- **Bold**: double asterisks `**bold**` — not double underscores.
- *Italic*: single asterisks `*italic*` — not single underscores.
- Do **not** use emphasis in place of a heading.
- Do **not** use ALL CAPS for emphasis; use `**bold**` instead.
- Do **not** add spaces inside emphasis markers: `**good**` not `** bad **`.

---

## Links

- Write descriptive link text — never `click here`, `link`, or a bare URL as anchor text.
- Wrap bare URLs in angle brackets when they appear in prose: `<https://example.com>`.
- Use reference-style links when the URL is long enough to disrupt reading flow, or when the same URL is used more than once.
- Place reference definitions at the end of the section (just before the next heading) where first used. Place definitions used in multiple sections at the very end of the file.
- Do **not** use relative `../` paths for links across directories.

```markdown
<!-- Inline link — short URL -->
See the [roadmap](references/roadmap/roadmap.md) for details.

<!-- Reference link — long URL -->
The [Intelligence Stack][intel-stack] documents all source layers.

[intel-stack]: references/knowledgebase/international-situation-intelligence-stack.md
```

---

## Images

- Always include descriptive `alt` text: `![Taiwan Strait map](assets/taiwan-strait.png)`.
- Use images sparingly; prefer text when the content can be conveyed clearly in prose.

---

## Tables

- Surround tables with one blank line above and below.
- Do **not** indent tables.
- Include a leading and trailing pipe `|` on every row.
- Align all pipes vertically.
- Separate the header row from the body with a hyphen row (`|---|`).
- Use reference links inside cells to keep line length manageable.
- Prefer a list with sub-headings over a table when cells would contain long prose.

```markdown
| Header A | Header B |
| -------- | -------- |
| value 1  | value 2  |
| value 3  | value 4  |
```

---

## Blockquotes

- Follow `>` with exactly one space.
- Repeat `>` on every wrapped line of the same quote.
- Do **not** leave blank lines inside a single blockquote block.

```markdown
> This is a blockquote.
> It continues on the next line.
```

---

## Horizontal Rules

- Use `---` (three hyphens, no spaces) for horizontal rules.
- Reserve horizontal rules only to visually mark the end of a major section when no heading follows.

---

## Avoid Inline HTML

- Use standard Markdown syntax wherever possible.
- Inline HTML reduces portability and readability; avoid it except when Markdown genuinely cannot express the required structure.

---

## File Conventions

- File extension: `.md`
- File name: lowercase, hyphen-separated, no leading or trailing hyphens (e.g., `roadmap.md`, `taiwan-strait-risk.md`).
- Encoding: UTF-8.
- End every file with exactly one newline character.
