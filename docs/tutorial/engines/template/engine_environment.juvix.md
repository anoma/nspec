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
    import node_architecture.types.engine_family open;
    ```

    The naming scheme for the module, after the path,
    is `[engine_family_name]_engine_environment`.

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

    Goal

    : An overview of how data types depend on each other.

    !!! quote "Pseudo-example"

        Members of engine family [engine family name]
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
    of the engine family [engine family name].[^2--0]

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

    :   First, we have a hidden note `??? note "Auxiliary Juvix code"`
        followed by a juvix code block that gives the Juvix type;
         the type name follows the pattern `[EngineFamilyName]Message`.


    :   Afterwards,
        we want exactly one level three heading
        of the form `### [Message constructor]`
        for each constructor of the message type
        (or, equivalently, for each message tag).
        The content of the sub-subsections under
        those level three headings for each message tag
        have again three parts:
        a code snippet,
        a message tag documentation that concludes with an example,
        and additional remarks.

        Code snippet

        :   For each message constructor,
            we should put two "invisible" comments into the juvix record type,
            namely a pair of lines like

            ```
            -- --8<-- [start:messageK]
            ```

            : and

            ```
            -- --8<-- [end:messageK]
            ```

            that embrace the constructor of the $k$-th message;
            then we can include the very same code by writing
            `--8<-- "./[engine_family]_engine_environment:messageK"`
            to obtain the required code fragment.[^2-0]

        Message tag documentation and example

        : The message tag documentation start with a description of
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
        The documentation of the message tag is
        followed by an example term with the respective message tag.

    Goal

    : Each receivable message is documented
    like a public method of some mutable object would be documented
    in object oriented languages.

    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            syntax alias MethodOneArgOne := Nat;
            syntax alias MethodOneArgTwo := Nat;
            syntax alias MethodOneArgThree := Nat;
            syntax alias MethodTwoArgOne := Nat;
            syntax alias MethodFourArgOne := Unit;
            syntax alias MethodFourArgTwo := Unit;
            ```

        ```juvix
        type TemplateMessage :=
          | -- --8<-- [start:messageOne]
            messageOne {
              argOneOne : MethodOneArgOne;
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
        if argOne and argThree satisfy some properties.

        ```juvix
        module message_one_example;
           example_message_one : TemplateMessage := messageOne@{
            argOneOne := 1;
            argTwo := 2;
            argThree := 3
           };
        end;
        ```


        argOne

        : The `argOne` is almost self-explanatory, but we need to talk about it.

        argTwo

        : This is the second argument.

        argThree

        : This is the last argument and here we actually
          can describe more detail about the property about `argOne` and `argThree` mentioned above

        ### messageTwo

        [...]

        ### messageThree

        [...]

        ### messageFour

        [...]

## Mailbox states

!!! note "On `Mailbox states`"

    If an engine family relies on non-trivial mailbox state,
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

    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            syntax alias MailboxOneOne := Nat;
            syntax alias MailboxTwoOne := String;
            syntax alias MailboxTwoTwo := Bool;
            ```

        ```juvix
        type TemplateMailboxState :=
        | -- --8<-- [start:stateOne]
          stateOne { fieldOne : MailboxOneOne }
          -- --8<-- [end:stateOne]
        | -- --8<-- [start:stateTwo]
          stateTwo { fieldOne : MailboxTwoOne; fieldTwo : MailboxTwoTwo }
          -- --8<-- [end:stateTwo]
        ;
        ```

        ### stateOne

        !!! quote ""

            --8<-- "./engine_environment.juvix.md:stateOne"

        This is one family of mailbox states without much complexity.

        ```juvix
        module state_one_example;

        stateOneExample : TemplateMailboxState := stateOne@{
          fieldOne := 1
        };
        end;
        ```

        fieldOne

        : A Nat is a Nat is a Nat.

        ### stateTwo

        [...]

## Local state

!!! note "On `Local state`"

    Here we define the so-called _local state_ of
    the engine environment,
    which is typically tailor-made for each engine family.

    Form

    : First, the local state is described in broad terms
    (different than in the other sections).
    The informal description is followed
    by either a new definition of the type in Juvix
    (or a snippet with a link where it is defined);
    any auxiliary code is given in a
    `??? note "Auxiliary Juvix code"` admonition.
    Finally, we want to describe all data items
    and also the data structures used
    in English language;
    technical terms should be linked,
    either to documentation, here, elsewhere or on Wikipedia-page (or similar).

    Goal

    : Besides documentation for each data item,
    the reader may follow links to
    descriptions of data structures
    (beyond the most basic one like trees, hash maps, etc.
    and those defined in the Juvix standard library).

    !!! quote "Pseudo-example"

        We use [Fibonacci heaps](https://en.wikipedia.org/wiki/Fibonacci_heap)
        to keep track of tasks to be performed.
        Note that we use [Borsh](https://borsh.io/)
        for deserialisation of Fibonacci heaps.

        ??? note "Auxiliary Juvix code"

            ```juvix
            someComplicatedFunction : Type -> Type := undef;
            SomeAuxiliaryDataType : Type := undef;
            ```

        ```juvix
        type FakeFibonacciHeap := mkFakeFibonacciHeap {
            stringRepresentation : String
        };

        type TemplateLocalState := mkTemplateLocalState {
             taskQueue : FakeFibonacciHeap
        };
        ```

        stringRepresentation

        : This is a representation of the Fibonacci heap,
        using [Borsh](https://borsh.io/).

## Timer handles

!!! note "On `Timer handles`"

    This section is about the type of timer handles.
    Recall that a timer may carry some information
     as part of its _handle,_
    e.g., about the context in which it was set.

    Form

    : A juvix data type plus documentation.
    The form is mirroring that of
    [[Engine Environment Template#messages|messages]].

    Goal

    : Get an overview of a family of timers,
    and what data is relevant for each family.[^3]

    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            syntax alias ArgOne := Nat;
            ```

        ```juvix
        type TemplateTimerHandle :=
        | -- --8<-- [start:handleOne]
          timerHandleOne { argOne : ArgOne }
          -- --8<-- [end:handleOne]
        | timerHandleTwo { argOne : String; argTwo : Bool }
        | timerHandleThree {
        };
        ```

        ### timerHandleOne

        !!! quote ""

            --8<-- "./engine_environment.juvix.md:handleOne"

        The first kind of timer handle.

        ```juvix
        module handle_one_example;

        handleOneExample : TemplateTimerHandle := timerHandleOne@{
          argOne := 7;
        };
        end;
        ```

        argOne

        : This is argument №1.

        ### timerHandleTwo

        [...]

        ### timerHandleTwo

        [...]

## Environment summary

!!! note

    This is the place where the environment type is defined.
    If applicable,
    this is a good place to put additional comments
    that only make sense after everything is defined.

    Form

    : This section is free form,
      _except_ for the datatype definition and
      an example in Juvix at the end.

    !!! quote "Pseudo-example"

        We have finished all the type definitions,
        there is nothing to explain in the template
        as the code is self-explanatory.


        ```juvix
        TemplateEnvironment : Type :=
          EngineEnvironment
          TemplateLocalState
          TemplateMessage
          TemplateMailboxState
          TemplateTimerHandle;
        ```

        !!! todo "fix example 👇"

        ```juvix
        module template_environment_example;
        templateEnvironmentExample : TemplateEnvironment := undef;
        end;
        ```

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
