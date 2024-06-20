# `<` _Name of action- `>` on `<` _Name of guard- `>` {V2 Template ⊂ V3 Template}

Each guarded action is a pair of a guard and an action.
The guard specifies a predicate that
decides if the action is enabled,
based on local data only; 
_moreover,_ in order to allow for typical pattern matching techniques,
we complement the predicate with an output of _matched arguments._
The action takes local data and matched argument as input and 
computes 

- the updates to local data
- messages to be sent
- timers to be set, and 
- engines to be spawned.

In theory,
all guards of an engine are evaluated in parallel,
each of which potentially triggers an event,
(e.g., upon  arrival of new  message);
in practice, for specific cases, one may want to choose 
a more efficient, but equivalent strategy.

In many simple cases,
it is never the case that several guards become true;
however, 
if several actions are enabled,
priorities of guards may be used to resolve unwanted non-determinism. 
It is necessary to mark the non-determinism if it is desired.
Each guard comes with an associated action that is executed
if the guard is satisfied (and has the highest priority).

!!! Note

	New events are "muted" for the time of 
	guard evaluation and action execution.

## Guard

<!-- this seemed to be outdated 
The following conditions are permissible guards:
- Received a message matching some pattern from another engine
- Received a message (timer elapsed) matching some pattern from my clock
¶
For the time being, guards can check only a single message at once.
-->

`<description of conditions for the action (cf. _event_ in event-driven machine) and the optional argument that are matched if conditions are satisfied>`

Guards can provide information (similar to pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.

## Action [`<` _ActionName_ `>`]

The action of a guarded action is a function $f_{act}$, 
named `<` _ActionName_ `>` .
I take as input
all local data of an engine _and also_
the _arguments_ that are returned by the guard.
In more detail, the list of inputs is

- matched arguments
- external + internal ID of the engine itself (unchangeable)
- the "event trigger"
  - message received or
  - timer "handle(s)" of elapsing timer(s)
- engine-specific local state
- local time (when guard evaluation started)
- mailbox contents and their optional state (for every mailbox)
- remembered timers with their scheduled time
- acquaintances (known other engine instances)
  - a (finite) map from names to external IDs

The output of the action describes after the event has finished

- updates to the above local data (except for identities and arguments)
- a finite set of messages to be sent
- a finite set of engines to be spawned, setting
  - engine type
  - initial state
  - initial time
  - a name for the process (that is unique relative to the engine)

<!-- This needs to be revisted -->
Moreover, it will be possible to also use randomness 
and "direct" user input. 
Roughly,
the output can depend on randomness and inputs,
possibly interdependently, 
e.g., if a user is given the chance to override 
playing an engines's purely stochastic strategy 
(in the context of a stochastic game).

The full type corresponds to the transition function for
engine _systems_ in the [formal model](https://github.com/anoma/formanoma/blob/915039faa7cfe77c2998b309ef65b671e604fead/Types/Engine.thy#L174-L189).
The engine local state also is in correspondence with the [state map](https://github.com/anoma/formanoma/blob/915039faa7cfe77c2998b309ef65b671e604fead/Types/Engine.thy#L162-L169)
of the formal model.

!!! todo

	establish some proper reciprocal linking scheme here 
	
	<!--
	make PR for https://github.com/anoma/formanoma/tree/heindel/engine-locale
	-->	


A description of the action is necessary,
ideally complemented with juvix code.

!!! todo

	simple juvix code example of client server

!!! todo
	
	add details according to the discussion in the PR,
	see e.g., here https://github.com/anoma/nspec/pull/84#discussion_r1639785764
	

### state update

### messages to be sent

### engines to be spawned

### [timers to be set]





