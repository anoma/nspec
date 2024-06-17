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

## Wikilinks

Wikilinks offer a simple method for citing and referencing other pages in the
documentation without lengthy URLs. **Wikilinks are the preferred method for
linking to other pages** in the documentation, so please use them whenever
possible.

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

The "Reference Page" is the name/key use in the navigation of the documentation,
found in the `nav` attribute of the `mkdocs.yml` file. For example,

```yaml
nav:
  - Home: index.md
  - MyRef X: reference.md
```

provides the following wikilink:

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



