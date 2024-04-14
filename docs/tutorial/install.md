---
icon: material/auto-download
tags:
    - GitHub
    - python
    - MkDocs
    - Makefile
---

# Install

--8<-- "./README.md:all"

# Build and serve this tutorial

The files of this tutorial are in the `docs/tutorial` directory. The
`tutorial.yml` file is the configuration file for this tutorial website.

```
mkdocs serve --config-file tutorial.yml
```

When merged with the main documentation, the tutorial will be available at
`http://anoma.github.io/nspec/tutorial/`. For pull requests, the tutorial will
be available at `http://anoma.github.io/nspec/pull-<PR_NUMBER>/tutorial/`.