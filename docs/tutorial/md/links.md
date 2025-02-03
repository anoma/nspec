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

## Basic Syntax

For a simple link, we only need

- a pair of opening brackets `[‍[`;
- a page title, e.g., `page title with spaces`; and
- a pair of closing brackets `]‍]`.

In short, the basic syntax for a wiki link is:

=== "Markdown pattern description"

    ```markdown
    [‍[page title with spaces]‍]
    ```

=== "Markdown example"

    ```markdown
    [‍[Support for Wiki Links‍]]
    ```

=== "Example Preview"
    
    [[Support for Wiki Links]]


## Full Syntax

### test

=== "Example Preview"
    
    [[Support for Wiki Links#full-syntax]]

=== "Example Preview two"
    
    [[Support for Wiki Links#Full-Syntax]]

=== "Example Preview three"
    
    [[Support for Wiki Links#full syntax]]

=== "Example Preview four"
    
    [[Support for Wiki Links#Full Syntax]]



### real


The full syntax for a wiki link allows to give extra information,
e.g., an _anchor_ to a sub-section, and a custom caption
to adapt to the encompassing prose.

=== "Markdown pattern description"

    ```markdown title="Wiki Link: Full Syntax"
    [‍[hintpath/to:page title with spaces#lowercase-anchor-using-hyphens|Custom caption]‍]
    ```

=== "maybe Working preview"

    ```markdown
    [[Support for Wiki Links‍#full-syntax|foo bar fizz]]
    ```

=== "Example preview"

    ```markdown
    [[docs/tutorial/md:Support for Wiki Links‍#full-syntax|foo bar fizz]]
    ```

=== "Example preview two"

    ```markdown
    [[./docs/tutorial/md:Support for Wiki Links‍#full-syntax|foo bar fizz]]
    ```

=== "Example preview three"

    ```markdown
    [[./docs/tutorial/md/:Support for Wiki Links‍#full-syntax|foo bar fizz]]
    ```

=== "Example preview three"

    ```markdown
    [[./docs/tutorial/md/to:Support for Wiki Links‍#full-syntax|foo bar fizz]]
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
[‍[MyRef X]‍]
```


### Path Hints

(**Optional**) You can use path hints to specify the location of the file. The syntax is:

```markdown title="Path Hints"
[‍[hintpath/to:page title with spaces]‍]
```

Where:

- `hintpath/to` is the path (or prefix) to the file
- `page title with spaces` is the title of the target page

### Anchors

(**Optional**) Use anchors to link to specific sections within a page. If the
page does not have an anchor, the link would render as the caption provided,
and you'll find a warning in the build process.

```markdown title="Anchors"
[‍[page title with spaces#lowercase-anchor-using-hyphens]‍]
```

Where:

- `page title with spaces` is the title of the target page
- `lowercase-anchor-using-hyphens` is a specific section within the page


### Custom captions

(**Optional**) Provide custom text to display for the link instead of the page title.

```markdown title="Custom Captions"
[‍[page title with spaces#lowercase-anchor-using-hyphens|Custom caption]‍]
```

Where:

- `page title with spaces` is the title of the target page
- `lowercase-anchor-using-hyphens` is a specific section within the page

Captions can include icons, for example:

=== "Markdown"

    ```markdown
    [‍[Home | :material-link: this is a caption with an icon ]‍]
    ```

=== "Preview"

    [[Home | :material-link: this is a caption with an icon ]]


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
