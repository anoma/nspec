---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- template
---

<!-- Do not delete the following link since it contains the base document for this page: https://raw.githubusercontent.com/anoma/nspec/c61eb3d4e2733ad5712155beabe5e80a6aaff59d/docs/tutorial/engines/template/engine_environment.juvix.md?token=GHSAT0AAAAAACVOLA35IMRBAMF7POUITPSGZWX6GJQ
-->

# Engine "Environment" Template

In this page, we present the template for writing the environment for an engine
family `X`, content separated into several parts for easier handling. The
environment's page for an engine family is a Juvix Markdown file that describes
_all_ types—or rather type parameters, to be precise—regardless of whether they
are specific to the [[Engine Family Types|engine family]] or shared with others
(and used).

??? note "Family-specific vs. shared types"

    Family-specific type definitions

    : A type declaration is _family-specific_ if
    no other module imports that type directly,
    with the possible exception of the module for protocol-level messages and environments,
    i.e., `[protocol_name]_protocol_types`
    is the only module that may ímport a family-specific type.

    : A family-specific type definition has to be described in
    [[Engine Environment Template|this page]].

    Shared type definitions

    : A type is _shared_ if
      at least one other engine family is directly importing
      the type declaration in its engine environment module.

    : A shared type declaration should be included via
    [[Include code snippets| snippeting `--8<--`]] in a `!!! quote ""` admonition
    (see also [PyMdown Extensions Documentation](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/))—_including the explanation_
    (and a link to the original may be useful).

    : The location of the type declaration of a shared type
    is either

    : - the lowest common ancestor that the engine families share in
      the [[Engine Family Hierarchy]], or
      - a more suitable place,
      e.g., if it is one of the [[Basic Types]].


!!! info

    Press the :material-content-copy: button in the code snippet below to copy each part of the
    template and save its content in a new file
    `docs/node_architecture/engines/x_environment.juvix.md`.


## Front Matter

```html linenums="1" title="docs/node_architecture/engines/x_environment.juvix.md"
--- <!-- (1)! -->
icon: octicons/gear-16  <!-- (2)! -->
search:
  exclude: false
categories:
- engine-family <!-- (3)! -->
- juvix-module
tags:
- mytag1 <!-- (4)! -->
- engine-environment
---
```

--8<-- "./docs/tutorial/engines/template/engine_overview.md:annotations"

## Juvix preamble

The _Juvix preamble_ is a collapsed admonition that contains the [Juvix `module` declaration](https://docs.juvix.org/latest/reference/language/modules.html)
and all necessary imports. It starts with the module declaration (based on the path and file name), followed by imports, opens, etc. The module's name, after the path, is for our example, `X_environment`.

=== "Markdown"

    ```markdown linenums="13" hl_lines="4" title="docs/node_architecture/engines/x_environment.juvix.md"
    --8<-- "./docs/node_architecture/engines/x_environment.juvix.md!:juvix-preamble"
    ```

=== "Preview"

    --8<-- "./docs/node_architecture/engines/x_environment.juvix.md:juvix-preamble"


## Main content

```html linenums="1" linenums="21" title="docs/node_architecture/engines/x_environment.juvix.md"
!!! warning "[Under construction]"  <!-- (1)! -->

    This (Juvix) page is still under construction, needs to be updated with the latest
    changes in the engine family type.

# X Environment <!-- (2)! -->

## Overview <!-- (3)! -->

[...] <!-- (4)! -->

## Messages  <!-- (5)! -->

??? note "Auxiliary Juvix code <!-- (6)! -->

    [...] <!-- (7)! -->

[...] <!-- (8)! -->

## Mailbox states <!-- (9)! -->

[...] <!-- (10)! -->

## Local state <!-- (11)! -->

[...] <!-- (12)! -->

## Timer handles <!-- (13)! -->

[...] <!-- (14)! -->

## Environment summary <!-- (15)! -->

[...] <!-- (16)! -->

```

1. Although not mandatory, it is recommended to include a warning that the page
  is under construction, or other relevant information. Other admonitions may
  be used as well. Read more about admonitions in the
  [Markdown Guide](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

2. This is the page title and must follow the schema `[Engine family name] Environment`.

3. For complicated engines, we want an overview of how types relate to each
  other, either within the engine family or beyond engine family boundaries
  and/or intra-node or inter-node.

4.  Form

    : This is free form (and shorter is better), _except_ for that
    at the end, we eventually want some rendering of the code dependencies
    (in particular if they can be automatically generated).

    Goal

    : An overview of how data types depend on each other.

    !!! quote "Pseudo-example"

        Members of engine family X can do many different things.
        In particular, they enable communication of X engines with Y engines.

5.  First, we define _the_ Juvix record type for _all_ messages that members of
  family `X` are able to process;[^2] then, we document this type, one
  constructor at a time. We call these constructors the _message tags_ of the
  engine family `X`.[^2--0]

6. This hidden content contains a Juvix code block that gives the Juvix type;
   the type name follows the pattern `XMessage`

7. Test!

    --8<-- "./docs/node_architecture/engines/x_environment.juvix.md:juvix-preamble"

8. X

9. X

10. X

11. X

12. X

13. X

14. X

15. X

16. X



<!-- footnotes -->

[^2]: Thus, any messages that cannot be interpreted as
    terms of this type are simply dropped.

[^2--0]: The term `message tag` is borrowed from
  [the Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832).
  The list of argument types has to be uniquely determined by
  the message tag (at least within this engine family).


[^2-0]: There is no syntax highlighting, yet,
        but we want snippeting to help reach consistency
        and avoid copy and paste errors.

[^3]: The purpose of timers should be explained already
      in the engine overview in broad terms.