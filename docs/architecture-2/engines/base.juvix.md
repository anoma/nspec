---
search:
exclude: false
tags:
- engine
- engine-type
- Juvix
---


??? info "Juvix imports"

    ```juvix
    module architecture-2.engines.base;
    import architecture-2.engines.basic-types open;
    ```


# Engine Family Types

## Core Types and Concepts

This page highlights the essential types and concepts needed to define an engine
family in the Anoma Specification, specifically focusing on writing these
families in Juvix. Please refer to the [[Engines in Anoma]] page for a better
overview and motivation of the concept of engines for Anoma.

Each engine family must declare specific components essential to its purpose.
For Anoma specifications, these components include:

- **Local Environment**: This serves as the execution context for engines.
  In addition to the local state, the local
  environment encompasses elements such as the mailbox cluster owned by an
  engine instance and a set of acquaintances—other engine instances known to the
  current one that can interact with it.

- **Guarded Action**: Engines are not merely storage units; they also process
  information and communicate with other engine instances through messages.
  Their behavior is defined by their guarded actions, which are rules or
  state-transition functions accompanied by specific conditions allowing their
  execution when messages are received.

So, let's introduce the type for each of these components.


### Local Environment

The local environment encompasses static information for engine instances in the
following categories:

- A global name or identifier for the engine instance.
- Local state.
- Mailbox cluster, which is a map of mailbox IDs to mailboxes.
- A set of names of acquainted engine instances.
- A list of timers that have been set.

This data is encapsulated in the `LocalEnvironment` type. The `LocalEnvironment` 
type is parameterised by two types: `LocalStateType` and 
`MessageType` representing the local state and message types, respectively.

```juvix
type LocalEnvironment (LocalStateType : Type) (MessageType : Type):= mkLocalEnvironment {
      engineName : Name ;
      localState : LocalStateType;
      mailboxCluster : Map MailboxID (Mailbox MessageType);
      acquaintances : Set Name;
      timers : List Timer;
};
```

For short, we will use the type parameters `S` and `M` to represent 
the type of the local state and message types, respectively.

### Engine Behaviours

In alignment with Actor theories, Anoma's engines function as event-driven state
machines. This implies that our engines respond exclusively to messages stored
in or received by the `mailboxCluster` through their _guarded actions_. As part
of this response, they produce a new state and may have other effects. Each
engine processes only one message at a time, ensuring synchronized operation
during this process.

So with the execution context type defined for an engine family, our next step is
to determine the type for these _guarded actions_. These actions are defined by a
state transition function—the core of an engine's operation—under specific
conditions, known as _guards_. 

First, we need to define the type for state transitions, which uses
`StateTransitionArguments` and `StateTransitionResult` types.

```juvix
StateTransition (S M T : Type) : Type := StateTransitionArguments S M T -> StateTransitionResult S M;
```

A state transition function takes the following arguments:

- The output of the guard function (`Maybe T`), ensuring the guard is satisfied.
- The engine instance's local environment.
- The actual trigger message.
- The time at which the state transition is triggered.

These arguments are encapsulated in the `StateTransitionArguments` record type below.

```juvix
type StateTransitionArguments (S M T : Type)
  := mkStateTransitionArguments {
      inputGuard : T; -- The guard's output
      env : LocalEnvironment S M;
      trigger : Trigger; -- TODO: update
      time : Time; -- The time at which the state transition is triggered
};
```

The `StateTransitionResult` type defines the results produced by a state
transition function. When executing such a function, the engine instance will:

- Update its local state.
- Queue messages for transmission.
- Set timers.
- Define new engine instances to be created.

To create these new engine instances, we need to specify the following data:

- The engine family type.
- The name of the new engine instance.
- The initial state of the engine instance.

This information is encapsulated within the `SpawnedEngine` type.

<!-- Improve the following definition once https://github.com/anoma/juvix/issue
is solved -->

```juvix
type SpawnedEngine : Type := mkSpawnedEngine { 
  need : {S M : Type} -> 
    (engFamily : EngineFamily S M) -> 
    (insName : Name) ->
    S;
};
```

We can now define the `StateTransitionResult` type as follows:

```juvix
type StateTransitionResult (S M : Type)
  := mkStateTransitionResult {
      newEnv : LocalEnvironment S M;
      producedMessages : {T : Type} -> Mailbox T;
      spawnedEngines : List SpawnedEngine;
      timers : List Timer;
};
```

#### Guarded Actions

A guarded action consists of a _guard_ and an _action_. The guard is a function
that evaluates conditions on the engine's local environment to decide if the
action should be executed. The action is a function that updates the local
environment and may include additional effects, as said before, such as setting
timers, messages, and spawning new engines.


```juvix
type GuardedAction (S : Type) (M : Type) := mkGuardedAction {
  guard : {T : Type} -> LocalEnvironment S M -> Maybe T;
  action : {T : Type} -> StateTransition S M T;
};
```

??? info "Notation: Curly braces in guard and action's type signature"

    The curly braces notation used in the type signature of the guard function
    indicates that the type argument `T` can be omitted, as it is inferred from the
    return type.

    Ideally, type `T` should be an implicit field of `GuardedAction`, indicating
    that the action takes input from the guard's evaluation when satisfied. However,
    this is not feasible in Juvix at the moment.

??? info "On the type signature of the guard function"

    In principle, a guard is a predicate that evaluates the current state and local
    environment of the engine instance, that is, a function returning a boolean. 
    
    ```
    boolean-guard : State -> LocalEnvironment LocalStateType -> Bool;
    ```

    However, as a design choice, guards will return additional data of type `T` from
    the local environment if the condition is met. So, if the guard is satisfied,
    this data (of type `T`) will be passed to the action function; otherwise, that
    is, if the guard is not satisfied, no data is returned.
    
## Engine Family Type

The `EngineFamily` type is the core type for defining an engine family in Anoma.
It encapsulates the local environment and the list of guarded actions that define
the behavior of the engine instances in the family. Our type is parameterised
by the local state type `LocalStateType` and the message type `MessageType`.
This means, while several engine instances share the same behavior, each instance
has its own local state and mailbox cluster.

```juvix
type EngineFamily (LocalStateType : Type) (MessageType : Type) := mkEngineFamily {
  env : LocalEnvironment LocalStateType MessageType;
  Behaviour : List (GuardedAction LocalStateType MessageType);
};
```

!!! example "Example of an Engine Family in Words"

    For example, to define an engine family for voting:

    - `LocalStateType` could be a record with fields like `votes`, `voters`, and `results`.
    - The message type might be a coproduct of `Vote` and `Result`.
    - The guarded actions may include actions like:
        - `storeVote` to store a vote in the local state,
        - `computeResult` to compute the result of the election, and
        - `announceResult` to send the result to some other engine instances.

   In this example, engine instances may vary (e.g., different elections or
   voters), but the voting systems will operate identically given the same
   initial state. This ensures consistent behavior across all engine instances
   within the same family.

!!! info

    In the `EngineFamily` type above, `List` is used because if multiple guards are 
    satisfied, we assume that their corresponding actions are executed according to
    their index in the list, defining the priority of each (guarded) action. This behaviour
    may, in principle, change in the future.
