---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - engine
  - mailbox
  - engine-instance
  - engine-type
  - guarded-action
  - engine-acquaintances
---

# On Engines in the Anoma Specification

## Introduction: on actors and engine instances

The Anoma specification is inspired by the actor model[^3]
where systems consist of _actors_ that communicate via message passing.
An Anoma node instance is modelled as a finite[^4] collection of
_engine instances_ that communicate by sending messages to each other.
The behaviour of each engine instance—i.e., 
how it reacts to receiving a message in 
the context of previously sent messages—is
determined by a _state transition function,_
reminiscent of the next-state function of
[finite state machines](https://en.wikipedia.org/wiki/Automata_theory#Formal_definition) 
(or rather [Moore machines](https://en.wikipedia.org/wiki/Moore_machine#Formal_definition)), 
defined formally as an [Isabelle/HOL-locale](https://github.com/anoma/formanoma/blob/1b9fa7558ce33bb4c2e4d31277255cdeabbc59b5/Types/Engine.thy#L215),
and is explained in more concrete terms in
the guarded action template below. <!-- needs updating -->
The state transition function is invoked
whenever an event (in the sense of the actor model theory) is
triggered at the engine instance,
typically, by the arrival of a new message[^1];
the result of applying the state transition function to
the local state and the event trigger describes 
not only the state update of the engine instance, 
but also which further actions need to be taken: 
sending of messages, setting timers, and spawning new engine instances.

Crucially,
the Anoma specification describes
a _fixed_ finite number of state transition functions
such that
the behaviour of every (correct and non-faulty) engine instance in an Anoma instance
is determined by exactly one of these state transition functions.<!-- add footnote to engine system locale ["axiom" state_partition](https://github.com/anoma/formanoma/blob/915039faa7cfe77c2998b309ef65b671e604fead/Types/Engine.thy#L192) -->
<!-- this be moved elsewhere
!!! definition 
¶
	We call the set of all engine instances that share the same state transition function the _engine type_ of the state transition function.
-->
We start by describing in more detail the "internal" structure of
each engine instance, and the accompanying design choices.
With that in place,
we then describe state transition function in more detail
before we finally come to how we actually will specify state transition functions in the anoma specification via guarded actions.
<!-- Then, we describe how the corresponding engine type can be described. -->

## On the local data of engine instances

Each engine instance has the following local data that is directly and
exclusively accessible at any given moment (in local time):

- its _identity_, given by a pair of

    - an [[Identity#external-identity|external identity]] and
    - an [[Identity#internal-identity|internal identity]]

- its mailboxes that store received messages, represented by a pair of

    - a finite set of _mailbox identifiers_ (**MID** for short),
    typically non-empty
      
    - a function that maps mailbox identifiers to pairs of
		- a list of messages that were sent to the MID but not processed yet
		- an optional mailbox-specific state (for quick processing of incoming messages)

  - a finite set of _named acquaintances_[^2] represented by
    - a finite set of names
    - a map from these names to the
	  [[Identity#external-identity|external identities]] of the acquaintances

- memory for previously set timers, given by
    - a finite set of timer handles
    - a map from these timer handles to the requested notification time

- memory for names of spawned engines that 
  do not have a cryptographic ID yet

- engine-specific local state

- the current time 

The engine's identity is unchangeable,
but a new *"continuation engine"* could be spawned with a new identifier.

## On transition functions

!!! todo

	spell out the formal in english

## Transition functions via guards and actions =: guarded actions

The Anoma specification defines transition functions
via a set of guarded actions.
The word `guarded` is taken from Dijkstra's 
[_guarded_ command language (ɢᴄʟ)](https://en.wikipedia.org/wiki/Guarded_Command_Language),
`action` is taken from Lamport's 
[temporal logic of _actions_ (ᴛʟᴀ⁺)](https://lamport.azurewebsites.net/tla/tla.html),
and indeed, guarded actions are a mix of the two;
the notion of action (together with local data) allows us to
express properties in the temporal logic [ᴄᴛʟ*](https://en.wikipedia.org/wiki/CTL*),
while guards emphasise that actions have clear pre-conditions,
and we may also use [weakest-precondition calculus](https://en.wikipedia.org/wiki/Predicate_transformer_semantics),
e.g., for deriving invariants.

<!--
The basic idea of guarded actions is to split up
the set of possible inputs of the state transition function into
a finite number of cases, 
each of which corresponds to an _event kind_—very much like
the transitions of a [Petri net](https://en.wikipedia.org/wiki/Petri_net#Execution_semantics)
can be "unfolded" into an [event structure](https://dl.acm.org/doi/abs/10.5555/898126),
where events are _occurrences of transitions_ of the original net.
-->
The basic idea of guarded actions is to describe 
the state transition function in a modular way
such that each (non-trivial) state transition corresponds to 
the execution of (at least) one guarded action.[^6]
The guard of a guarded action specifies the precondition of the action,
which describes what state changes should happen when the guard is triggered.
However,
guarded actions may be concurrent or in conflict with each other,
and this situation need to be handled with care.
The details of guarded actions are explained in the [[Guarded Engine Template]].

## On engine types

An engine type is in bijective correspondence to a function that
describes how every instance that is based on this function behaves;
we may just speak of an engine type as if it was a function.
This function takes as input all local data of engine instances. 
Each item of local data falls into one of the following three categories:

- information that is not changed (as part result of mere state transition):
    - the cryptographic identity
- specific information about the event that has occurred
    - for a message, the time of arrival and the actual message
    - for a timer that has elapsed, the _handle_ of the timer
- all other local data (as described above in the section
  `On the local data of engine instances`)

<!-- 

As this function is strongly typed in the formal model / in juvix, 
the engine type thus determines a list of types, which seems long.
Thus, let us "annotate" the above list.



!!! todo

	clean up the following annotated quote (ignore for the review for the moment) 🙏

> - an {engine independent type for the} identity, namely a pair of
>     - an external identity {type} and
>     - an internal identity {type}
> - {types for} mailboxes that store received messages in a list in more detail
>   - a finite set of mailboxes, typically non-empty {from a finite set of types
>     for mailbox contents---not to be confused with mailbox types}
>   - a map from (engine-relative) mailbox identifiers to the above mailboxes
>     {so a function type `mailbox identifier type` => `mailbox type list`}
>   - optionally, each mailbox may have a mailbox-state {i.e., the function type
>     is actually `mailbox identifier type` => `(mailbox state type) * (mailbox
>     type list)`}
> - a finite set of _acquaintances_ (borrowing actor terminology), in more
>   detail
  >   - a finite set of names {hence a type `ac_name`}
  >   - a map from names to the identities of an engine instance {we have all
  >     those types already}
> - a local clock {we assume one, and we do not have to do anything here}
> - memory for previously set timers (that are still relevant) {a type of `timer
>   handles`}
> - memory for spawned processes that do not have a cryptographic identity yet
>   {here we should probably just re-use the name type for acquaintances}
> - engine-specific local state {the one type `state` that is "really" specific
>   to each engine}

-->

Besides updates to the changeable data, the transition function produces

- requests for spawning new engines
- the messages to be sent
- the timers to be set on the clock


## The conceptual structure of each Engine Type page in the specs

As a short synopsis, the structure of each engine type page 
starts with a big picture, some examples, and then the details.
A table of contents has the following structure.

- engine type name (e.g., _Auctioneer_)
  - purpose {very big picture}
  - list of engine-specific types
    - local state
	- message types received and sent
    - mailbox state types (for optimisations)
  - message sequence diagram(s) {specific example(s)}
  - conversation diagram {big picture}
    - conversation partners
        - partner A
    		- incoming 
	    	    - A1
		        - ...
		        - Anₐ
      		- outgoing 
                - A1
 		        - ...
    		    - Amₐ
	    - ...
	    - partner X
	        - incoming 
	            - X1
     		    - ...
	    	    - Xnₓ
		    - outgoing 
		        - X1
    		    - ...
	    	    - Xmₓ
  - guarded actions {now for the details}
    - guarded action α1 (e.g., receive bid)
  	    - guard α1 {`local data * trigger → arguments option`}
	    - action α1 {`local data * arguments → local data update * sends * timers * spawns`}
	        - local data update {prose}
            - messages to be sent {prose}
		    - timer to be set {prose}
		    - engines to be spawned {prose}
	- ...	
    - guarded action αk (e.g., finalise auction)
  	    - guard αk {`local data * trigger → arguments option`}
	    - action αk {`local data * arguments → local data update * sends * timers * spawns`}
	        - local data update {prose}
            - messages to be sent {prose}
		    - timer to be set {prose}
		    - engines to be spawned {prose}

## Template files


??? "Engine template"

    !!! info 

        The following template can be found in the `overrides/templates/engine-template.md` file.
    

    --8<-- "./../overrides/templates/engine-template.md:6"

??? "Guarded action template"


    !!! info 

        The following template can be found in the `overrides/templates/guarded-action-template.md` file.

    --8<-- "./../overrides/templates/guarded-action-template.md"


---

<!-- footnotes -->

[^1]: We also will allow for elapsing of timers,
which is a technical detail concerning the handling of 
local time in engine instances.
The role of the template is the organisation of 
the specification of engine types and their engine instances.

[^2]: Here, we borrow actor terminology.

[^3]: At the time of writing V2 specs, further relevant sources are *Selectors:
Actors with Multiple Guarded Mailboxes*[@selectors-actors-2014] and *Special
Delivery: Programming with Mailbox Types*[@special-delivery-mailbox-types-2023].
We shall refer to the latter as _mailbox usage_ types to avoid a name clash with
the type of messages that are contained in mailboxes.

[^4]: The specification does not fix any bound on 
	the number of engines in existence.

[^5]: Note that in TLA⁺, pre-conditions of actions are
	present in the guise of the `ENABLED` predicate. 

[^6]: Arriving messages that do not trigger any "non-trivial" guarded action
	are added to the mailbox they are addressed,
	time is incremented by a default delay, and nothing else changes.


