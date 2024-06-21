---
icon: octicons/gear-16
search:
exclude: false
tags:
- engine
- mailbox
- engine-type
- Juvix
---

!!! warning

    This document is a work in progress. Please do not review it yet.
    Also, this file should be probably somewhere else, like in the architecture-2 folder.


??? info "Juvix imports"

    ```juvix
    module tutorial.engines.base;
    import architecture-2.engines.basic-types open;
    ```


# Engine Types

```juvix
EngineLabel : Type := Label;
```

This page focuses on the fundamental types and concepts necessary to define an
engine in the Anoma Specification, specifically the types and terms in Juvix. It
does not explore the rationale or design choices behind engines in Anoma, as
these are covered in the [[Engines in Anoma]] page.

## Data components of an engine

Each engine type must declare specific components relevant to its purpose. 
For Anoma specs, these components include:

- A local environment which depends on a local state and message type specific to the engine
- Guarded actions, which briefly are the actions that the engine can take under certain conditions


### Local Environment

To define an engine, we need to know the local state and message type it will
handle, represented as type parameters `EngineLocalState` and `MessageType`.

The local environment includes static information in these categories:

- Engine identity
- Engine instance's local state
- Local time
- Mapping of MIDs (mailbox IDs) to mailboxes
- List of timers set by the engine instance
- List of engines spawned by the instance (acquaintances or conversion partners)
  by their names

This data is encapsulated in the `EngineLocalEnv` type.

```juvix
type EngineLocalEnv (LocalState : Type) (MessageType : Type) 
  := mkEngineLocalEnv {
      engineInstanceIdentity : Identity;
      localState : LocalState;
      localTime : Time;
      timers : List Timer;
      mailboxCluster : Map MailboxID (Mailbox MessageType);
      acquaintances : Map Name (Maybe ExternalID);
};
```


## State Transition Functions

With a local environment in place, the remaining part of an engine is its
*guarded actions*. These actions rely on a state transition function, the core
of an engine's operation. So we define their type first.

A state transition function takes a set of arguments, including the engine's local environment, and the trigger for the state
transition. These arguments are encapsulated in the `StateTransitionArguments`
record type.

```juvix
StateTransition (EngineLocalState : Type) (MessageType : Type) : Type :=
  StateTransitionArguments EngineLocalState MessageType
    -> StateTransitionResult EngineLocalState MessageType;
```

Where the arguments and results for state transition functions has the following
structure.

### State Transition Arguments

```juvix
type StateTransitionArguments (EngineLocalState : Type) (MessageType : Type) 
  := mkStateTransitionArguments {
    localEnvironment : EngineLocalEnv EngineLocalState MessageType;
    trigger : Trigger MessageType;
    time : Time; -- The time at which the state transition is triggered
};
```

<!-- This is more involved for sure, for now, we can keep it simple. -->

### State Transition Result


!!! todo

    Update this type after updatng the mailbox type, which should include
    the identities of the sender.

```juvix

type StateTransitionResult (EngineLocalState : Type) (MessageType : Type)
  := mkStateTransitionResult {
  localEnvironment : EngineLocalEnv EngineLocalState MessageType;
  producedMessages : Mailbox MessageType;
  timers : List Timer;
  spawnedEngines : List (Pair (Pair EngineLabel Name) EngineLocalState); 
};
```

So when executing a state transition function, the engine instance will:

- Update its local state
- Send messages
- Set timers
- Spawn new engines (if necessary)

## Guarded Actions

A guarded action consist of a _guard_ and an _action_. The guard is a
  function that determines whether the action should be executed, and the action
  is a _state transition function_ describing the state transition of the engine
  instance.


```juvix
type GuardedAction (EngineLocalState : Type) (MessageType : Type) := mkGuardedAction {
  guard : {T : Type} -> EngineLocalEnv EngineLocalState MessageType -> Maybe T;
  action : {T : Type} -> T -> StateTransition EngineLocalState MessageType
};
```


??? info "On the type signature of the guard function"

    In principle, a guard is a predicate that evaluates the current state and local
    environment of the engine instance, that is, a function returning a boolean. 
    
    ```
    boolean-guard : State -> EngineLocalEnv EngineLocalState -> Bool;
    ```

    However, as a design choice, guards will return additional data of type T from
    the local environment if the condition is met. So, if the guard is satisfied,
    this data (of type `T`) will be passed to the action function; otherwise, that
    is, if the guard is not satisfied, no data is returned.
    

??? info "Notation: Curly braces in guard and action's type signature"

    The curly braces notation used in the type signature of the guard function
    indicates that the type argument `T` can be omitted, as it is inferred from the
    return type.

    Ideally, type `T` should be an implicit field of `GuardedAction`, indicating
    that the action takes input from the guard's evaluation when satisfied. However,
    this is not feasible in Juvix at the moment.

    ```
    type GuardedAction (EngineLocalState : Type) := mkGuardedAction {
      {ReturnGuardType : Type};
      guard : EngineLocalEnv EngineLocalState -> Maybe ReturnGuardType;
      action : ReturnGuardType -> StateTransition EngineLocalState
    };
    ```

## A type for Anoma Engines



```juvix
type EngineType (EngineLocalState : Type) (MessageType : Type) := mkEngineType {
   localEnvironment : EngineLocalEnv EngineLocalState MessageType;
   guardedActions : List (GuardedAction EngineLocalState MessageType)
};
```

In conclusion, we define the type `EngineType` that defines the structure of an
engine type. It indicates that an engine (instance) includes a local environment
and a list of [guarded actions](#guarded-actions) (read more on this concept in
Section [[Engines#on-engine-types |On Engine Types]]). It requires a type
parameter, `EngineLocalState`, which defines data specific to each engine
instance. For example, in a voting engine, `EngineLocalState` could be a record
with fields like `votes` and `voters`, or simply the unit type if no local state
is needed.

!!! warning

    In `EngineType`, `List` is used for guarded actions to maintain their order. The
    sequence is crucial because if multiple guards are satisfied, actions are
    executed in the listed order.


## Engine instances

Imagine an engine as a process running on your machine. Each engine has:

- A unique identifier
- A local environment necessary for its operation

To create (or spawn) an engine instance in Anoma, you will need the following information:

- The [[Identity#external-identity|identity]] of the engine instance.
- The initial _local state_ for the engine instance.

In addition to knowing which engine you want to spawn, it's then crucial to
understand the type of the local state for the engine instance.  

Let's assume we have a primitive `primGetEngineLocalStateType` that provides
such a type for a given engine identity and function that can spawn an engine
instance.

```juvix
axiom primGetEngineLocalStateType : ExternalID -> Type;
```

```juvix
axiom 
  engineInstanceSpawn
    : (engineInstanceIdentity : ExternalID)
    -> (initialState : primGetEngineLocalStateType engineInstanceIdentity)
    -> Unit;
```
