# Guarded Action `<` _Name of guarded action- `>` {V2 Template ⊂ V3 Template}

Each guard specifies a predicate that
decides if a certain "action" is enabled
based on local data only;
_moreover,_ in order to allow for typical pattern matching techniques,
we complement the predicate with an output of "matched" arguments.

!!! todo
	
	add juvix type here

In theory,
all guards of an engine are evaluated in parallel,
whenever a new event (e.g., the arrival of a message) occurs;
in practice, for specific cases, one may want to choose 
a more efficient, but equivalent strategy.

In a simple cases,
it is never the case that several guards are enabled at the same time;
however, 
if several guards are enabled,
priorities of guards may be used to resolve unwanted non-determinism. 
It is necessary to mark the non-determinism if it is desired.

Each guard comes with an associated action that is executed
if the guard is satisfied (and has highest priority).

!!! Note

	New events are "muted" for the time of guard and action execution.

## Guard

<!-- this seemed to be outdated 
The following conditions are permissible guards:
- Received a message matching some pattern from another engine
- Received a message (timer elapsed) matching some pattern from my clock

For the time being, guards can check only a single message at once.
-->

`<description of conditions for the action (cf. _event_ in event-driven machine) and the optional argument that are matched if conditions are satisfied>`

Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.

## Action [`<` _ActionName_ `>`]

The action of a guarded action is a function $f_{act}$.
I takes as input
all local data of an engine _and also_
the _arguments_ that are returned by the guard.
In more detail, the list of inputs is

- matched arguments
- the "trigger"
  - message read
  - timer "handle" of elapsing timer
- external + internal id of the engine itself (unchangeable)
- engine-specific local state
- messages or timer information of the trigger
- local time (when guard evalutation started)
- mailbox contents and state
- remembered timers with their elapsing time
- acquaintances of other engines

The output of the action describes

- updates to the above local data (except for identities)
- messages to be sent
- engines to be spawned

Moreover it will be possible to also use randomness 
and "direct" user input. 
Roughly,
the output can depend on randomness and inputs,
possibly interdependenty, 
e.g., if a user is given the chance to override 
playing an engines's purely stochastic strategy 
(in the context of a stochastic game).


!!! todo

	make PR for https://github.com/anoma/formanoma/tree/heindel/engine-locale

A description of the action is necessary,
ideally complemented with juvix code.

!!! todo

	simple juvix code example of client server

### state update

### messages to be sent

### engines to be spawned

### [timers to be set]





