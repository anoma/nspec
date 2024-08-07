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

    We need also import (and for the moment write)
    protocol-level type descriptions.

    !!! todo
    
        add the file and "empty" definitions

## Overview

!!! note 

    Give a broad overview of how the guarded actions
    relate to each other and their purposes.
    The specification necessarily presents
    a list of guarded actions and/or action labels.

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
    the section structure of 
    [[Engine Dynamics Template#action-labels|this section]]
    should reflect the structure of the main type
    of action labels.

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
      | alternativeOne (Either someActionLabel anotherActionLabel)
      | alternativeTwo (Pair someActionLabel anotherActionLabel) 
      | anotherAction String
    ;
    ```

    The corresponding structure would be the one of the last type.

    ### alternativeOne

    does this by 

    #### Either.Left `{` optional `}`

    either this
    
    #### Either.Right  `{` optional `}`

    or that

    ### alternativeTwo

    does that by 

    #### first  `{` optional `}`

    doing that

    #### second  `{` optional `}`

    and also that
    
    ### anotherAction 

    the third kind of action
    
!!! todo "ᚦ continue here"

    👇

## [Guarded Action ⟨$i$⟩] `{` $1<i<k$, i.e. $k$ such sections `}`

!!! note

    For each guarded action of the engine family,
    we provide a guard description
    and and action description.

### Purpose

!!! note

    We want a high level description of
    which conditions enable actions
    and the effects of each potential action to be performed.

    Form

    : Some short paragraphs as a summary, ideally just one.
    More details will follow in
    the respective secion(s) on the guard and the action(s).

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
    we want a short description of the conditions that enable actions;
    we may have a case distinction.
    For each case, also if it is just one,
    we need to describe the matched arguments,
    the action label,
    and any other precomputations.
    
    Conceptual structure
    
    : We essentially need a decision tree, flow chart, or similar for
    
    - how to determine whether an action is enabled (and which one), and
    
    - describe the list of matched arguments and pre-computations
    and how they are computed along the way.


    Form
    
    : There are three parts:
    
    1. an (optional?) flow chart that matches the conceptual structure
    where decision are diamonds (`{ decision node text }`),
    we (ab-)use rectangular boxes to describe matching of arguments
    (`[ processing node text ]`), and
    the terminals are "stadium" (`([ action label &  additional args])`).

    2. an English language description of the logic
    that the flow chart illustrates (even in absense of a flowchart) and
    also descriptions of the  matched argument,
    using a [definition list](https://pandoc.org/MANUAL.html#definition-lists)
    as in the example below.

    3. Juvix code of the actual guard function

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
    
    The guard _may_ have a complicated tree-like structure,
    at least one for each "leaf" of the action label data type.
    If there are several natural distinct cases
    each of which corresponds to a different "leaf" of the action label data type,
    then we may want to describe each of these cases.

??? todo "where to put the code ?!"



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



### Overview

!!! note

	Some paragraphs of English language prose
	as the author sees fit.

!!! example

	Besides answering the request,
	we have to update the ringbuffer of the mailbox state.

    ??? "show me the code"

	♢juvix


<!-- ᚦdon't think we need this any more
!!! todo

	simple juvix code example of client server
-->


### Effects

!!! note

	We give quick descriptions of the effects.

#### state update

!!! note

	Describe the state update

!!! example

	The rate limit is constant in the example.

#### messages to be sent

!!! note

	Describe the messages to be sent
	as a list (or a set if you prefer).

!!! example

	We send only a single message.

	- Send the time stamped hash to the requested »reply to« address.

#### engines to be created

!!! note

	Describe the engines to be created.

!!! example

	No engines are created.

#### timers to be set/cancelled/reset

!!! note

	Describe the engines timers to be set/cancelled/reset.

!!! example

	The time stamping server does not need to set any timers.
