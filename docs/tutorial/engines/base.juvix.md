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

```juvix hide
module tutorial.engines.base;
import architecture-2.engines.basic-types open;
```

# Engines

## How to Spawn an Engine Instance

Imagine an engine as a process running on your machine. Each engine has:

- A unique identifier
- A local environment necessary for its operation

To create (or spawn) an engine instance in Anoma, you will need the following information:

- The _identity_ of the engine instance.
- The initial _local state_ for the engine instance.
- The time at which the engine instance is spawned.

In addition to knowing which engine you want to spawn, it's then crucial to understand the type of the local state for the engine instance.  

Let's assume we have a primitive `primGetEngineLocalStateType` that provides such a type for a given engine identity and function that can spawn an engine instance.

```juvix
axiom primGetEngineLocalStateType : ExternalID -> Type;
```

```juvix
axiom 
  engineInstanceSpawn
    : (engineIdentity : ExternalID)
    -> (initialState : primGetEngineLocalStateType engineIdentity)
    -> (spawnTime : Time)
    -> Unit;
```

## Data components of an engine

Each engine type must declare specific components relevant to its purpose. 
For Anoma specs, these components include:

- Local environment
- Guarded actions, which briefly are the actions that the engine can take under certain conditions


### Local Environment

The local environment comprises static information in the following categories:

- Identity of the engine
- Local state of the engine instance
- Local time
- A list of mailboxes storing received messages
- A list of timers set by the engine instance
- A list of engines spawned by the engine instance (acquaintances or conversion
  partners)

<!-- As part of the local state, we have specific-types. Not sure if it's useful to have that info seperately. -->


```juvix
type EngineLocalEnv (LocalState : Type) := mkEngineLocalEnv {
  engineIdentity : Identity;
  localState : LocalState;
  localTime : Time;
  mailboxes : List Mailbox; -- TODO: replace this for Map
  timers : List Timer;
  acquaintances : List ExternalID;
}
```

## State Transition Functions

```juvix
StateTransition (EngineLocalState : Type) : Type := StateTransitionArguments EngineLocalState -> StateTransitionResult EngineLocalState;
```

Define the arguments and results for state transition functions:

### State Transition Arguments

```juvix
type StateTransitionArguments (EngineLocalState : Type) := mkStateTransitionArguments {
  state : State;
  localEnvironment : EngineLocalEnv EngineLocalState;
  trigger : Trigger;
  time : Time; -- The time at which the state transition is triggered
  -- Mailbox business
};
```

<!-- This is more involved for sure, for now, we can keep it simple. -->

### State Transition Result

```juvix
type StateTransitionResult (EngineLocalState : Type)
  := mkStateTransitionResult {
  state : State;
  localEnvironment : EngineLocalEnv EngineLocalState;
  producedMessages : List Message; -- The set of messages to be sent
  timers : List Timer;
  spawnedEngines : List (Pair ExternalID EngineLocalState);   -- the set of spawned engines
};
```

So when executing a state transition function, the engine instance will:

- Update its local state
- Send messages
- Provides a new state
- Set timers
- Spawn new engines (if necessary) via an internal call to engineInstanceSpawn

## Guarded Actions

A guarded action consist of a _guard_ and an _action_. The guard is a
  function that determines whether the action should be executed, and the action
  is a _state transition function_ describing the state transition of the engine
  instance.

??? info "On the type signature of the guard function"

    In principle, a guard is a predicate that evaluates the current state and local environment of the engine instance, that is, a function returning a boolean. 
    
    ```
    boolean-guard : State -> EngineLocalEnv EngineLocalState -> Bool;
    ```
    
    However, as a design choice, guards will return additional data of type T from the local environment if the condition is met. So, if the guard is satisfied, this data (T) will be passed to the action function; otherwise,that is, if the guard is not satisfied, no data is returned.
    

```juvix
type GuardedAction (EngineLocalState : Type) := mkGuardedAction {
  guard : {T : Type} -> EngineLocalEnv EngineLocalState -> Maybe T;
  action : {T : Type} -> T -> StateTransition EngineLocalState
};
```

??? info "Notation: Curly braces in guard and action's type signature"

    The curly braces notation used in the type signature of the guard function indicates that the type argument `T` can be ommited, as it is inferred from the return type.

    Ideally, type `T` should be an implicit field of `GuardedAction`, indicating that the action takes input from the guard's evaluation when satisfied. However, this is not feasible in Juvix at the moment.

    ```
    type GuardedAction (EngineLocalState : Type) := mkGuardedAction {
      {ReturnGuardType : Type};
      guard : State -> EngineLocalEnv EngineLocalState -> Maybe ReturnGuardType;
      action : ReturnGuardType -> StateTransition EngineLocalState
    };
    ```

# Resulting Engine Type

```juvix
type EngineType (EngineLocalState : Type) := mkEngineType {
   localEnvironment : EngineLocalEnv EngineLocalState;
   guardedActions : List (GuardedAction EngineLocalState)
};
```

Then, an engine type is represented by its local environment and a list of guarded actions. We use a list instead of a set because the order of the guarded actions is crucial. If multiple guards are satisfied, the actions are executed in the sequence they appear in the list.
