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


??? info "Juvix imports"

    ```juvix
    module architecture-2.engines.base;
    import architecture-2.engines.basic-types open;
    ```


# Engine Types

!!! info 

    Each engine page in the specs describes one particular "kind" of engine. The
    formal core of each page is the transition function, which describes the
    behaviour of all engine instances of this "kind". In principle, we could use the
    URL of each engine page as a _label_ for engine instances of this "kind", but
    any string that uniquely refers either to the engine page (or the transition
    function) is suitable.

This page focuses on the fundamental types and concepts necessary to define an
engine type in the Anoma Specification, specifically the types and terms in
Juvix. See the page on [[Engines in Anoma]] for more background of how Anoma
instances are composed of communicating engine instances, in particular how
transition functions are described as a set of _guarded actions._

## Data components of an engine

Each engine kind must declare specific components relevant to its purpose. 
For Anoma specs, these components include:

- A local environment parameterised by the types of the local state and
  messages. In fact, the local environment includes the engine's
  identity, local state, mailbox cluster, local time, timers, and acquaintances.

- Guarded actions, which briefly are the actions that the engine can take under
  certain conditions


### Local Environment

To define an engine, we need to know the local state and message type it will
handle, represented as type parameters `LocalStateType` and `MessageType`.

The local environment includes static information in these categories:

- Engine identity
- Engine instance's local state
<!-- - Local time -->
- Map of mailbox IDs to mailboxes
- List of timers set by the engine instance
<!-- - List of engines spawned by the instance (acquaintances or conversion partners)
  by their names -->
- List of acquainted engine instances, each which may be known by their external identity.

This data is encapsulated in the `LocalEnvironment` type.

```juvix
type LocalEnvironment (LocalStateType : Type) (MessageType : Type) 
  := mkLocalEnvironment {
      engineInstanceIdentity : Identity;
      localState : LocalStateType;
      mailboxCluster : Map MailboxID (Mailbox MessageType);
      localTime : Time;
      timers : List Timer;
      acquaintances : Map Name (Maybe ExternalID);
};
```


## State Transition Function as List of Guarded Actions

With the types of a local environment in place, the remaining part of an engine
is its *guarded actions*. These actions describe a state transition function, the
core of an engine's operation. So we define their type first.

A state transition function takes a set of arguments, including the engine's
local environment, and the time-stamped trigger for the state transition. These
arguments are encapsulated in the `StateTransitionArguments` record type.

```juvix
StateTransition (LocalStateType : Type) (MessageType : Type) : Type :=
  StateTransitionArguments LocalStateType MessageType
    -> StateTransitionResult LocalStateType MessageType;
```

The arguments and results for state transition functions has the following
structure.

### State Transition Arguments

```juvix
type StateTransitionArguments (LocalStateType : Type) (MessageType : Type) 
  := mkStateTransitionArguments {
      localEnvironment : LocalEnvironment LocalStateType MessageType;
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

type StateTransitionResult (LocalStateType : Type) (MessageType : Type)
  := mkStateTransitionResult {
    localEnvironment : LocalEnvironment LocalStateType MessageType;
    producedMessages : Mailbox MessageType;
    timers : List Timer;
    spawnedEngines : List (Pair (Pair EngineLabel Name) LocalStateType); --todo: update this type
};
```

So when executing a state transition function, the engine instance will:

- Update its local state
- Set messages to be sent
- Set timers
- Spawn new engines (if necessary)

## Guarded Actions

A guarded action consists of a _guard_ and an _action_. The guard is a function
that evaluates conditions on the engine's local environment to decide if the
action should be executed. The action is a function that updates the local
environment and may include additional effects, as said before, such as setting
timers, messages, and spawning new engines.

```juvix
type GuardedAction (LocalStateType : Type) (MessageType : Type) := mkGuardedAction {
  guard : {T : Type} -> LocalEnvironment LocalStateType MessageType -> Maybe T;
  action : {T : Type} -> T -> StateTransition LocalStateType MessageType
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

    However, as a design choice, guards will return additional data of type T from
    the local environment if the condition is met. So, if the guard is satisfied,
    this data (of type `T`) will be passed to the action function; otherwise, that
    is, if the guard is not satisfied, no data is returned.
    
## Anoma Engine Type Definition

```juvix
type Engine (LocalStateType : Type) (MessageType : Type) := 
  mkEngine {
    localEnvironment : LocalEnvironment LocalStateType MessageType;
    guardedActions : List (GuardedAction LocalStateType MessageType)
};
```

In conclusion, the `Engine` type specifies the structure of an Anoma engine.
Each engine instance includes a local environment and a list of [guarded
actions](#guarded-actions) (refer to Section [[Engines in
Anoma#on-engine-types|On Engine Types]] for more details). The `Engine` type
requires two parameters: `LocalStateType`, which defines instance-specific
data, and `MessageType`, which represents the types of messages handled by the
engine.

For example, in a voting engine, `LocalStateType` could be a record with
fields such as `votes`, `voters`, and `results`. Alternatively, it could be set
to the unit type if no local state is needed. The message type for the voting
engine might be a coproduct type of `Vote` and `Result`.

!!! warning

    In the `Engine` type above, `List` is used because if multiple guards are 
    satisfied, their corresponding actions are executed according to their index
    in the list, defining the priority of each (guarded) action.