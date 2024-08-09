---
icon: octicons/project-template-24
search:
  exclude: false
---

# [Engine Family Name] Environment

!!! note

    The [[Engine Environment Template| ⟦Engine Family Name⟧ Environment]] page lists
    _all_ types—or rather type parameters,
    to be precise—that are either
    specific to the [[Engine Family Types|engine family]] or shared with others (and used).

    Family-specific type definitions

    : A type declaration is _family-specific_ if
    no other module ímports that type directly,
    with the possible exception of the module for protocol-level messages and environments,
    i.e., `[protocol_name]_protocol_types`
    is the only module that may ímport a family-specific type.

    : A family-specific type definition has to be described in
    [[Engine Environment Template|this page]].

    Shared type definitions

    : A type is _shared_ if
      at least one other engine family is directly ímporting
      the type declaration in its engine environment module.

    : A shared type declaration should be be linked _and_ included via
    [[Include code snippets| snippeting `--8<--`]] in a `!!! quote` environment
    (see also [PyMdown Extensions Documentation](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/))—_including the explanation_.[^1]

    : The location of the type declaration of a shared type
    is either

    : - the lowest common ancestor that the engine families share in
      the [[Engine Family Hierarchy]], or
      - a more suitable place,
      e.g., if it is one of the [[Basic Types]].

    Now, we come back to the actual description of types.

    Conceptual structure

    : We describe each of the following type parameters in order
    (or include a description via snippeting):
    [[Engine Environment Template#messages|messages]],
    [[Engine Environment Template#mailbox-states|mailbox states]],
    [[Engine Environment Template#local-state|local state]], and
    [[Engine Environment Template#timer-handles|timer handles]].
    Interdependencies between those type should be explained.
    In particular,
    for each data item in the local state,
    it should be explained why it rather belongs to the engines generic local state
    and should not be moved to a mailbox state.

    Goals

    : Engineering can quickly access all type information of the
    engine family and moreover can read a description of the purpose of
    the inhabitants of the  message type, mailbox state type, local state type,
    and timer handle type,
    in broad terms.

    Form

    : Tips (`!!! tip "[some tip]"`) or warnings (`!!! warning "[some warning]"`) may be used to highlight ímportant details.

!!! tip "Time is ɴᴏᴛ part of engine environments"

    The local clocks of engine instances are "external" to engine instances.
    If you need information about wall-clock time,
    you must rely on "time stamps" of triggers.
    Use local time and timers only if necessary.
    Moreover, each Anoma node may at some point in time have
    a node-wide wall-clock time service,
    which would be yet different
    in that it will try to relate to local time
    of users on their watches in the vicinity of the node.

!!! note "Juvix preamble"

    We have the `module` declaration (according to the path and file name)
    followed by `import`s, `open`s, etc.

    ```juvix
    module tutorial.engines.template.engine_environment;
    ```

    The naming scheme for the module, after the path,
    is `[engine_family_name]_engine_environment`.

    !!! todo "fix the location"

        The modules of the actual specification
        should certainly ɴᴏᴛ reside in the tutorial folder!

!!! warning "Reminder about “derived” protocol-level types"

    Note that after the definition of all engine-specific types,
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

    For complicated engines,
    we want an overview of how types relate to each other,
    either within the engine family or beyond engine family boundaries
    and/or intra-node or inter-node.

    Form

    : This is free form (and shorter is better), _except_ for that
    at the end, we eventually want some rendering of the code dependencies
    (in particular if they can be automatically generated).

    Goal

    : An overview of how data types depend on each other.

!!! question "Can we haz code dependency diagram?"

    If only we had
    [something like this](https://www.jetbrains.com/guide/java/tutorials/analyzing-dependencies/dependency-diagram/).
    However,
    somebody will write a small script probably some time soon.

## Messages

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

    Form

    : First, we have `!!! note "Message type"` with the juvix type definitions,
    where the type name follows the pattern `[EngineFamilyName]Message`.

    : Afterwards, we want exactly one level four heading `#### [Message tag]` for
    each receivable message tag
    (or, equivalently, for each constructor of the record type).
    The content of the level four heading has again two parts:
    message documentation and additional remarks.

    Message documentation

    : Part one is given in the _form_ of
    a [definition list](https://pandoc.org/MANUAL.html#definition-lists)
    in the sense of markdown
    (see also [here](https://stackoverflow.com/q/28057101))
    where the "terms" are the formal parameter name defaults,
    and the definitions are a short English language description of
    the role (and type) of the parameter,
    plus the type definition (with a link to where it is defined—if applicable).

    !!! question "How to add example code?"

        Each such explanation should be followed by
        an example instance of the message in juvix.
        How to best do this?

    Additional comments `{` optional `}`

    : You may provide additional information,
    e.g., design choices, explanation of the naming process, etc.
    This is in the form of a `??? note "[something to remember]"`
    or a `!!! note "[something to remember]"`,
    and similarly for `tip` and `warning`.

<!--
!!! question "ᚦ: _Is this the right spot for the Juvix code?_"

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

## Mailbox states

!!! note

    Mailboxes of engines may have non-trivial state
    for each mailbox;
    if an engine family relies on non-trivial mailbox state,
    it has to be documented here.
    We want one Juvix record type or algebraic data type
    at the level of the engine family;
    each constructor typically correspond to a family of mailboxes
    that serve a similar purpose.

    Form

    : A record type and explanatory prose for each constructor;
      the explanatory prose is succeeding the type definition.
      The form is similar that for
      [[Engine Environment Template#messages|messages]].

    Goal

    : Each constructor should have a clearly stated purpose.

<!--ᚦ: keep this here for a moment ¶
!!! example

    - Each mailbox has a ring buffer to estimate
      the frequency of time stamping requests.

??? todo

    add juvix code for a ring buffer for this example ☝️
-->

## Local state

!!! note

    The engine-specific local state type is often the most complex type,
    tailor-made for a specific engine family.


    Form

    : First, the local state is described in broad terms;
    then follows either a new definition of the type in Juvix, a snippet, or a link where it is defined.
    Finally, we want to describe all data items
    and also the data structures used
    in English language;
    technical terms should be linked,
    either to documentation, here, elsewhere or on Wikipedia-page (or similar).

    Goal

    : Besides documentation for each data item, we also require links to
    descriptions of data structures beyond trees, hash maps
    unless they are defined in the Juvix standard library;
    links to descriptions may be sufficient in many cases.

<!--ᚦ:
!!! example

    We use the state of the time stamping server
    to store the rate limit
    (that we assume to be static for the sake of simplicity).


    `juvix`
    ```
    TimeStampingServerState := Nat;
    ```
-->

## Timer handles

!!! note

    Similar to mailbox specific types,
    each timer may carry some information,
    e.g., about the context in which it was set.

    Form

    : A juvix data type plus documentation.
    This is similar to
    [[Engine Environment Template#messages|messages]].

    Goal

    : Get an overview of different purposes of different timers.

## Environment summary

!!! note

    This is the place where the environment type is defined.
    If applicable,
    this is a good place to put additional comments
    that only make sense after everything is defined.

    Form

    : free form, _except_ for the data type definition in Juvix at the end.

[^1]: The main reason for the linking is that we do not have syntax highlighting, yet
    (and that it does not hurt to have a section title for each type definition).
