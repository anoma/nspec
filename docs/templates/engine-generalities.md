# On engines in the Anoma specification

## Introduction

In rough analogy to the actor model,
where systems consist of actors that communcate via message passing,
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

## On the lcoal information at egnine instances

Each engine instance has
- an identity, namely a pair of
  - an external identity and
  - an internal identity
- mailboxes that store received messages in a list, in more detail
  - a finite set of mailboxes, typically non-empty
  - a map from (engine-relative) mailbox identifiers to the above mailboxes
  - optionally, each mailbox may have a mailbox-state
- a finite set of _acquaintances_ (borrowing actor terminology), in more detail
  - a finite set of names
  - a map from names to the idenetities of an engine instance
- a local clock
- memory for previously set timers (that are still relevant)
- memory for spawned process that do not have a cryptographic identity yet
- engine-specific local state

## On egnine types

An engine type is in bijective correspondence to a function that
describes how every instance that is basen on this function behaves.
It has a number of inputs, which belong to one of three categories:

- information that is not changed (as part result of mere state transition function):
  - the cryptographic identifier
- specific information about the event that has occured
  - for a message, the time of arrival and the actual message
  - for a timer that has elapsed, the "handle" of the timer
- all other local information (as described above)

As this funcion is strongly typed in the formal model, 
the engine type thus determines a list of types, which seems long.

!!! todo

	add the details when the list above concerning what each engine should have as local state is fixed
