---
icon: octicons/gear-16
search:
  exclude: false
---

# On Engines in the Anoma Specification

## Introduction

The Anoma specification is inspiredy by the actor model,[^3]
where systems consist of actors that communicate via message passing:
every Anoma instance is considered as a finite[^4] collection of
_engine instances_ that communicate by sending messages to each other.
The behavior of each engine instance—i.e., 
how it reacts to receiving a message in 
the context of previously sent messages—is
determined by a _state transition function_.
The latter is invoked whenever an event occurs at the engine instance,
typically, the arrival of a new message.[^1]
The most important fact is that
the Anoma specification describes 
a _fixed_ finite number of state transition functions 
such that
the behaviour of every (correct and non-faulty) engine instance in an Anoma instance
is determined by exactly one of these state transition functions.
We dub the equivalence class of engine instances that share 
the same state transition function an _engine type_.

We now describe in more detail the "internal" structure of
each engine instance; this is also a deliberate design choice.
<!-- Then, we describe how the corresponding engine type can be described. -->

## On the local data of engine instances

Each engine instance, at any given moment (in local time),
has the following local data (directly and exclusively accessible):

- its _identity_, given by a pair of
    - an [[External Identity|external identity]] and
    - an [[Internal Identity|internal identity]]

- its mailboxes that store received messages, represented by a pair of

  - a finite set of _mailbox identifiers_ (MID for short),
	typically non-empty
  - a function that maps mailbox identifiers to pairs of
    - a list of messages that were sent to the MID but not processed yet
    - an optional mailbox-specific state (for quick processing of incoming messages)

- a finite set of _named acquaintances_,[^2] represented by
    - a finite set of names
    - a map from these names to the
	  [[External Identity|external identities]] of the acquaintances

- memory for previously set timers, given by
    - a finite set of timer handles
    - a map from these timer handles to the requested notification time

- optionally,  memory for names of spawned engines that 
  do not have a cryptographic id yet

- engine-specific local state

- the current time 

The engine's identity is unchangeable,
but a new "continuation engine" could be spawned with a new identifier.


## On engine types

An engine type is in bijective correspondence to a function that
describes how every instance that is based on this function behaves;
we may just speak of an engine type as if it was a function.
This function takes as input all local data of engine instances. 
each item of local data falls into one of the following three categories:

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

	clean up the following annonated quote (ignore for the review for the moment) 🙏

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

- requests for spawning new processes
- the messages to be sent
- the timers to be set on the clock

## Transition functions via guarded actions

The Anoma specification defines transition functions
via a set of guarded actions.
The word `guarded` is taken from Dijkstra's 
[guarded command language (ɢᴄʟ)](https://en.wikipedia.org/wiki/Guarded_Command_Language),
`action` is taken from Lamport's 
[temporal logic of actions (ᴛʟᴀ⁺)](https://lamport.azurewebsites.net/tla/tla.html),
and indeed, guarded actions are a mix of the two;
the notion of action (together with local data) allows us to
express properties in the temporal logoc [ᴄᴛʟ*](https://en.wikipedia.org/wiki/CTL*),
while guards emphasize that actions have clear pre-conditions
and we may also use [weakest-precondition calculus](https://en.wikipedia.org/wiki/Predicate_transformer_semantics),
e.g., for deriving invariants.


The basic idea of guarded actions is to split up
the set of possible inputs of the state transition function into
a finite number of cases, 
each of which corresponds to an _event kind_—very much like
the transitions of a [Petri net](https://en.wikipedia.org/wiki/Petri_net#Execution_semantics)
can be "unfolded" into an [event structure](https://dl.acm.org/doi/abs/10.5555/898126).
However,
guarded actions may be concurrent or in conflict with each other,
and these situation need to be handled with care.
The details of guarded actions are explained in the [[Engine Template|template]].

## Template files


??? "Engine template"

    !!! info 

        The following template can be found in the `overrides/templates/engine-template.md` file.
    

    --8<-- "./../overrides/templates/engine-template.md"

??? "Guarded action template"


    !!! info 

        The following template can be found in the `overrides/templates/guarded-action-template.md` file.

    --8<-- "./../overrides/templates/guarded-action-template.md"

---

<!-- footnotes -->

[^1]: We also will allow for elapsing of timers,
which is a technical detail concerning the handling of 
local time in engine instances.
The role of the template is the organization of 
the specification of engine types and their engine instances.

[^2]: Here, we borrow actor terminology.

[^3]: At the time of writing V2 specs, further relevant sources are
    [Selectors](https://dl.acm.org/doi/10.1145/2687357.2687360) and
	[mailbox types](https://simonjf.com/writing/pat.pdf);
	we shall refer to the latter as _mailbox usage_ types
	to avoid a name clash with
	the type of messages that are contained in mailboxes.

[^4]: The specification does not fix any bound on 
	the number of engines in existence.

[^5]: Note that in TLA⁺, pre-conditions of actions are
	present in the guise of the `ENABLED` predicate. 
