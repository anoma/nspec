---
icon: octicons/project-template-24
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

    The environment page describes
    _all_ types—or type parameters, to be precise—that are
    **specific to engine family [engine family name]**.
    However,
    if several engine families share a type,
    the best place to place the definition of the Juvix type is either

    - the lowest common ancenstor that the engine families share in
      the engine family hierarchy, or

    - a more suitable place, if that is not an option,
      e.g., if it is one of the [[Basic Types]].

    Conceptual structure

    : We start with messages, mailbox state, then describe local state;
    interdependencies should be explained in the overview section.

    Goals

    : Engineering can quickly get an overview of the types of the
    engine family and also a rough idea of the function of
    each message or how state is used.


!!! warning "Reminder about “derived” protocol-level types"

    Note that after the defintion of all engine-specific types,
    there are "derived types" for engine environments
    and messages at the protocol-level.
    This is relevant also for specs writing as
    for the creation of new engine instances,
    we use the protocol-level engine environment type,
    and similarly, for sending new messages,
    we rely on thy protocol-level message type.
    This will be relevant for the
    [[Engine Dynamics Template|dynamics of engines]].

## Overview `{`optional`}`

!!! note

    We first give an overview of how things relate to each other,
    either within the engine family or beyond engine family boundaries    
    and/or intra-node or inter-node.
    
    Form

    : This is free form (and shorter is better), _except_ for that
    at the end, we eventually want some rendering of the code dependencies,
    if they can be automatically generated.

    Goal

    : Give an overview of data types relate to each other.

!!! question "Can we haz code dependency diagram?"

    If only we had
    [something like this](https://www.jetbrains.com/guide/java/tutorials/analyzing-dependencies/dependency-diagram/).
    However,
    somebody will write a small script probably some time soon. 


### Messages

!!! note

    First, we define _the_ message type (as a juvix record)
    whose terms members of family [family name]
    are able to process, in principle.
    For each such _receivable message_,
    we have

    - a _message tag_
    - a list of _argument types_
    - a (default value for a) _formal parameter name_ for
      each element of the list of argument types

    where the message tag is given by a constructor,
    the default parameter names are the field names of the "embedded" record,
    and the types are given as the types of the field names.

    Then, we document this type.
    
    !!! question "Why message tag⁈"

        The term `message tag` is borrowed from
        [the Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832).
        The list of argument types has to be uniquely determined by
        the message tag (at least within this engine family).

    #### Form

    First, we have `!!! note "message type"` with the juvix type definitions.

    Afterwards, we want exactly one level four heading `#### [Message Tag]` for
    each receivable message tag (or, if you prefer, for each constructor of the record type).
    The content of the level four heading has again two parts:
    message documentation, additional remarks

    ##### Message documentation

    Part one is given in the _form_ of
    a [definition list](https://pandoc.org/MANUAL.html#definition-lists)
    in the sense of markdown
    (see also [here](https://stackoverflow.com/q/28057101))
    where the "terms" are the formal parameter name defaults,
    and the definitions are a short English language description of
    the role (and type) of the parameter,
    plus the type definition (with a link to where it is defined—if applicable).

    !!! question "How to add example code?" 

        Each such explantion should be followed by
        an example instance of the message in juvix.
        How to best do this?

    ##### Addiitional comments `{` optional `}`

    Here, we can provide additional information,
    e.g., design choices, explanation of the naming process, etc.

<!--
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
-->


