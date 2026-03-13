---
applyTo: "**"
---

# Coding conventions

- **Line length:** 120 characters
- **Quotes:** Double quotes
- **Indentation:** 4 spaces (Python), 2 spaces (YAML, TOML, Markdown)
- **Type hints:** Required on all function signatures
- **Docstrings:** Google style on all public APIs
- **Imports:** isort-ordered, `homemade_intelligence` as first-party
- **Paths:** Use `pathlib.Path`, not `os.path`
- **Tests:** Mirror `tools/` structure in `tests/`; use pytest fixtures and parametrize
- **Validation:** All code must pass `ruff check` and `ruff format --check`
- **Pre-commit:** `pixi run -e dev pre-commit run --all-files`

## Commit messages

Imperative mood, optional category prefix, under 72 characters:

```text
feat: Add Taiwan strait risk module
fix: Correct CDS data source URL
docs: Update intelligence stack to v2.1
ci: Add markdown lint step
test: Add parametrized tests for report generator
```

## Hard constraints

- **Never** commit API keys, secrets, or `.env` files
- **Never** use Simplified Chinese (简体中文) for Taiwan-audience content
- **Never** generate analysis without source citations and confidence levels
- **Never** treat a single-source claim as established fact
- **Never** skip confidence-level annotations on key assessments
- **Never** omit manipulation-awareness checks on time-sensitive analysis
- **Never** present opinion as fact in generated reports
- **Always** use `pixi run` — never bare `pip` or `conda` commands
