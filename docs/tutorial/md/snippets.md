---
icon: material/code-brackets
search:
  exclude: false
todos: false
check_paths: false
---

## Code Snippets

Include excerpts from other files using the Snippet extension detailed here:
[PyMdown Extensions -
Snippets](https://facelessuser.GitHub.io/pymdown-extensions/extensions/snippets/).

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

