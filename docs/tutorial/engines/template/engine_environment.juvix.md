---
icon: octicons/project-template-24
search:
  exclude: false
---

??? note "Juvix preamble: ʜᴇʀᴇ 👇 are the `module` declaration, `import`s, `open`s, etc."

    We have the `module` declaration (according to the path and file name)
    followed by `import`s, `open`s, etc.

    ```juvix
    module tutorial.engines.template.engine_environment;
    import prelude open;
    ```

    The naming scheme for the module, after the path,
    is `[engine_family_name]_engine_environment`.

!!! todo "fix the location of the module declaration"

    The modules of the actual specification
    should certainly ɴᴏᴛ reside in the tutorial folder!



# [Engine Family Name] Environment

!!! note "On `[Engine Family Name] Environment`"

    The [[Engine Environment Template| ⟦Engine Family Name⟧ Environment]] page describes
    _all_ types—or rather type parameters,
    to be precise—regardless of whether they are
    specific to the [[Engine Family Types|engine family]] or
    shared with others (and used).

    ??? note "Family-specific vs. shared"

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
    the inhabitants of the  message type, mailbox state type, local state type,
    and timer handle type,
    in broad terms.

    Form

    : The present template describes the form.
    _The juvix preamble is preceding the page title._
    Moreover,
    tips (`!!! tip "[some tip]"`) or
    warnings (`!!! warning "[some warning]"`)
    may be used to highlight ímportant details.

<!--ᚦ: this is to be moved to the tutorial¶
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
-->
<!--ᚦ: this probably should be moved as well:
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
-->

## Overview `{`optional`}`

!!! note "On `Overview`"

    For complicated engines,
    we want an overview of how types relate to each other,
    either within the engine family or beyond engine family boundaries
    and/or intra-node or inter-node.

    Form

    : This is free form (and shorter is better), _except_ for that
    at the end, we eventually want some rendering of the code dependencies
    (in particular if they can be automatically generated).

    !!! question "Can we haz code dependency diagram?"

        If only we had
        [something like this](https://www.jetbrains.com/guide/java/tutorials/analyzing-dependencies/dependency-diagram/).
        However,
        somebody will write a small script probably some time soon.

    Goal

    : An overview of how data types depend on each other.




!!! quote ""

    Members of engine family [engine fmaily name]
    can do many different things.
    In particular,
    they enable communication of X engines with Y engines.

## Messages

!!! note "On `Messages`"

    First, we define _the_ Juvix record type
    for _all_ messages that members of family [family name]
    are able to process;[^2]
    then, we document this type,
    one constructor at a time.
    We call these constructors the _message tags_
    of the engine familiy [engine family name].[^2--0]

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




    Form

    : First, we have a
    `!!! note "[EngineFamilyName] message type"` admonition with
    the juvix type definition,
    where the type name follows the pattern `[EngineFamilyName]Message`.

    !!! question "where to put the actual auxiliary definitions"

        Where do we put the type definitions for nontrivial message arguments?

    : Afterwards,
    we want exactly one level three heading
    of the form `### [Message constructor]`
    for each constructor of the message type
    (or, equivalently, for each message tag).
    The content of the sub-subsections under
    those level three headings for each message tag
    have again three parts:
    a code snippet,
    a message tag documentation,
    and additional remarks.

    Form: code snippet

    : For each message constructor,
    we should put two "invisible" comments into the juvix record type,
    namely a pair of lines like

    ```
    -- --8<-- [start:messageK]
    ```

    : and

    ```
    -- --8<-- [end:messageK]
    ```

    : that embrace the constructor of the $k$-th message;
      then we can include the very same code by writing
      `--<8-- "./[engine_family]_engine_environment:messageK"`
      to obtain the required code fragment.[^2-0]

    Form : message tag documentation

    : The message tag documention start with a description of
    what reactions the receiving engine may perform as a reaction
    in broad terms.
    After this description,
    we use the syntax of what pandoc calls a
    [definition list](https://pandoc.org/MANUAL.html#definition-lists)
    (see also [here](https://stackoverflow.com/q/28057101))
    where the "terms" are the record fields
    and the "definitions" are short English language descriptions of
    the role of the respective parameter—plus optional
    explanations of its type
    (with a link to where it is defined—if applicable).

    !!! question "How to add actual example code?"

        Each such explanation should be followed by
        an example instance of the message in juvix.
        How to best do this? If nothing better,
        we can have code snippeting into
        an auxiliary module/page that has all such
        "explanatory" code.

    Form: additional comments `{` optional `}`

    : You may provide additional information,
    e.g., design choices, explanation of the naming process, etc.
    This is in the form of a `??? note "[something to remember]"`
    or a `!!! note "[something to remember]"`,
    and similarly for `tip` and `warning`.

    Goal

    : Each receivable message is documented
    like a public method of some mutable object would be documented
    in object oriented languages.

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

!!! quote ""


    !!! note "Template engine message type"

        ```juvix
        syntax alias MethodOneArgOne := Unit;

        syntax alias MethodOneArgTwo := Unit;

        syntax alias MethodOneArgThree := Unit;

        syntax alias MethodTwoArgOne := Unit;

        syntax alias MethodFourArgOne := Unit;

        syntax alias MethodFourArgTwo := Unit;

        type TemplateMessage :=
          | -- --8<-- [start:messageOne]
            messageOne {
              argOne : MethodOneArgOne;
              argTwo : MethodOneArgTwo;
              argThree : MethodOneArgThree
            }
            -- --8<-- [end:messageOne]
          | messageTwo {
              argOne : MethodTwoArgOne
          }
          | messageThree {}
          | messageFour {
              argOne : MethodFourArgOne;
              argTwo : MethodFourArgTwo
            }
          ;
        ```

    ### messageOne

    !!! quote ""

        --8<-- "./engine_environment.juvix.md:messageOne"

    If an [engine family name] receives a messageOne-message,
    it will store argTwo,
    if argOne and argThree satisfy some properties
    that are to be explained here.

    !!! todo "does this make sense to fill in ?"

    ### messageTwo

    ### messageThree

    ### messageFour

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

<!-- footnotes -->

[^1]: The main reason for the linking is that we do not have syntax highlighting, yet
    (and that it does not hurt to have a section title for each type definition).

[^2]: Thus, any messages that cannot be interpreted as
    terms of this type are simply dropped.

[^2--0]: The term `message tag` is borrowed from
  [the Special Delivery paper](https://dl.acm.org/doi/abs/10.1145/3607832).
  The list of argument types has to be uniquely determined by
  the message tag (at least within this engine family).


[^2-0]: The syntax highlighting is lost for the moment.


