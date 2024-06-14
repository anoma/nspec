# Actions Xi and Guard Xi {V2 Template ⊂ V3 Template}

Each guard is a predicate that decides if a certain "action" is enabled
based on local information only---whence the name.

All guards of an engine are evaluated whenever a new event occurs.

Ideally, given an event, at most one guard becomes enabled;
if several guards are enabled given an event,
priorities of guards may be used to resolve unwanted non-determinism. 
However, on the level of specs,
it may be useful to mark the non-determinism
provided that any resolution of non-determinism is correct.

Each guard comes with an associated action that is executed
if the guard is evaluated to true (and has highest priority).

!!! Note

	New events are "muted" for the time of guard execution.


## Guard Xi

The following conditions are permissible guards:
- Received a message matching some pattern from another engine
- Received a message (timer elapsed) matching some pattern from my clock

For the time being, guards can check only a single message at once.
`<description of conditions for the action (cf. _event_ in event-driven machine) >`
Guards can provide information (a la pattern-matching) which can then be used in the action. Each guard should come with a specified type `LocalData -> Maybe<T>` where `T` is the data that the guard will bind (pattern-match) out of the local data if (and only if) it matches.
## Action Xi

`<description of "action" cf. Dijkstra's GCL >`

### state update

### messages to be sent

### engines to be spawned

### [timers to be set]





