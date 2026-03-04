# Skill: define-terms

Produce a definition for every abbreviation or technical term in the given text, using the
Intelligence Stack Section 0 Glossary as the authoritative source.

## Input

Any text containing abbreviations or technical terms.

## Action

For each term:

1. Look it up in Intelligence Stack Section 0 Glossary.
1. If found, use that definition verbatim.
1. If absent from the Glossary, write your own definition and mark it *(local definition)*.

Inline format (for use in prose): `TERM (Full Name — definition)`

## Output

One definition table row per term:

`| **TERM** | Full name | Definition |`

Collect all rows into the **Abbreviations and key terms** section of the report.
