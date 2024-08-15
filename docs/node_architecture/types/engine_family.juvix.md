---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Engine-Family
- Engine-Instances
- Juvix
---


??? info "Juvix imports"

    ```juvix
    module node_architecture.types.engine_family;
    import node_architecture.basics open;
    ```

# Engine Family Types

## Core types and concepts

This page highlights the essential types and concepts of an engine family in the
Anoma Specification, specifically focusing on writing these families in
[Juvix](https://docs.juvix.org).

Each engine family must declare specific _components_ that each of its member
engine instances will have. For Anoma specifications, the components are:

*Engine Environment*

:   This serves as the execution context for engines. In addition to the local
    state, the engine environment encompasses elements such as the mailbox
    cluster owned by an engine instance and a finite set of acquaintances—other
    engine instances known to the current one that can interact with it.

*Action Function*

:   The function that describes all possible ways in which engines can act, by
    changing their environment, sending messages, spawning new engine instances,
    and update their list of active timers.

*Guards*

:   The finite set of guard functions that describe the conditions under which
    the local state of the engine's instance should change by invoking the action
    function.

*Conflict Solver*

:   The function that resolves conflicts between actions to maximize their
    concurrency.


### Engine family environment

The engine family environment encompasses static information for engine instances in the
following categories:

- A global reference, `name`, for the engine instance.
- Local state whose type is specific to the engine family.
- Mailbox cluster, which is a map of mailbox IDs to mailboxes.
- A set of names of acquainted engine instances. It is implicit that the engine
  instance is acquainted with itself, so there is no need to include its own
  name.
- A list of timers that have been set.

This data is encapsulated within the `EngineEnvironment` type family, which is
parameterised by four types: `S`, representing the local state, `I`,
representing the type of incoming messages to the engine instance, `M`,
representing the type of mailboxes' states, and finally, `H`, representing the
type of handles for timers. These same letters will be used in the rest of the
document to represent these types.

```juvix
type EngineEnvironment (S I M H : Type) :=
  mkEngineEnvironment {
      name : Name ; -- read-only
      localState : S;
      mailboxCluster : Map MailboxID (Mailbox I M);
      acquaintances : Set Name;
      timers : List (Timer H);
};
```

### Engine Behaviours

Each engine processes only one message at a time. The behaviour of an engine is
specified by a finite set of _guards_ and an _action function,_ which determing
how engine react to recevied messages or timer notifications.


#### Guards

Guards are terms of type `Guard`, which is a function type

```
Trigger I H -> EngineEnvironment S I M H -> GuardOutput A L X
```

where  the _trigger_ of type `Trigger I H` is a term that captures the message received or the clock notification. This
trigger can include the received message or timers that have elapsed during
 the engine's operation. Guards return data of type `GuardOutput A L X` if the condition is met.

Recall that the behaviour is described by a set of  guards
and an action function.
The guard is a function that evaluates conditions in the engine environment to determine whether an action should be performed.

The guard function receives, not in any particular order:

- the trigger that caused it to be evaluated,
- the environment of the engine instance, and
- an optional time reference for the starting point of the evaluation of all guards.

Given these inputs,
the guard function determines if the condition for running the action(s) it is guardeding are met.
The action function can compute the effects of actions—not only
changes to the engine environment,
but also which messages will be sent,
what engines will be created,
and how the list of timers is updated.

```juvix
Guard (I H S M A L X : Type) : Type :=
  Maybe Time -> Trigger I H -> EngineEnvironment S I M H -> Maybe (GuardOutput A L X);
```


<!--ᚦleft here for the moment¶
#### Actions

The output of a guard is input for the action function.

- An _action_ of type `Action S I M H A L X O C`, where the new type parameters `O`
  denote the type of outgoing messages, and `C` signifies the type encoding the engine
  instances to be created.
-->

#### Action Function

The input is parametrised by the types for:
local state, incoming messages, mailboxes' state, the output of
guard functions, timer's handles,
matched arguments, action labels, and precomutation result.
The types of the input and output of an action are

- `ActionInput S I M H A L X` and
- `ActionEffect S I M H A L X O C`.

The `ActionInput S I M H A L X ` type is a record that encapsulates the following data:

- A term of type `GuardOutput A L X`, which represents
  - the matched arguments, e.g., from a received message,
  - the action label that determines the action to be performed
  - other (expensive) precomputation results that
    the guard function has already caclulatet.
- The environment of the corresponding engine instance.
- The local time of the engine instance when guard evaluation was triggered.

```juvix
type GuardOutput (A L X : Type) := mkGuardOutput{
     args : List A;
     label : L;
     other : X
};

type ActionInput (S I M H A L X : Type)
  := mkActionInput {
      guardOutput : GuardOutput A L X;
      env : EngineEnvironment S I M H;
      trigger : Trigger I H;
      time : Maybe Time
};
```

The `ActionEffect S I M H A L X O C` type defines the results produced by the
action, which can be

- Update its environment (while leaving the name unchanged).
- Produce a set of messages to be sent to other engine instances.
- Set, discards, or supersede timers.
- Define new engine instances to be created.

```juvix
type ActionEffect (S I M H A L X O C : Type) := mkActionEffect {
    newEnv : EngineEnvironment S I M H;
    producedMessages : List (EnvelopedMessage O);
    timers : List (Timer H);
    spawnedEngines : List C;
};
```

??? info "On creating new engine instances"

    To create new engine instances, we need to specify the following data:

    - A unique name for the new engine instance.

      !!! todo "We have to talk about this"

          !!! quote

              , assuming the system will ensure its uniqueness.

    - The initial state of the engine instance.
    - The corresponding set of guards and the action function.

    The last point is however implicit.

    !!! todo "this forward pointer needs a link"

        ... and so does the next sentence

    In the code,
    we use a type parameter `C` for convenience;
    this parameter has a canonical instantiation for each protocol,
    namely the protocol-level environment type.



If the guard does not give a result,
this means that none of its guarded actions are triggered.

??? info "On the type signature of the guard function"

    In principle, borrowing terminology from Hoare logic, a guard is a
    _precondition_ to run an action. The corresponding predicate is activated by a
    trigger and evaluated within the context of the engine's environment. It then
    returns a boolean when the predicate is satisfied, specifically of type

    ```haskell
    Trigger I H -> EngineEnvironment S I M H -> Bool;
    ```

    However, as a design choice, guards will return additional data of type `GuardOutput A L X` that
    may or may not use the engine environment if the condition is met. Thus, if
    the guard is satisfied, this data (of type `GuardOutput A L X`) is assumed to be passed to the
    action function. Then, if the guard is not satisfied, no data is
    returned.

#### Conflict resolution

Finally, `resolveConflict` is a function that
takes a finite set of action labels as input;
it outputs a list of action label sets
that are pairwise disjoint and whose union is the input set
or is empty,
if conflict resolution fails.
And for each element of the output it should be
that if applied to this element,
it returns the one element list of the set itself.

```
resolveConflicts : Set A -> List (Set A);
```

## Engine families and instances

The `EngineFamily` type encapsulates the concept of engines within Anoma. As defined,
it clears up that engines are essentially a collection of guarded state-transition
functions. Our type for these families is parameterised by a type for their local states,
a type for their incoming messages, a type for its mailboxes' state, a type for returned
data by the guard functions, and a type for outgoing messages.

```juvix
type EngineFamily (S I M H A L X O C : Type) := mkEngineFamily {
  guards : Set (Maybe Time -> Trigger I H -> EngineEnvironment S I M H -> Maybe (GuardOutput A L X));
  action : ActionInput S I M H A L X -> Maybe (ActionEffect S I M H A L X O C);
  resolveConflicts : Set A -> List (Set A);
};
```

??? info "On the use of `Set` for guards in `EngineFamily`"

    In the `EngineFamily` type, we used `Set`
    as it allows for the possibility that
    several guards are processed in parallel.
    However,
    the specification of an engine family must describe
    when guards are to be considered concurrent
    and when they are competing.
    In the latter case,
    we can assign priorties to guards
    to resolve unwanted non-determinism.

!!! todo "rework/adapt the rest of this page"

!!! todo "Do we really need the `Engine` type?"

Additionally, we define the `Engine` type, which represents an engine within a family.
A term of this `Engine` type is referred to as an engine instance. Each engine instance
is associated with a specific name and a family of engines, plus a declaration of its own
execution context, that is, the specific state, mailbox cluster, acquaintances, and timers.

```juvix
type Engine (S I M H A L X O C : Type):= mkEngine {
  name : Name;
  family : EngineFamily S I M H A L X O C;
  initEnv : EngineEnvironment S I M H;
};
```

!!! example

    As an example, we could define an engine family for voting:

    - `LocalStateType` could be a record with fields like `votes`, `voters`, and `results`.
    - The incomming message type might be a coproduct of `Vote` and `Result`.
    - The guarded actions may include actions like:
        - `storeVote` to store a vote in the local state,
        - `computeResult` to compute the result of the election, and
        - `announceResult` to send the result to some other engine instances.

    With each different election or kind of voters, we obtain a new engine instance,
    while the underlining voting system, the voting engine family, remains the same.

!!! note

    Both the `EngineFamily` and `Engine` types are parameterised by several types. When
    not used in the context of a new engine family declaration, these types can be
    replaced by the unit type `Unit`.
