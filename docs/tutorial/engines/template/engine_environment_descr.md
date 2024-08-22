---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- template
---

# Engine "Environment" Template

In this page, we present the template for writing the environment for an engine
family `x`, content separated into several parts for easier handling. The
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
    `docs/node_architecture/engines/X_environment.juvix.md`.


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

=== "Markdown"

    The _Juvix preamble_ is a collapsed admonition that contains the [Juvix `module` declaration](https://docs.juvix.org/latest/reference/language/modules.html)
    and all necessary imports. It starts with the module declaration (based on the path and file name), followed by imports, opens, etc. The module's name, after the path, is for our example, `X_environment`.

    ```markdown linenums="13" hl_lines="4" title="docs/node_architecture/engines/x_environment.juvix.md"
    --8<-- "./docs/node_architecture/engines/x_environment.juvix.md!:juvix-preamble"
    ```

=== "Preview"

    --8<-- "./docs/node_architecture/engines/x_environment.juvix.md:juvix-preamble"


```html linenums="1" linenums="21" title="x_overview.md"
!!! warning "[Under construction]"  <!-- (1)! -->

    This page is still under construction, needs to be updated with the latest
    changes in the engine family type.

# X Environment <!-- (2)! -->

```

2. Although not mandatory, it is recommended to include a warning that the page
  is under construction, or other relevant information. Other admonitions may
  be used as well. Read more about admonitions in the
  [Markdown Guide](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

1. This is the page title and must follow the schema `[Engine family name] Environment`.


??? note "On `X Environment`"

    Conceptual structure

    : We describe each of the following type parameters in order
    (or include a description via snippeting):
    [[Engine Environment Template#messages|messages]],
    [[Engine Environment Template#mailbox-states|mailbox states]],
    [[Engine Environment Template#local-state|local state]], and
    [[Engine Environment Template#timer-handles|timer handles]].
    Interdependencies between these type definitions should be explained.
    In particular,
    for each data item in the local state,
    it should be explained why it rather belongs to
    the generic local state of the engine,
    e.g., by giving a list of hurdles, inconveniences, and issues that
    are in the way of moving it to a mailbox state.

    Goals

    : Engineering can quickly access all type information of the
    engine family and moreover can read a description of the purpose of
    the inhabitants of the message type, mailbox state type, local state type,
    and timer handle type,
    in broad terms.