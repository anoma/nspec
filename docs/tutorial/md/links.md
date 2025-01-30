---
icon: octicons/link-16
search:
  exclude: false
tags:
  - tutorial
  - conventions
---

# Support for Wiki Links

Wiki links offer a simple method for citing and referencing other pages in the
documentation without lengthy URLs. **Wiki links are the preferred method for
linking to other pages** in the documentation, so please use them whenever
possible.

## Basic Syntax

The basic syntax for a wiki link is:

```
[[page]]
```

Where:

- `page` is the title of the target page

## Full Syntax

The full syntax for a wiki link is:
```markdown title="Wiki Link Syntax"
  [[hintpath/to:page#anchor|Custom caption]]
```

When resolving a wiki link, the system follows these rules:

### Page Title

(**Mandatory**) The 'page' in a wiki link refers to the title
specified in the `nav` attribute of the `mkdocs.yml` file. For example,

  ```yaml title="mkdocs.yml"
  nav:
    - Home: index.md
    - MyRef X: reference.md
  ```

provides the following wiki link:

```markdown
[[MyRef X]]
```


### Path Hints

(**Optional**) You can use path hints to specify the location of the file. The syntax is:

```markdown title="Path Hints"
[[hintpath/to:page]]
```

Where:

- `hintpath/to` is the path (or prefix) to the file
- `page` is the title of the target page

### Anchors

(**Optional**) Use anchors to link to specific sections within a page. If the
page does not have an anchor, the link would render as the caption provided,
and you'll find a warning in the build process.

```markdown title="Anchors"
[[page#anchor]]
```

Where:

- `page` is the title of the target page
- `anchor` is a specific section within the page


### Custom captions

(**Optional**) Provide custom text to display for the link instead of the page title.

```markdown title="Custom Captions"
[[page#anchor|Custom caption]]
```

Where:

- `page` is the title of the target page
- `anchor` is a specific section within the page

Captions can include icons, for example:

=== "Markdown"

    ```markdown
    [[Home | :material-link: this is a caption with an icon ]]
    ```

=== "Preview"

    [[Home | :material-link: this is a caption with an icon ]]

