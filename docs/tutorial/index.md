---
icon: material/format-textbox
search:
  exclude: false
tags:
  - tutorial
---

# Tutorials and guidelines for writing Anoma Specification documentation

## Global principles and guidelines

### Principles

Clarity

: Make every page clear and concise.
Footnotes may be used to add context.
Additional notes that exceed a paragraph may deserve to be put into a separate file
(and [[Write Markdown|thus]] will appear in the navigation bar).

Don't repeat yourself!

: Do not paste any copied material.
Instead, include the material, e.g., via [[Include code snippets|snippeting]].
The only exception is material for which there is no established method for inclusion;
in this case,
include the material inside a todo note `!!! todo "unrepeat this"`,
paired with a reference to its source.

Consistency

: Terms from the glossary must be used consistently throughout the specification.
Where applicable, adhere to naming schemes.


Style

: Conform to style guides, unless this would lead to inconsistency.

Citations

: Use [[Citing in Markdown|citations]] to refer to articles, books, and similar publications.

### Guidelines

Accessibility

: The specification should be accessible to its intended readership,
which should encompass at least the members of the Anoma engineering team.

Internal and external linking

: If you have a link for something, please use it.
Chances are that it improves accessibility and moreover
it helps discover inconsistencies.
Use wikilinks for internal links and
URL links (`[target](URL)`) only for external material
(or if wikilinks do not work as expected).

Implementability

: The specification should keep design decisions to a minimum,
but design decisions that are left to the potential implementer _on purpose_
should be discussed in footnotes or notes.


## List of tutorials and guidelines

The following tutorials and guidelines are available. If you want to contribute
to this website in anyhow, ask for access to the
**[anoma/nspec](http://github.com/anoma/nspec)** repository, and submit a pull
request with your changes.

- [[Prepare working environment]]
- [[Use Git and GitHub]]
- [[Updating the changelog]]
- [[Versioning]]
- [[File naming conventions]]
- [[Write Markdown]]
- [[Headers and other Markdown formatting conventions]]
- [[Use Wiki style links]]
- [[Include images in Markdown]]
- [[Include code snippets]]
- [[Add Juvix code for specification]]
- [[Add pending tasks with Todos admonition]]
- [[Add literature references]]
- [[Add diffs for versioning]]
