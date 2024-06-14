---
icon: octicons/markdown-16
search:
  exclude: false
tags:
  - wikilinks
  - images
  - snippets
todos: False
---

# Markdown Basics for Anoma Documentation

Our theme and main Markdown reference is [Material for
MkDocs](https://squidfunk.github.io/mkdocs-material/reference). You may use
anything found in this reference, including all possible Markdown extensions.

This guide provides an overview of the key markdown features we use in the
documentation. Please note that this guide is a work-in-progress.

## Front Matter

Each markdown file should begin with a front matter section. It typically
includes metadata such as `icon`, `tags`, `categories`. For more examples, refer
to other files within the documentation. For example, the icons name can be found
[here](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/?h=icon).

### Example Front Matter

```markdown
---
icon: material/auto-download
search:
  exclude: false
  boost: 3
tags:
  - GitHub
  - python
  - MkDocs
  - Makefile
categories:
  - tutorial
---
```

!!! warning

    Any new markdown file added to the `docs` directory must, in principle, have
    an entry in the `mkdocs.yml` file, precisely in the `nav` section. 

    The filename may be relevant depending on where it is placed in the
    navigation. For example, any file intended to be the landing page of a section, say Section X, must be named `index.md` and placed right below the `Section X` item. Children of `Section X` do not need to follow any specific naming convention. 

    ```
    ...
    - Section X:
        - ./path-to/index.md
        - NameRef Child1 : ./path-to/child1.md
        - NameRef Child2 : ./path-to/child2.md
    ```
