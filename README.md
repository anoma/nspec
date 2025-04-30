# Anoma Specs [![deploy](https://github.com/anoma/nspec/actions/workflows/deploy.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/deploy.yml)

<!-- --8<-- [start:all]-- -->

## Getting Started

Welcome to the Anoma Specs repository! This project uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/) for documentation and is designed for easy contribution and local development.

- **Latest Specs**: [https://specs.anoma.net/latest/](https://specs.anoma.net/latest/)

---

## Quick Start

### 1. Prerequisites

Make sure you have the following tools installed:

- **uv** (Python package/dependency manager)
  - macOS/Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  - Windows:
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
  - Or via Homebrew:
    ```bash
    brew install uv
    ```

- **graphviz** (for local documentation deployment)

- **juvix** (for typechecking and specs development)
  ```bash
  curl --proto '=https' --tlsv1.2 -sSfL https://get.juvix.org | sh
  ```

- **just** (a simple command runner, replacement for Make)
  - Install via your [package manager](https://github.com/casey/just?tab=readme-ov-file#cross-platform).

---

### 2. Installation

Choose one of the following:

- With **uv**:
  ```bash
  uv sync
  ```
- With **just**:
  ```bash
  just sync
  ```
- With **pip**:
  ```bash
  pip install -r requirements.txt
  ```

---

### 3. Common Commands

You can use either `just` or `uv run` for most tasks. Below are the most common commands:

#### Dependency Management

| Task                        | Command                                        | Command (just)      |
|-----------------------------|------------------------------------------------|---------------------|
| Synchronize dependencies    | `uv sync`                                      | `just sync`         |
| Run all pre-commit checks   | `uv run pre-commit -- run --all-files`         | `just check`        |
| Typecheck the code          | `juvix typecheck docs/everything.juvix.md`     | `just juvix-check`  |

#### Development Tools

- **Install pre-commit hooks** (for specs writers only):
  ```bash
  uv run pre-commit -- install --install-hooks
  ```
  or
  ```bash
  just install-hooks
  ```

- **Install development tools**:
  ```bash
  uv tool install pre-commit
  uv tool install commitizen
  ```
  or
  ```bash
  just install-tools
  ```

#### Documentation

| Task                        | Command                                        | Command (just)      |
|-----------------------------|------------------------------------------------|---------------------|
| Build documentation         | `uv run mkdocs build --config-file mkdocs.yml` | `just build`        |
| Serve documentation locally | `uv run mkdocs serve --config-file mkdocs.yml` | `just serve`        |

#### Git Operations

| Task                        | Command                                        | Command (just)      |
|-----------------------------|------------------------------------------------|---------------------|
| Commit using commitizen     | `uv run cz commit`                             | `just commit`       |
| Commit skipping hooks       | `git commit --no-verify -m "<msg>"`            | `just commit-skip`  |
| Amend commit (skip hooks)   | `git commit --amend --no-verify`               | `just commit-amend` |
| Amend using commitizen      | `uv run cz commit --amend`                     | `just cz-amend`     |

If you have installed the pre-commit hooks (which is recommended), but need to
make a commit or push changes without running the hooks (for example, when
working on a branch or PR), you can use the `--no-verify` flag as shown in the
table above. The Commitizen is a tool to help you write better commit messages.

---

### 4. Short Reference

- **Install**: `uv sync` or `pip install -r requirements.txt`
- **Build**: `just build` or `uv run mkdocs build`
- **Serve Locally**: `just serve` or `uv run mkdocs serve`

---

## Development with Nix

If you use [Nix](https://nixos.org/download/):

1. **Install Nix**: [Download](https://nixos.org/download/)
2. **Enable Flakes**: [Guide](https://nixos.wiki/wiki/flakes)
3. **Enter Development Shell**:
   ```bash
   nix develop
   ```

<!-- --8<-- [end:all]-- -->
