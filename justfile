# ===== Setup and Environment =====

# Set up the repository with all dependencies and hooks
setup-repo:
	uv sync
	uv run just install-hooks
	uv run just install-tools

# Install pre-commit hooks
install-hooks:
	uv run pre-commit install --install-hooks

# Install development tools
install-tools:
	uv sync
	uv tool install pre-commit
	uv tool install commitizen

# ===== Dependency Management =====

# Synchronize dependencies
sync:
	uv sync

# Lock dependencies
lock:
	uv lock

# Export dependencies
export:
	uv export

# Run all pre-commit checks
check:
	uv run pre-commit run --all-files

# Typecheck the code
juvix-check:
	juvix typecheck docs/everything.juvix.md

# ===== Documentation =====

# Build documentation
build:
	uv run mkdocs build

# Serve documentation locally
serve:
	uv run mkdocs serve

# Deploy documentation to GitHub Pages
deploy:
	uv run mkdocs gh-deploy --force

# ===== Git Operations =====

# Commit using commitizen
commit:
	uv run cz commit

# Commit skipping pre-commit hooks
commit-skip m:
	git commit --no-verify -m "{{m}}"

# Amend skipping pre-commit hooks
amend:
	git commit --amend --no-verify

# Amend using commitizen
amend-cz:
	uv run cz commit --amend