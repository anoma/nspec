---
icon: octicons/project-template-24
search:
  exclude: false
---

??? note "Juvix module"

    ```juvix
    module tutorial.engines.template.engine_dynamics;

    import Stdlib.Data.String open;
    import prelude open;
    ```

# [Engine Family Name] Dynamics

!!! note

    To complete the definition of
    [[Engine Family Types|engine family ⟦engine family name⟧]],
    we have to define its set of
    [[Engine Family Types#guarded-actions|guarded actions]].

    For this, we in particular have
    to define a datatype of _action labels,_
    which describe what actions a member of the engine family can
    perform in response to messages or timer notifications—irrespective
    of the specific circumastances that call for such actions.
    The action labels are complemented by a set of guarded actions,
    which describe situations under which certain actions are actually performed.
    Finally,
    action functions compute the effects of actions
    as [pure functions](https://en.wikipedia.org/wiki/Pure_function)
    (see also [[On LTS semantics of guarded actions]]).

    !!! todo "definition of _engine system_"

        Where do we have the definition of engine system now?

!!! warning "Juvix protocol-level types"

    We also have to write (and import)
    protocol-level type descriptions.
    These are two type declarations.

    Protocol-level message type

    : The name of the message type is the name of the protocol in which the engines take part,
    i.e., `Anoma` for the Anoma specification,
    followed by `ProtocolMessage`.
    This is an algebraic data type with one constructor per engine family
    that takes as argument a message of the respective engine family.

    : 👉 _This type is **the** type used for sending messages._

    Protocol-level environment type

    : Similarly, for engine environments, we have a type as above,
    but with `ProtocolEnvironment` instead of `ProtocolMessage`,
    and constructors taking environments from the respective engine families.

    : 👉 _This type is **the** type used for creating new engine instances._

    See the file `engine_protocol_type.juvix`.
    Note that for the purpose of these two types,
    the [[Engine Family Hierarchy]] is "flattened",
    i.e., the algebraic data type does not encode the hiearchy of engine families.


## Overview

!!! note

    We want a broad overview of how the guarded actions
    relate to each other and a description of their purposes.
    For each guarded action
    we have one guard, one action,
    and one or several action labels.
    The specification pages impose
    a linear order on guarded actions and action labels.

    !!! todo "settle the order business!!!"

        alphabetic vs. conceptual order ?


    Form

    : free form, but preferably short (as many descriptions will follow)

## Action labels

!!! note

    We have to define a type of action labels.
    This type may be arbitrarily complex,
    in principle.
    However,
    for the purposes of the Anoma specification,
    it has to be a record type or algebraic data type
    at the _top level._
    The constructors of this type are called _action tags,_
    in analogy to _message tag._

    ??? warning "Every action label determines the action effect: _∀ label ∃! effect_"

        The action label alone has to determine the ensuing state update,
        the list of message for the send queue,
        the set of engines to be spawned,
        and the changes to the timer list.
        Note that the action tag may take parameters.

        👉 _The action tag parameters should be "minimal"!_

        Thus,
        for each parameter that you may consider to add to an action label,
        consider to move it to the type of
        [[Engine Dynamics Template#matchable-arguments|matchable arguments]]
        or arbitrary
        [[Engine Dynamics Template#precomputation-results|precomputation results]].

    Conceptual structure

    : Each action tag should have a small
    description of what the effects of the associated action are,
    in broad terms.

    Form

    : Often, this may not be the case and we just have
    one sub-section for each action tag.

    Goal

    : An understanding of the purpose of the actions that action labels describe,
    without the need to consult later sections.


!!! Example "Generic Action Label Pattern"

    Consider the following code.

    ```juvix
    type someActionLabel :=
      | doThis String
      ;
    type anotherActionLabel :=
      | doThat String
    ;

    type allLabels :=
      | doAlternative (Either someActionLabel anotherActionLabel)
      | doBoth (Pair someActionLabel anotherActionLabel)
      | doAnotherAction String
    ;
    ```

    The corresponding structure would be the one of the last type.

    ### doAlternative

    We do one of the two.

    #### Either.Left `{` optional `}`

    The first alternative does _this._

    #### Either.Right  `{` optional `}`

    The other alternative does _that._

    ### doBoth

    Here we do both.

    #### first  `{` optional `}`

    Well, we have described _this_ above.

    #### second  `{` optional `}`

    Well, we have described _that_ above.

    ### doAnotherAction

    Finally, we have a third kind of action
    that also has to be documented.

## Matchable arguments

!!! note

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

    : An algebraic data type or record type followed by a definition list
    that describes for each action tag (or, equivalently, each constructor),
    the corresponding action effects,
    in broad terms.

## Precomputation results

!!! note

    Guard evaluation may involve non-trivial computation
    that should not have to be repeated in
    the computation of the actions effects.
    Thus,
    we have a third input for action functions,
    which is meant to relay any precomputation results
    beyond matching and label computation.

    Form

    : A type definition with an explanation of its purpose.

## [Guarded Action ⟨$i$⟩] `{` $1<i<k$, i.e. $k$ such sections `}`

!!! note

    For each guarded action of the engine family,
    we provide a guard description
    and an action description.

### Purpose

!!! note

    We want a high level description of
    which conditions enable actions
    and the effects of each potential action to be performed.

    Form

    : Some short paragraphs as a summary, ideally just one.
    More details will follow in
    the respective secions for the guard and the action labels.

<!--ᚦ: have this here for the moment ¶
!!! example

	The time stamping server has a build in rate limit.
	Time stamping requests are only served
	if the mean time between received requests is within
	bounds that have been fixed at creation.
-->

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

### [Guard ⟨guard $i$⟩]

!!! note

    For each guard
    we want a short description of the conditions that enable its action;
    we may have a case distinction for action labels,
    which may possibly be nested.
    For each case,
    also if it is just one,
    we need to describe
    the action label,
    the matched arguments,
    and any other precomputations.

    Conceptual structure

    : We essentially need a decision tree, flow chart, or similar for

    - how to determine whether the action of the guard is enabled

    - describe the action lable, matched arguments,
    and pre-computations results;
    for the latter, we may describe how or when they are computed along the way.

    Form

    : There are three parts:

    1. a [flowchart](https://en.wikipedia.org/wiki/Flowchart)
    that illustrates the guard logic.
    Recall that decision nodes are diamond shaped (`{ decision node text }`);
    we (ab-)use rectangular boxes to describe matching of arguments
    or other computations
    (`[ processing node text ]`)
    and the final guard output
    is summarized in terminal nodes
    (`([matched arguments,  action label, precompuation result])`),
    which Mermaid calls "stadiums".

    2. Juvix code of the actual guard function

    3. an English language description of the code in broad terms.

    Goal

    : The flowchart should illustrate at a glance
    what action labels the guard may produce as part of its output.

!!! warning

    Mermaid has some restriction on how to use markdown by default:

    - [markdown](https://mermaid.js.org/syntax/flowchart.html#markdown-formatting)
	  has to be enclosed into ``"` ‌`` ``‌ `"`` braces;

	- the typewriter style, i.e., `text like this`, seems not easily usable.

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


## Action `{` possibly several labels !!! `}`

!!! note

    The guard _may_ have a complicated structure,
    which ideally is reflected by the flowchart.
    at least one for each "leaf" of the action label data type.
    If there are several natural distinct cases
    each of which corresponds to a different "leaf" of the action label data type,
    then we may want to describe each of these cases.

??? todo "where to put the code of the action ?!"



 <!--!!! example
¶
	There is always the `no op` opeartion as default,
	which just drops the message.
-->

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

### Overview `{` action ⟨$i$⟩`}`

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
