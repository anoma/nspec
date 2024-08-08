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

    To complete the definition of an engine family,
    we have to define a set of guarded actions.

!!! warning "Juvix protocol-level types"

    We also need to write (and import)
    protocol-level type descriptions.
    These are two type declarations.

    Protocol-level message type

    : The name of the message type is the name of the protocol in which the engines take part,
    i.e., `Anoma` for the Anoma specification,
    followed by `ProtocolMessage`.
    This is an algebraic data type with one constructor per engine family
    that takes as argument a message of the respective engine family.
    
    Protocol-level environment type

    : Similarly, we have a type as above, but with `ProtocolEnvironment` instead of `ProtocolMessage`, and constructors taking environments from the respective engine family.

    See the file `engine_protocol_type.juvix`.

## Overview

!!! note 

    We want a broad overview of how the guarded actions
    relate to each other and a descriptio of their purposes.
    The specification necessarily presents
    a list of guarded actions
    and for each guarded action one guard, one action,
    one or several action labels for the action.

    Form

    : free form

## Action labels

!!! note

    We have to define a type of action labels.
    This type may be arbitrarily complex,
    in principle.
    It should only be a nesting of record types
    or algebraic data types.
    Each action label should have a small
    description of what the action performs
    in broad terms.
    If somehow possible,
    the section structure of the
    [[Engine Dynamics Template#action-labels|Action labels section]]
    should reflect the structure of the type of action labels.

!!! warning

    The action label alone determines
    the state update function.
    In other words,
    matched arguments and precomputation results
    are for convenience and improved code quality.

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
      | doAlternativeOne (Either someActionLabel anotherActionLabel)
      | doAlternativeTwo (Pair someActionLabel anotherActionLabel) 
      | doAnotherAction String
    ;
    ```

    The corresponding structure would be the one of the last type.

    ### doAlternativeOne

    does this by 

    #### Either.Left `{` optional `}`

    either this
    
    #### Either.Right  `{` optional `}`

    or that

    ### doAlternativeTwo

    does that by 

    #### first  `{` optional `}`

    doing that

    #### second  `{` optional `}`

    and also that
    
    ### doAnotherAction

    the third kind of action

## Matchable arguments

!!! note

    Matchable arguments are inspired by pattern matching;
    e.g., in
    [`receive do`-statements](https://hexdocs.pm/elixir/main/processes.html#sending-and-receiving-messages)
    in Elixir,
    we may match a subset of the arguments.
    The type of matchable arguments defines
    which arguments possibly will be matched.
    
    Form

    : An algebraic data type or record type followed by a definition list
    that describes for each constructor the action labels that are relevant.


## Precomputation results

!!! note

    Guard evaluation may involve non-trivial computations,
    which should not have to be repeated in
    the associated action.
    Thus,
    we have a third input for actions,
    which are arbitrary precomputation results.

    Form

    : A type definition with an explanation of the purpose.

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
