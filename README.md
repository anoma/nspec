# Anoma Specs [![anoma-spec-ci](https://github.com/anoma/nspec/actions/workflows/ci.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/ci.yml)

<!-- --8<-- [start:all]-- -->

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. If this is not your goal,
you can edit the files Markdown directly on GitHub, open a PR with the changes,
and the CI/CD pipeline will automatically build and deploy the website, once
the PR is merged.

To write the content, we use Markdown with some extensions as described in the
[Material for MkDocs's reference](https://squidfunk.github.io/mkdocs-material/reference/).

In addition, we support the use of Juvix code examples in the files with the
`.juvix.md` extension. These files are rendered using [Juvix
(+v0.6.1)](https://docs.juvix.org/), and if you want to make sure that the
code examples are correct, you must have Juvix installed on your machine. One
way to do this is to install the Juvix plugin for VS Code from [the
marketplace](https://marketplace.visualstudio.com/items?itemName=heliax.juvix-mode).

### Installing with Python

1. Install prerequisites

    The following are the prerequisites to build the website locally:

    - Python 3.9 or higher + `pip`: You can install it from [here](https://www.python.org/downloads/).

    - To deploy the website locally, you would need to install `graphviz` to generate SVG files for *dot* files.

    - As mentioned, we would need `juvix` to render the Juvix code examples.

2. Create a virtual environment

    ```bash
    python3 -m venv env
    ```

3. Activate the virtual environment

    Make sure to activate the virtual environment before proceeding. If you are using
    `bash`, you can do this by running:

    ```bash
    source env/bin/activate
    ```

    On `fish`, you can do this by running:

    ```bash
    source env/bin/activate.fish
    ```

    On `zsh`, you can do this by running:

    ```bash
    source env/bin/activate
    ```

4. Install the required packages (preferably in the virtual environment) using Poetry:


    ```bash
    pip3 install poetry
    poetry install
    ```

### Development shell with Nix

1. Install Nix: https://nixos.org/download/

2. Enable Nix Flakes: https://nixos.wiki/wiki/flakes

3. Enter development shell:

    ```bash
    nix develop
    ```

### Building the specs

1. To generate the website in the `site/` directory, run:

    ```bash
    mkdocs build
    ```

2. To serve the website locally, run the following command:

    ```bash
    mkdocs serve
    ```

    Take into account that this web server will automatically reload the website
    when you make changes to the files, and it is not especially fast.

<details> <summary> Builds with quiet mode </summary>

By default, both `make build` or `make serve` are not configured to use the
`--quiet` flag that suppresses the output of the build process, including
warnings and errors. If you don't see all this output, you can run:

```bash
MKDOCSFLAGS=--quiet make build
```

```bash
make test-build
```

</details>

<!-- --8<-- [end:all]-- -->
