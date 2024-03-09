# Anoma Specs [![anoma-spec-ci](https://github.com/anoma/nspec/actions/workflows/ci.yml/badge.svg)](https://github.com/anoma/nspec/actions/workflows/ci.yml)

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. If this is not your goal,
you can edit the files Markdown directly on GitHub, the CI/CD pipeline will
automatically build and deploy the website.

### Prerequisites

- Python 3.6 or higher + `pip`: You can install it from [here](https://www.python.org/downloads/).
- Python packages including [MkDocs](https://www.mkdocs.org/), and [Material
  for MkDocs](https://squidfunk.github.io/mkdocs-material/).

- Juvix (optional)

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