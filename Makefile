# =============================================================================
# Makefile — convenience shortcuts for common tasks
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install dev lint format test pre-commit clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install default pixi environment
	pixi install

dev: ## Install dev environment with linting & testing tools
	pixi install -e dev
	pixi run -e dev pre-commit install

lint: ## Run ruff linter
	pixi run -e dev ruff check .

format: ## Run ruff formatter
	pixi run -e dev ruff format .

test: ## Run pytest
	pixi run -e dev pytest tests/ -v

pre-commit: ## Run all pre-commit hooks
	pixi run -e dev pre-commit run --all-files

clean: ## Remove caches and build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/
