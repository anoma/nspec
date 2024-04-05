# Anoma Specs [![anoma-spec-ci](https://github.com/anoma/nspec/actions/workflows/ci.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/ci.yml)

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
(+v0.6.1)](https://docs.juvix.org/), and and if you want to make sure that the
code examples are correct, you must have Juvix installed on your machine. One
way to do this is to install the Juvix plugin for VsCode from [the
marketplace](https://marketplace.visualstudio.com/items?itemName=heliax.juvix-mode).

### Prerequisites

The following are the prerequisites to build the website locally:

- Python 3.6 or higher + `pip`: You can install it from [here](https://www.python.org/downloads/).
- To deploy the website locally, you would need to install `graphviz` to render *dot* files.
- As mentioned, we recomend to install Juvix.

### Installing

1. Clone the repository

    ```bash
    git clone http://github.com/anoma/nspec
    ```

2. Create a virtual environment

    ```bash
    python3 -m venv env
    ```

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
    source env/bin/activate.zsh
    ```

3. Install the required packages

    ```bash
    pip3 install -r requirements.txt
    ```

4. Make sure that everything is working by building the website

    ```bash
    mkdocs build
    ```

  Here, you should see the website being built in the `site` directory.
  Some warnings and info messages are expected, but if you see any error, please
  open an issue.

5. To serve the website locally, run the following command:

    ```bash
    mkdocs serve
    ```

    Alternatively, you can run the following command to serve the website without
    only error messages:

    ```bash
    MKDOCSFLAGS=--quiet make serve
    ```

6. Accessing Material Insider Features

For access to [Material for MkDocs
Insiders](https://squidfunk.github.io/mkdocs-material/reference/) features,
contact us to obtain a token. However, you can still build the website without
these features. So, to use insiders features (you require to set the `GH_TOKEN`),

```bash
pip3 install -r requirements.insiders.txt
```

and run, for example:

```bash
MKDOCSFLAGS=--quiet MKDOCSCONFIG=mkdocs.insiders.yml make serve
```
