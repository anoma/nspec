---
icon: octicons/gear-16
search:
  exclude: false
---

# On Engines in the Anoma Specification

## Introduction

In rough analogy to the actor model,
where systems consist of actors that communicate via message passing,
every Anoma instance consists of a finite collection of
_engine instances_ that communicate by sending messages to each other.
The behavior of each engine instance
is determined by a _state transition function_ that is
invoked whenever an event occurs at the engine instance,
typically, the arrival of a new message.[^1]
The most important fact is that
the Anoma specification describes 
a fixed finite number of _state transition functions_ 
such that
the behavior of every (correct and non-faulty) engine instance in Anoma
is determined by exactly one of these _state transition functions_.
We dub the equivalence class of engine instances that share 
the same _state transition function_ an _engine type_.

We now describe in more detail the "internal" structure of
each engine instance; this is also a deliberate design choice.
The, we describe how the corresponding engine type can be described.

[^1]: We also will allow for elapsing of timers,
which is a technical detail concerning the handling of 
local time in engine instances.
The role of the template is the organization of 
the specification of engine types and their engine instances.

## On the local information at engine instances

Each engine instance, at any given point in local time,
has local information, namely 

- its identity, given by a pair of
    - an external identity and
    - an internal identity

- its mailboxes that store received messages, represented by

  - a finite set of mailbox identifiers (MID for short), typically non-empty

  - a map from these mailbox identifiers to pairs of
    - a list of messages that were sent to the MID but not processed yet-the associated mailbox
    - an optional mailbox-specific state (for quick processing of incoming messages)

- a finite set of _named acquaintances_,[^2] represented by
    - a finite set of names
    - a map from these names to the identities of the acquaintances

- memory for previously set timers, given by 
    - a finite set of timer handles
    - a map from these timer handles to the requested notification time

- optionally,  memory for names of spawned engines that do not have a
  cryptographic id yet

- engine-specific local state
- the current time 

The engine's identity is unchangeable,
but a new "continuation engine" could be spawned with a new identifier.




[^2]: Here, we borrow actor terminology.

## On engine types

An engine type is in bijective correspondence to a function that
describes how every instance that is basen on this function behaves.
It has a number of inputs, which belong to one of three categories:

- information that is not changed (as part result of mere state transition
  function):
    - the cryptographic identifier
- specific information about the event that has occured
    - for a message, the time of arrival and the actual message
    - for a timer that has elapsed, the "handle" of the timer
- all other local information (as described above)

As this funcion is strongly typed in the formal model, 
the engine type thus determines a list of types, which seems long.
Thus, let us "annotate" the above list.

> - an {engine independent type for the} identity, namely a pair of
>     - an external identity {type} and
>     - an internal identity {type}
> - {types for} mailboxes that store received messages in a list, in more detail
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
  >   - a map from names to the idenetities of an engine instance {we have all
  >     those types already}
> - a local clock {we assume one and we do not have to do anything here}
> - memory for previously set timers (that are still relevant) {a type of `timer
>   handles`}
> - memory for spawned process that do not have a cryptographic identity yet
>   {here we should probably just re-use the name type for acquaintances}
> - engine-specific local state {the one type `state` that is "really" specific
>   to each engine}

Besides updates to the changeable data, the transition function produces

- requests for spawning new processes
- the messages to be sent
- the timers to be set on the clock
