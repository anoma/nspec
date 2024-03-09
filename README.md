# Anoma Specs [![anoma-spec-ci](https://github.com/anoma/nspec/actions/workflows/ci.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/ci.yml)

> [!IMPORTANT] This repository is under construction. The content is not ready
> for active use. It requires to install the Juvix compiler from source if you
> intend to introduce any datatype or function in the code examples.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. If this is not your goal,
you can edit the files Markdown directly on GitHub, the CI/CD pipeline will
automatically build and deploy the website.

### Prerequisites

- Python 3.6 or higher + `pip`: You can install it from [here](https://www.python.org/downloads/).
- Python packages including [MkDocs](https://www.mkdocs.org/), and [Material
  for MkDocs](https://squidfunk.github.io/mkdocs-material/).

- We recomend to install Juvix from [source](https://github.com/anoma/juvix). Otherwise, you can install it following the steps from [our documentation](https://docs.juvix.org/).

### Installing

1. Clone the repository
   
    ```bash
    git clone http://github.com/anoma/nspec
    ```

2. Install the required packages
   
    ```bash
    pip3 install -r requirements.txt
    ```

## Building the Website

Once you have everything set up, you can build the website using MkDocs. Run the
following command in your terminal:

```bash
mkdocs serve
```

## Serving the Website Locally

Once you have built the website, you can serve it locally to see your changes in
real time. Run the following command in your terminal:

```bash
mkdocs serve
```