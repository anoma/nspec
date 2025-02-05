# Anoma Specs [![deploy](https://github.com/anoma/nspec/actions/workflows/deploy.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/deploy.yml)
<!-- --8<-- [start:all]-- -->

## Getting Started

> **Note**
> All you need to know to contribute to the documentation is in:
> - https://specs.anoma.net/latest/tutorial/index.html

We use Markdown with extensions according to the [Material for MkDocs reference](https://squidfunk.github.io/mkdocs-material/reference/).

To set up the project for development and testing on your local machine, please follow these steps.
Alternatively, you can edit the Markdown files directly on GitHub, open a pull request (PR), and
the CI/CD pipeline will manage the build and deployment process after the changes are merged.

For `.juvix.md` files, which include Juvix code examples, ensure that Juvix is
installed. You can install the Juvix plugin for VS Code
from [the
marketplace](https://marketplace.visualstudio.com/items?itemName=heliax.juvix-mode).

### Installing

1. Install prerequisites

  The following are the prerequisites to build the website locally:

  - Python or higher which includes `pip`

  - Poetry: You can install by running `pip install poetry`.

  - To deploy the website locally, you would need to install `graphviz` to
    generate SVG files for *dot* files and `juvix` to render the Juvix code
    examples.

2. Install the required packages (preferably in the virtual environment) using Poetry:

    ```bash
    poetry install
    ```

### Building and serving the website

1. To generate the website in the `site/` directory, run:

    ```bash
    poetry run mkdocs build
    ```

2. To serve the website locally, run the following command:

    ```bash
    poetry run mkdocs serve
    ```

    Take into account that this web server will automatically reload the website
    when you make any changes to the files, and it is slow.


### Development shell with Nix

1. Install Nix: https://nixos.org/download/

2. Enable Nix Flakes: https://nixos.wiki/wiki/flakes

3. Enter development shell:

    ```bash
    nix develop
    ```

<!-- --8<-- [end:all]-- -->
