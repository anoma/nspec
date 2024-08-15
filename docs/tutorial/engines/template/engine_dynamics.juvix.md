---
icon: octicons/project-template-24
search:
  exclude: false
---

??? note "Juvix preamble: ʜᴇʀᴇ 👇 are the `module` declaration, `import`s, `open`s, etc."

    ```juvix
    module tutorial.engines.template.engine_dynamics;

    import tutorial.engines.template.template_protocol_types;

    import Stdlib.Data.String open;
    import prelude open;
    ```

# [Engine Family Name] Dynamics

!!! note

    In this page,
    we complete the definition of the
    engine family [engine family name] by defining
    a set of [[Engine Family Types#guards|guards]],
    an  [[Engine Family Types#action-function|action function]], and
    a [[Engine Family Types#conflict-resolution|conflict resolution function]].
    Most notably,
    this involves the definition of action labels[^0]
    and a description of the effects of the associated actions.

    ??? note "Short summary of guards, the action function, and conflict resolution"

        In short,
        the action function computes the effects of actions to be taken,
        while being a [pure function](https://en.wikipedia.org/wiki/Pure_function);
        <!--(see also [[On LTS semantics of guarded actions]]);-->
        the guards determine for each possible circumstance
        which actions are to performed as a reaction.

    Conceptual structure

    :   First, we want a description of all action labels,
    in particular the effects of the associated actions;
    we also want a description of how
    conflicts of sets of action labels are resolved
    (unless we have a "smooth" engine with no such conflicts).[^1]
    After action labels and their conflict resolution
    have been described,
    we come to the description of guards,
    which, in turn,
    requires that we define the type of
    matched arguments and pre-computation results beforehand.
    Finally,
    the page contains the code of the action function,
    including code comments;
    however,
    the most ímportant points about the code
    should be described separately.[^2']

    Form

    : The form is prescribed by this template file.

    Goal

    : The main goals are two:

    : - an overview of the action labels and guards
        that should be accessible
        to a widest possible audience
        and rely only on those definitions of the engine environment
        given in the message type section (or earlier);

    : - a documentation of details that are relevant for every implementation
        (not only the model implementation).

    !!! warning "This is really ɪᴍᴘᴏʀᴛᴀɴᴛ!"

        The data of an action label should be
        as independent as possible of the engine environment.
        Roughly,
        replacing one engine implementation with a different one
        that uses a "completely different" environment type
        should always be possible.[^2]

        🚨 **Never** use the local state type of environments
        for arguments of the action label. 🚨

        Whenever you consider doing this ☝️,
        the relevant data _must_ be moved
        to the precomputation result;
        also note that the action function
        has access to the _whole environment!_
<!--ᚦ leave this here for the time being¶
    This involves the definition of three types—or type parameters,
    to be precise—besides those defined in the engine environment,
    whose terms guards compute and
    also feature in the input of the action function.

    Matched arguments

    :   Matched arguments are typically obtained by pattern matching of messages,
        be it from a trigger or previously received messages in one of the mailboxes.

    Action labels

    :   Action labels describe actions that members of the engine family
        [engine family name] can perform, in principle.


    Precomputation results

    :   Guards may involve non-trivial computations,
        which should not be repeated;
         instead the results are passed on as precomputation result.

--><!--
    For this,
    we first define a datatype of _action labels,_
    each of which defines an action that
    a member of the engine family can perform
    (in response to messages or timer notifications)—without
    mentioning the specific circumstances that call
    for performing the action that the action label describes.
    The action labels are complemented by a set of guarded actions,
    which describe situations under which certain actions are actually performed.-->

## Overview

!!! note "On `Overview`"

    Form

    : The overview is free form,
    but preferably short
    (as many descriptions will follow).

    !!! quote "Pseudo-example"

        We give actions the structure of serial-parallel graphs
        such that computation can be parallelised.
        This involves splitting up the state into several parts
        and recombine results of what we shall call
        _action primitives._

## Action labels

!!! note "On `Action labels`"

    We first define a Juvix type of action labels.
    This type is required to be a record type or an algebraic data type
    for the purposes of the Anoma specification.
    The constructors of this type are called _action tags,_
    in analogy to _message tag._

    ??? info "Action labels determine unique action effects: _∀ label ∃! effect_"

        The action label alone has to determine
        the ensuing action effect,
        i.e.,
        how the state is to be updated,
        which list of messages has to be added to the send queue,
        what set of engines is to be spawned, and
        the changes to the timer list of the engine environment.
        Note that the action label has arguments that carry non-trivial data.

        👉 _The action tag parameters should be "minimal"!_

        The rule of thumb is that
        for each parameter that you may consider to add to an action label,
        consider to move it to the type of
        [[Engine Dynamics Template#matchable-arguments|matchable arguments]]
        or arbitrary
        [[Engine Dynamics Template#precomputation-results|precomputation results]].

    Conceptual structure

    :   Each action tag should have a small
        description of what the effects of the associated action(s) are,
        in broad terms, and a specific example term of the action label type.
        Ideally,
        the action tag alone determines a single action,
        because the guards should take care of any case distinctions;
        however, there may be exceptions to the rule.

    Form

    :   The form is similar to that of
        the message datatype of
        [[Engine Environment Template#messages|engine environments]].

    :   - We first give the Juvix code of
          the action label datatype
          named `[EngineFamilyName]ActionLabel`
          with auxiliary code in a `??? note "Auxiliary Juvix code"` admonition.

    :   - Then we have
          one sub-subsection for each action tag of the Juvix datatype,
          with a level three heading  `### [Action Tag ⟨𝑖⟩]`.
          In these sub-subsections, we have the following.

          Action tag code snippet

          : We first have the code snippet of the constructor,
          quoting the respective portion of the Juvix datatype.

          Description

          : We describe in broad terms of the associated action.[^3]

          Example term

          : We give an example term.

          Action effects

          : We describe the action effects in more detail,
          using a definition list for each of the following "terms":
          state update,
          messages to be sent,
          engines to be spawned,
          timer updates.

    Goal

    : An understanding of the purpose of the actions that action labels describe,
    without the need to consult later sections.

    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            type someActionLabel :=
              | -- --8<-- [start:doThis]
                doThis String
                -- --8<-- [end:doThis]
            ;
            type anotherActionLabel :=
              | doThat String
            ;
            ```

        ```juvix
        type TemplateActionLabel :=
          | -- --8<-- [start:doAlternative]
            doAlternative (Either someActionLabel anotherActionLabel)
            -- --8<-- [end:doAlternative]
          | doBoth (Pair someActionLabel anotherActionLabel)
          | doAnotherAction String
        ;
        ```

        ### doAlternative

        !!! quote ""

            --8<-- "./engine_dynamics.juvix.md:doAlternative"

        We perform one of the two altertives,
         depending on user input and randomness—`coming soon™`.

        ```juvix
        module do_alternative_example;

        doAlternativeExample : TemplateActionLabel :=
          doAlternative (prelude.Left (doThis "do it!"));

        end;
        ```

        #### Either.Left

        The first alternative does _this._

        State update

        : The state is unchanged as the timer will have all information necessary.

        Messages to be sent

        : No messages are added to the send queue.

        Engines to be spawned

        : We shall create a new engine.

        Timer updates

        : We set a timer for 10 seconds to check up on the spawned engine
          (although that should not be necessary as
           it will send messages as the first thing after spawning).

        #### Either.Right

        […]

        ### doBoth

        […]

        ### doAnotherAction

        […]

## Matchable arguments

!!! note "On `Matchable arguments`"

    Matchable arguments are inspired by pattern matching;
    e.g., in
    [`receive do`-statements](https://hexdocs.pm/elixir/main/processes.html#sending-and-receiving-messages)
    in Elixir,
    we may match a subset of the arguments of a message tag.
    The type of matchable arguments defines
    which arguments possibly will be matched.
    Note that some ímportant arguments may already be covered by
    the arguments of the action label.

    Form

    : A Juvix algebraic datatype followed by documentation,
      with one level three heading `### [Matched argument ⟨𝑗⟩]`
      for each kind of matching mechanism
      where we have the code snippet,
      a description,
      and an example.


    Goal

    : Get an overview of which arguments we want to pass to the action function
      besides the action label.

    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            syntax alias thisOneNatFromAllMessages := Nat;
            ```

        ```juvix
        type TemplateMatchableArgument :=
          | -- --8<-- [start:messageOne]
            messageOne thisOneNatFromAllMessages
            -- --8<-- [end:messageOne]
          | messageTwo thisOneNatFromAllMessages
          | -- --8<-- [start:someThingFromAMailbox]
            someThingFromAMailbox String
            -- --8<-- [end:someThingFromAMailbox]
        ;
        ```

        We only match a natural number from messages
        and occasionally from a mailbox.

        ### messageOne

        !!! quote ""

            --8<-- "./engine_dynamics.juvix.md:messageOne"

        We compute a natural number from the arguments of message one.

        ```juvix
        module message_one_example;

        messageOneExample : TemplateMatchableArgument := messageOne 1;

        end;
        ```

        ### messageTwo

        […]

        ### someThingFromAMailbox

        !!! quote ""

            --8<-- "./engine_dynamics.juvix.md:someThingFromAMailbox"

        We also match a message from a message that
        we had stored in a mailbox.
        See the section on pre-computation results
        for more on how we remember which messages
        we will remove from which mailbox.

        ```juvix
        module some_thing_from_a_mailbox;
          someThingFromAMailboxExample : TemplateMatchableArgument :=
            someThingFromAMailbox "Hello World!";
        end;
        ```

## Precomputation results

!!! note "On `Precomputation results`"

    Guard evaluation may involve non-trivial computation
    that should not have to be repeated in
    the computation of the actions effects.
    Thus,
    we have a third input for action functions,
    which is meant to relay any precomputation results
    beyond matching and label computation.
    Often,
    this parameter will contain information
    for how to update the environment.

    Form

    : A type definition with an explanation of its purpose.
      The pattern is the usual one:
      first the Juvix code,
       a sub-section structure that reflects the type structures,
       and finally, for each data item,
       a code snippet, an explanation, and an example.

    Goal

    : Get an overview of non-trivial computations performed by guards.


    !!! quote "Pseudo-example"

        ??? note "Auxiliary Juvix code"

            ```juvix
            syntax alias someMessageType := undef;
            ```

    ```juvix
    type TemplatePrecomputationEntry :=
      | -- --8<-- [start:deleteThisMessageFromMailbox]
        deleteThisMessageFromMailbox someMessageType Nat
        -- --8<-- [end:deleteThisMessageFromMailbox]
      | closeMailbox Nat
    ;

    TemplatePrecomputation : Type := List TemplatePrecomputationEntry;
    ```

    Often, the guard detects that we can close a mailbox
    and that we have to add a message to a mailbox.
    Note that we have a list of `TemplatePrecomputationEntry`-terms
    as precomputation result
    and that we describe the latter in more detail.

    ### deleteThisMessageFromMailbox

    !!! quote ""

        --8<-- "./engine_dynamics.juvix.md:deleteThisMessageFromMailbox"

    We delete the given message from the mailbox with
    the mailbox ID.

    ```juvix
    module delete_this_message_from_mailbox;

    deleteThisMessageFromMailboxExample : TemplatePrecomputationEntry :=
      deleteThisMessageFromMailbox undef 1;
    end;
    ```


<!--ᚦplease keep this¶
!!! warning "Execution time may be unbounded (in V2)"

    New events are "muted" for the time of
    guard evaluation and action execution.
    The only envisaged way around this is
    the specification of a "hard" maximum duration of action processing,
    after which the action processing is terminated with a timeout,
    and a previously specified default value is returned
    (typically also indicating the occurrence of the timeout).
    However,
    this is not part of V2 specs.
-->

## Guards


!!! note "On `Guards`"

    For each guard of the engine family,
    we provide a guard description.
    For each guard,
    we have one sub-section `### [Guard ⟨guard 𝑖⟩]`
    for each of the guards,
    which contains
    a short description
    of which actions are enabled under which conditions
    by [guard 𝑖].
    Then we give the actual code,
    including code comments.

    Conceptual structure

    :   We essentially need a decision tree, flow chart, or similar for

        - how to determine whether this guard enables actions and then which ones

        - describe the action label, matched arguments,
          and pre-computations results for each of the cases;
          for the latter,
          we may describe how or when they are computed along the way.

    Form

    :   There are three parts:

        [Flowchart](https://en.wikipedia.org/wiki/Flowchart)

        : The flowchart illustrates the guard logic.
        The terminal nodes are the action labels.
        Intermediate nodes describe matching of arguments
        and precomputations that are performed.

        ??? info "Recap flowchart and mermaid"

            Recall that decision nodes are diamond shaped (`{ decision node text }`);
            we (ab-)use rectangular boxes to describe matching of arguments
            or other computations
            (`[ processing node text ]`)
            and the final guard output
            is summarised in terminal nodes
            (`([matched arguments,  action label, precomputation result])`),
            which Mermaid calls "stadiums".

        Flow chart explanation

        : An English language description of the guard/code in broad terms.

        Juvix code

        : The actual guard function code, including code comments
        with additional documentation.

    Goal

    : The flowchart should illustrate at a glance
    how actions are enabled by this guard.
    Moreover,
    the relevant matched arguments and precomputation results
    are named.

    !!! quote "Pseudo-example"

        ### messageOneGuard

        ```mermaid
        flowchart TD
            C{messageOne<br>received?}
            C -->|Yes| D[enabled<br>n := argTwo<br>m := argThree ]
            C -->|No| E[not enabled]
            D --> F([doAnotherAction n m])
        ```

        For `messageOne`-messages,
        we do the other action,
        passing the String representation
        of the second and third argument.

        ```juvix
        --- messageOneGuard (see todo)
        guard : Type := undef;
        ```

        !!! todo "fix/add code (with conversion from Nat to String)"

            ```
            messageOneGuard :  Maybe Time
                -> Trigger I H
                    -> EngineEnvironment S I M H
                        -> Maybe (GuardOutput A L X) :=
                        […] ;
            ```

!!! warning "Mermaid restrictions"

    Mermaid has some restriction on how to use markdown by default:

    - [markdown](https://mermaid.js.org/syntax/flowchart.html#markdown-formatting)
	  has to be enclosed into ``"` ‌`` ``‌ `"`` braces;

	- the typewriter style, i.e., `text like this`, seems not easily usable.

    It may be useful to use the [live editor](https://mermaid.live/edit#pako:eNptkMFOwzAQRH9ltSeQ2h-woKgi9AYc6AXFPWztTWIpttHGpkJJ_h0HWglVzGlHejPSzogmWkaFcFbTx5PpSBLsKx3gjx5Hz8NALb8GBmHD7pPtw3wFwXq9md55mKCqOdCxZ3t3lE0AdQ8k7f4UF-svthNmOPzX8RIneKpDTHCuuaKqhYLdTW3jtlAdy9YkFwME8IdbXKFn8eRs-W1ckhoL41mjKqflhnKfNOowF5Ryim9fwaBKknmFEnPboWqoH4rLH5YSV45aIX9B2LoU5fl3vJ8N52-KL2Tj).

<!--ᚦ: [let's keep this one/three lines of Chris's here, just in case]
Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.
-->
<!--ᚦ: let's keep this here for the moment ¶
!!! example

	```mermaid
	flowchart TD
		check{are we below the rate limit ?}
		check -->|yes| A[match hash and »reply to address«]
	    A --> doA(["` time stamp _hash_ _reply to_ `"])
		check -->|no| B(["` no op `"])

	```

	If the rate limit is not surpassed, we answer the request.
	The matched arguments are the hash to be time stamped
	and the address to which we have to respond.

	hash

	:  matched argument


	returnAdress

	:  matched argument


	`juvix`
    ```
    if limitOK() then Some (hash,replyTo) else None ;
    ```
-->

## Action dependencies and conflict resolution

!!! note "On `Action dependencies and conflict resolution`"

    We need to describe how actions should be linearised
    if they are not all concurrent.
    In many cases,
    the conflict relation can be stated no the level
    of action tags.
    The default is the lexicographical ordering.

    !!! info "This is about actions!"

        The relation of conflict is for
        sets of action labels (and not about guards).

    Form

    : Free form, except for that we need the code for
    the conflict resolution function (at the end).

    !!! quote "Pseudo-example"

        We just use the lexicographical ordering.

        !!! todo "fix code"

        ```juvix
        lexicographicalOrdering : Type -> Type := undef;
        ```

## Action function

!!! note "On `Action function`"

    This is essentially well-documented code
    of the actual action function.

    Form

    : One or several code fragments,
      with the action function at the end,
      interlaced with explanatory prose
      and/or documentation in the code.

    !!! quote "Pseudo-example"

        The action function amounts to one single
        case statement.

        !!! todo "fix code"

        ```juvix
        actionFunction : Type -> Type := undef;
        ```

## Engine family summary

!!! note "On `Engine family summary`"

    Finally,
    we give an example of the engine family summary.

    Form

    :   This section is free form,
        _except_ for the family type definition and an example in Juvix.

    !!! quote "Pseudo-example"

        !!! todo "fix example 👇 (undef!)"

        ```juvix
        TemplateEngineFamily : Type := undef;
        ```

        !!! todo "fix example 👇 (undef!)"

        ```juvix
        module template_engine_family;
        templateEngineFamilyExample : TemplateEngineFamily := undef;
        end;
        ```

<!--
### [Action Name ⟨$i$⟩] `{` one such sub-section per guarded action `}`

!!! note

    The description of the actions starts
    with an English language high-level description,
    followed by more detailed descriptions
    of state update, messages to be sent, timers to be set/cancelled/reset,
    and engine instances to be spawned.

    This section may be split into several
    if there are several different cases
    such that each of them deserves a different action label.

### Overview `{` action ⟨𝒊⟩`}`

!!! note

	Some paragraphs of English language prose
	as the author sees fit.

!!! example

	Besides answering the request,
	we have to update the ringbuffer of the mailbox state.

### Code `{` action ⟨$i$⟩ `}`

??? note "show me the code"

    ♢juvix

### [Action label ⟨$i_j$⟩]

#### Purpose `{`⟨$i_j$⟩`}`

!!! note

    We give quick descriptions of the action for this label.

##### State update `{`⟨$i_j$⟩`}`

!!! note

    Describe the state update

!!! example

    The rate limit is constant in the example.

##### Messages to be sent `{`⟨$i_j$⟩`}`

!!! note

    Describe the messages to be sent
    as a list (or a set if you prefer).

!!! example

    We send only a single message.

    - Send the time stamped hash to the requested »reply to« address.

##### Engines to be created `{`⟨$i_j$⟩`}`

!!! note

    Describe the engines to be created.

!!! example

    No engines are created.

##### Timers to be set/cancelled/reset `{`⟨$i_j$⟩`}`

!!! note

    Describe the engines timers to be set/cancelled/reset.

!!! example

    The time stamping server does not need to set any timers.

## Concurrency, conflict, mutual exclusion. `{` v2' `}`

!!! note "Coming soon™"

    Finally, we need to define the relations of
    concurrency, conflict, mutual exclusion
    between action labels.

-->
<!-- footnotes -->

[^0]: The action labels will be relevant to
      give engine systems a
      [labelled transition system](https://en.wikipedia.org/?title=Labelled_transition_system&redirect=yes)
      semantics,
      which in turn is necessary to be able to check against
      [temporal logic](https://en.wikipedia.org/wiki/Temporal_logic)
      properties.


[^1]: The specification pages impose
      a linear order on guards / action labels;
      however,
      this is independent of
      any conflict resolution strategies.

[^2]: The only exception may be some messages
      that are prescribed by the [[Application Architecture]]
      and similarly actions.<!-- todo: well, where do we have those?-->

[^2']: Eventually,
    we may want to describe each action
    as a [series-parallel graph](https://en.wikipedia.org/wiki/Series%E2%80%93parallel_graph)
    of _action primitives;_
    the main rationale is fostering code re-use,
    but the potential for parallel execution deserves mention as well.
    Finally,
    in some situations,
    we can avoid sending messages to "self".
    Thus,
    you _should_ define action primitives if they naturally arise.

[^3]: The action may be structured,
for example there may
be alternatives or sequences of "sub-actions".
If the action has non-trivial structure,
the structure of this sub-subsection should reflect
the structure of the remainder of the sub-section.
One way to structure is to have a set of "sub-actions"
with a conflict resolution strategy.
