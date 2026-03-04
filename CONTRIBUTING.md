# Contributing

> **Homemade Intelligence** is a personal intelligence project. Contributions are not actively solicited, but the methodology and architecture are open for reference.

## If You'd Like to Contribute

1. **Fork** the repository.
2. **Create a feature branch** from `main`.
3. **Follow the project conventions**:
   - Python code: formatted with [Ruff](https://docs.astral.sh/ruff/)
   - Markdown: use consistent heading hierarchy, 2-space indentation
   - Commit messages: clear, imperative mood (e.g., "Add Taiwan strait risk module")
4. **Open a pull request** with a clear description of the change.

## Development Setup

```bash
# Install pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Set up the dev environment
pixi install -e dev

# Install pre-commit hooks
pixi run -e dev pre-commit install
```

## Reporting Issues

Feel free to open an issue for:

- Factual inaccuracies in source ratings or categorizations
- Suggestions for new intelligence sources
- Technical bugs in tooling or automation

---

*Thank you for your interest in this project.*
