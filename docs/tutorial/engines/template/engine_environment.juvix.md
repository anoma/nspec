---
icon: octicons/check-24
search:
  exclude: false
---

# [Engine Family Name] Environment

??? note "Juvix preamble"

    We have the `module` declaration (according to the path and file name)
    followed by `import`s, `open`s, etc.

    ```juvix
    module tutorial.engines.template.engine_environment;
    ```

!!! note

    This pages describes
    all types—or type parameters, to be precise—that are
    specific to engine family [engine family name].
    However,
    if several engine families share a type,
    the best place to place the definition of the Juvix type is either

    - the lowest common ancenstor that the engine families share in
      the engine family hierarchy, or

    - a more suitable place, if that is not an option,
      e.g., if it is one of the [[Basic Types]].

!!! warning "Reminder about “derived” protocol-level types"

    Note that after the defintion of all engine-specific types,
    there are "derived types" for engine environments
    and messages at the protocol-level.
    This is relevant also for specs writing as
    for the creation of new engine instances,
    we use the protocol-level engine environment type,
    and similarly, for sending new messages,
    we rely on a protocol-level message type.
    This will be relevant for the [[Engine Dynamics Template|dynamics of engines]].

## Overview `{`optional`}`

!!! note

    You may want to provide an overview of how things relate to each other.

    Form

    : free form, but shorter is better

### Messages

!!! note

    First, we describe the message type
    for all messages that members of family [family name]
    are able to process, in principle.
    For each such "receivable" message,
    we have

    - a _message tag_
    - a list of _argument types_
    - a (default value for a) _formal parameter name_ for
      each element of the list of argument types

    The term `message tag` is borrowed from
    [the Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832).
    The list of argument types has to be uniquely determined by the message tag (at least within this engine family).

    Form

    : First, we have `note` with the juvix type definitions.
    Afterwards, ther is exactly one level four heading `#### [Message Tag]` for each receivable message tag (or for each constructor of the record type, if you prefer).
    The content of the level four heading has two parts.

    1. Part one is given in the _form_ of a [definition list](https://pandoc.org/MANUAL.html#definition-lists) in the sense of markdown
       (see also [here](https://stackoverflow.com/q/28057101))
       where the "terms" are the formal parameter name defaults,
       and the definitions are a short English language description of
       the role (and type) of the parameter,
       plus the type definition (with a link to where it is defined—if applicable).

    2. Part is optional; if given, it  provides additional information,
       e.g., design choices, explanation of the naming process, etc.

!!! question "ᚦ: _Is this the right spoto for the Juvix code?_"

    The given option is in response to our dear engineers.
    Other options would be

    - collapsed at the top
    - uncollapsed at the bottom

    One downside of the very succinct record type is
    that the definition becomes "monolithic".

    ??? note "In an ideal world ..."

        If only the record type would be generated out of the markdown
        (also checking, that the markdown adheres to the template ...),
        but then we would need the type definitions for the parameters
        ...
