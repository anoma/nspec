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