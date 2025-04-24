# Anoma Specs [![deploy](https://github.com/anoma/nspec/actions/workflows/deploy.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/deploy.yml)

<!-- --8<-- [start:all]-- -->

## Getting Started

- **Contribute**: [Tutorial](https://specs.anoma.net/latest/tutorial/index.html)
- **Markdown**: Uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/)

### Setup

1. **Prerequisites**:

   - `uv`: Install via:
   
     ```bash
     # macOS/Linux
     curl -LsSf https://astral.sh/uv/install.sh | sh
     # Windows
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   - `graphviz` for local deployment,

   - `juvix` for local deployment,

     ```bash
     curl --proto '=https' --tlsv1.2 -sSfL https://get.juvix.org | sh
     ```
   - `just` for local development (although you can use `uv run` for most commands)

2. **Setup Commands**:

    ```bash
    just setup-repo
    ```

### Documentation

- **Build**: `just build`
- **Serve Locally**: `just serve`

### Development with Nix

1. **Install Nix**: [Download](https://nixos.org/download/)
2. **Enable Flakes**: [Guide](https://nixos.wiki/wiki/flakes)
3. **Enter Shell**: `nix develop`

<!-- --8<-- [end:all]-- -->
