---
icon: material/language-markdown
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

## Wikilinks

Wikilinks offer a simple method for citing and referencing other pages in the
documentation without lengthy URLs.

```
[[page#anchor|Custom caption]]
```



!!! info "Resolving Wikilinks"

    To resolve a wikilink, 'page' refers to the title found in the `nav` attribute of the markdown file or the `h1` level heading if not listed in `nav`. Only here, we can also use hints, for example.


    ```
    [[hintpath/to:page#anchor|Custom caption]]
    ```

    `hintpath/to` is the path (or prefix) to the file, and `anchor` is the optional anchor within the page. The `Custom caption` is the optional text to display in place of the page title.

### Wikilink Syntax Examples

- Basic wikilink:

  ```markdown
  [[Reference Page]]
  ```

- Anchors are optional:

  ```markdown
  [[Page#anchor]]
  ```

- With a custom caption (optional):

  ```markdown
  [[Page|This link points to a page]]
  ```

## Including Images

Images should be go in the `docs/images` folder.


### Basic Image Syntax

To add an image, apply the following syntax:

```markdown
![Alt Text](logo.svg){: width="200"}
```

#### Displayed Image Example

The syntax above will render the image in your document like so:

![Alt Text](logo.svg){: width="200"}

!!! tip "Enhanced Image Display"

    Use an HTML `<figure>` element with a `<figcaption>` for a refined presentation with captions. Markdown can also be used within the caption:

    ```html
    <figure markdown="1">
      <img src="docs/images/image-name.png" alt="Alt Text">
      <figcaption markdown="span">Image caption text can include *Markdown*!</figcaption>
    </figure>
    ```

## Code Snippets

Include excerpts from other files using the Snippet extension detailed here:
[PyMdown Extensions -
Snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/).

### Excerpt Wrapping Syntax

Enclose the excerpt with the following tags:

```markdown
<!-- Start snippet -->
;--8<-- [start:TAG]
...
;--8<-- [end:TAG]
<!-- End snippet -->
```

### Snippet Inclusion Syntax

To incorporate the excerpt elsewhere, specify its path and tag:

```markdown
;--8<-- "path/to/file.ext:TAG"
```

Following these practices ensures consistency, navigability, and professionalism
in the Anoma documentation.

## Todos

Incorporate todos with the following syntax:


```text
!!! todo

    Content of the todo
```

The above renders as:

!!! todo

    Content of the todo

!!! note

    Be aware that todos are automatically removed from the online version. If you want to keep them, set `todos: True` in the front matter.
