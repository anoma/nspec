---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- template
---

<!-- Do not delete the following link since it contains the base document for this page: https://raw.githubusercontent.com/anoma/nspec/c61eb3d4e2733ad5712155beabe5e80a6aaff59d/docs/tutorial/engines/template/engine_environment.juvix.md?token=GHSAT0AAAAAACVOLA35IMRBAMF7POUITPSGZWX6GJQ

-->

# Engine Environment Template

In this page, we present the template for writing the environment for a generic
engine family called `Template`. The template is separated into several parts for easier
handling. These engine-environment pages are, in principle, Juvix Markdown files
that describe _all_ types—or rather type parameters, to be precise—regardless
of whether they are specific to the [[Engine Family Types|engine family]] or
shared with others (and used).

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
    `docs/node_architecture/engines/template_environment.juvix.md`.


## Part 1: front matter

```html linenums="1" title="docs/node_architecture/engines/template_environment.juvix.md"
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

## Part 2: Juvix preamble

The _Juvix preamble_ is a collapsed admonition that contains the [Juvix `module`
declaration](https://docs.juvix.org/latest/reference/language/modules.html) and
all necessary imports. It starts with the module declaration (based on the path
and file name), followed by imports, opens, etc. The module's name, after the
path, is for our example, `template_environment`.

=== "Markdown"

    ```markdown linenums="13" hl_lines="4" title="docs/node_architecture/engines/template_environment.juvix.md"
    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md!:juvix-preamble"
    ```

=== "Preview"

    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md:juvix-preamble"


## Part 3: main content

```html linenums="1" linenums="21" title="docs/node_architecture/engines/template_environment.juvix.md"
!!! warning "[Under construction]"  <!-- (1)! -->

    This (Juvix) page is still under construction, needs to be
    updated with the latest changes in the engine family type.

# Template Environment <!-- (2)! -->

## Overview <!-- (3)! -->

[...] <!-- (4)! -->

## Messages  <!-- (5)! -->

[...] <!-- (6)! -->

??? note "Auxiliary Juvix code

    [...]

```juvix <!-- (7)! -->
type XMessage :=   <!-- (8)! -->
  | -- <!-- --8<-- [start:message1] -->
  MessageConstructor1 <!-- (9)! -->
  -- <!---8<-- - [end:message1] -->
  -- ...
```a

### [Message constructor 1] <!-- (10)! -->

If an [engine family] engine receives a message of
this type, it will [...]

<!-- Code snippet --> <!-- (11)! -->

<!-- Message tag documentation and example --> <!-- (12)! -->

### [Message constructor ...]

[...] <!-- (13)! -->

## Mailbox states <!-- (14)! -->

??? note "Auxiliary Juvix code

    [...]

[...]  <!-- (15)! -->

## Local state <!-- (16)! -->

[...] <!-- (17)! -->

## Timer handles <!-- (18)! -->

??? note "Auxiliary Juvix code"

    [...]

[...] <!-- (19)! -->

## Environment summary <!-- (20)! -->

[...] <!-- (21)! -->

```

1. Although not mandatory, it is recommended to include a warning that the page
  is under construction, or other relevant information. Other admonitions may
  be used as well. Read more about admonitions in the
  [Markdown Guide](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

2. This is the page title and must follow the schema `[Engine family name] Environment`.

3. This section is **optional**. For complicated engines, we want an overview of how types relate to each
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

5.  In this section, we define _the_ Juvix record type for _all_ messages that members of
  family `X` are able to process;[^2] then, we document this type, one
  constructor at a time. We call these constructors the _message tags_ of the
  engine family `X`.[^2--0]


    ??? note "On the relation to `receivable message` and `message tag`"

        Terms of this type represent a _receivable message_,
        consisting of

        - a _message tag_
        - a list of _argument types_
        - a (default value for a) _formal parameter name_ for
          each element of the list of argument types.

        The message tag is given by the constructor,
        the default parameter names correspond to the field names of the "embedded" record,
        and the associated types are the types of the respective fields.

6. First, we have a hidden note `??? note "Auxiliary Juvix code"` followed by a
    Juvix code block that gives the Juvix type; the type name follows the pattern
    `[EngineFamilyName]Message`.

    Juvix example:

    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md:message_auxiliary"

    :   Afterwards, we want exactly one level three heading of the form `###
        [Message constructor]` for each constructor of the message type (or,
        equivalently, for each message tag). The content of the sub-subsections
        under those level three headings for each message tag have again three
        parts: a code snippet, a message tag documentation that concludes with
        an example, and additional remarks.

7. At this precise point, we include the Juvix type definition for the message
   type. For example, the following type definition declares the type
   `TemplateMessage` with four data constructors corresponding to four different
   message tags:

    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md:TemplateMessageType"

8. In Juvix syntax, after `:=` we define the data constructors, each separated
   by `|`. Also, for each message constructor, we put two "invisible" comments
   into the Juvix record type to facilitate code-references, namely a pair of
   lines like

    ```
    -- <!-- --8<-- [start:messageK] -->
    ```
    and

    ```
    -- <!-- --8<-- [end:messageK] -->
    ```

    that embrace the constructor of the k-th message; then we can include the
    very same code by writing `--8<--
    "./[engine_family]_engine_environment:messageK"` to obtain the required code
    fragment.[^2-0]

9. As an example, we have one data constructor for the message type
   `TemplateMessage` called `messageOne`, which requires three arguments:
   `argOneOne`, `argTwo`, and `argThree`, of different types as defined as
   follows:

    ```
    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md!:messageOne"
    ```

    first data constructor in the `TemplateMessage` type:

      --8<-- "./docs/node_architecture/engines/template_environment.juvix.md:TemplateMessageType"

10. TODO

11. TODO

12. TODO

13. The message tag documentation start with a description of what reactions the
    receiving engine may perform as a reaction in broad terms. After this
    description, we use the syntax of what pandoc calls a [definition
    list](https://pandoc.org/MANUAL.html#definition-lists) (see also
    [here](https://stackoverflow.com/q/28057101)) where the "terms" are the record
    fields and the "definitions" are short English language descriptions of the role
    of the respective parameter—plus optional explanations of its type (with a link
    to where it is defined—if applicable). The documentation of the message tag is
    followed by an example term with the respective message tag.

    Goal

    : Each receivable message is documented
    like a public method of some mutable object would be documented
    in object-oriented languages.

14. If an engine family relies on non-trivial mailbox state,
    it has to be documented here.
    We want one Juvix record type or algebraic data type
    at the level of the engine family;
    each constructor typically corresponds to a family of mailboxes
    that serve a similar purpose.

    Form

    : A record type and explanatory prose for each constructor;
      the explanatory prose is succeeding the type definition.
      The form is similar to that for
      [[Engine Environment Template#messages|messages]];
      in particular,
      the sections starts with a note `??? note "Auxiliary Juvix code"`
      that contains any auxiliary definitions.


    Goal

    : Each constructor should have a clearly stated purpose
    and the role of the arguments is explained.

15. A record type and explanatory prose for each constructor; the explanatory
      prose is succeeding the type definition. The form is similar to that for
      [[Engine Environment Template#messages|messages]]; in particular, the
      sections starts with a note `??? note "Auxiliary Juvix code"` that
      contains any auxiliary definitions.

16. Here we define the so-called _local state_ of the engine environment, which
    is typically tailor-made for each engine family.

    Goal

    : Besides documentation for each data item,
    the reader may follow links to
    descriptions of data structures
    (beyond the most basic one like trees, hash maps, etc.
    and those defined in the Juvix standard library).

17. First, the local state is described in broad terms (different than from in
    the other sections). The informal description is followed by either a new
    definition of the type in Juvix (or a snippet with a link where it is
    defined); any auxiliary code is given in a `??? note "Auxiliary Juvix code"`
    admonition. Finally, we want to describe all data items and also the data
    structures used in English language; technical terms should be linked,
    either to documentation, here, elsewhere or on Wikipedia-page (or similar).

18. This section is about the type of timer handles. Recall that a timer may
    carry some information as part of its _handle,_ e.g., about the context in
     which it was set.

    Goal

    : Get an overview of a family of timers,
    and what data is relevant for each family.[^3]

19. Here we put a juvix data type plus documentation.
    The form is mirroring that of the messages' section.

20. This is the place where the environment type is defined. If applicable, this
    is a good place to put additional comments that only make sense after
    everything is defined.

21. This section is free form, _except_ for the datatype definition and an
    example in Juvix at the end. The datatype definition is as in the following
    example:

    --8<-- "./docs/node_architecture/engines/template_environment.juvix.md:TemplateEnvironment"


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