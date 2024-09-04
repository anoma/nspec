---
icon: octicons/link-16
search:
  exclude: false
tags:
  - wikilinks
  - images
  - snippets
todos: False
---

# Support for Wiki Links

Wiki links offer a simple method for citing and referencing other pages in the
documentation without lengthy URLs. **Wiki links are the preferred method for
linking to other pages** in the documentation, so please use them whenever
possible.

```
[[page#anchor|Custom caption]]
```


!!! info "Resolving Wiki links"

    To resolve a wikilink, 'page' refers to the title found in the `nav` attribute of the markdown file or the `h1` level heading if not listed in `nav`. Only here, we can also use hints, for example.


    ```
    [[hintpath/to:page#anchor|Custom caption]]
    ```

    `hintpath/to` is the path (or prefix) to the file, and `anchor` is the optional anchor within the page. The `Custom caption` is the optional text to display in place of the page title.

## Syntax examples

- Basic wiki link:

  ```markdown
  [[Reference Page]]
  ```

The "Reference Page" is the name/key use in the navigation of the documentation,
found in the `nav` attribute of the `mkdocs.yml` file. For example,

```yaml
nav:
  - Home: index.md
  - MyRef X: reference.md
```

provides the following wiki link:

```markdown
[[MyRef X]]
```


- Anchors are optional:

  ```markdown
  [[Page#anchor]]
  ```

- With a custom caption (optional):

  ```markdown
  [[Page|This link points to a page]]
  ```


## List of wiki-style links per Page

By default, the build process will generate a list of all wiki-style links per
page. This list is displayed at the bottom of the page, and it is useful for
identifying broken links or pages that are not linked to from other pages.

To disable this feature, set the `list_wikilinks` option to `false` in the front
matter of the page.

```yaml
list_wikilinks: false
```

Additionally, you could see a mermaid graph of the links by setting the
`graph_wikilinks` option to `true` in the front matter of the page. This,
however, may render graphs that are too large to be useful. Thus, it is
set to `false` by default.

```yaml
graph_wikilinks: true
```
