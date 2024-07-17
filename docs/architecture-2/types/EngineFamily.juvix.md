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
    module architecture-2.types.EngineFamily;
    import architecture-2.Prelude open;
    ```

# Engine Family Types

## Core Types and Concepts

This page highlights the essential types and concepts of an engine family in the
Anoma Specification, specifically focusing on writing these families in Juvix.
Please refer to the [[Engines in Anoma]] page for a better overview and
motivation of the concept of engines for Anoma.

Each engine family must declare specific components that each of its member
engine instances will have. For Anoma specifications, the components are:

Engine Environment

:   This serves as the execution context for engines. In addition to the local
    state, the engine environment encompasses elements such as the mailbox
    cluster owned by an engine instance and a finite set[^1] of acquaintances—other engine
    instances known to the current one that can interact with it.

Guarded Actions

:   The engine's behavior is specified by a finite set of functions that mutate
    the local state of the engine's instance. These functions, also called state
    transition functions, are accompanied by specific conditions on the messages
    received and the engine environment.


So, let's introduce the type for each of these components.


### Engine Family Environment

The engine family environment encompasses static information for engine instances in the
following categories:

- A global reference, `name`, for the engine instance.
- Local state that is engine-specific.
- Mailbox cluster, which is a map of mailbox IDs to mailboxes.
- A set of names of acquainted engine instances. It is implicit that the engine
  instance is acquainted with itself, so there is no need to include its own
  name.
- A list of timers that have been set.

This data is encapsulated within the `EngineEnvironment` type family, which is
parameterised by three types: `S`, representing the local state, `I`,
representing the type of incoming messages to the engine instance, and `M`,
representing the type of mailboxes' states.


```juvix
type EngineEnvironment (S I M : Type) :=
  mkEngineEnvironment {
      engineRef : Name ; -- read-only
      state : S;
      mailboxCluster : Map MailboxID (Mailbox I M);
      acquaintances : Set Name;
      timers : List Timer;
};
```

For short, we will use the type parameters `S`, `I`, and `M` to represent
the type of the local state, incoming message types, and mailboxes' state, respectively.

### Engine Behaviours

Each engine processes only one message at a time. The behaviour of an engine is
specified by a finite set of _guarded actions_, which define the transitions an engine
can make from one state to another based on specific conditions.

Guarded actions are terms of type `GuardedAction`, which encapsulates
the following components:

- A _guard function_ of type `Trigger I -> EngineEnvironment S I M -> Maybe R`, where
  the _trigger_ of type `Trigger I` is a term that captures the message received. This
  trigger can include the received message or timers that have elapsed during
  the engine's operation. Guards return data of type `R` if the condition is met.
  That data serves as input for the corresponding action.

- An _action_ of type `Action S I M R O C`, where the new type parameters `O`
  denote the type of outgoing messages, and `C` signifies the type encoding the engine
  instances to be created.


#### Action Functions

Below, we define the type for actions. These functions are parametrised by the
types for local state, incoming messages, the type for mailboxes' state,
the data returned by the guard function, and outgoing messages.

```juvix
Action (S I M R O C : Type) : Type := ActionInput S I M R -> ActionResult S I M R O C;
```

So, for convenience, we have the input and output of an action into two separate types:
`ActionInput S I R` and `ActionResult S I M R O C`. The `ActionInput S I R` type is a
record that encapsulates the following data:

- A term of type `R`, which represents the data returned by the guard function,
  if any.
- The environment of the corresponding engine instance.
- The time at which the corresponding trigger started.

```juvix
type ActionInput (S I M R : Type)
  := mkActionInput {
      guardOutput : R;
      env : EngineEnvironment S I M;
      time : Time;
};
```

Finally, the `ActionResult S I M R O C` type defines the results produced by the
action. When executing such a function, the engine instance can:

- Update its environment but not its name.
- Set messages to be sent to other engine instances.
- Set, discards, or supersede timers.
- Define new engine instances to be created.

    ??? info "On creating new engine instances"

        To create new engine instances, we need to specify the following data:

        - An engine family type.
        - A unique name for the new engine instance, assuming the system will ensure
          its uniqueness.
        - The initial state of the engine instance.

```juvix
type ActionResult (S I M R O C : Type) := mkActionResult {
    newEnv : EngineEnvironment S I M;
    producedMessages : List (EnvelopedMessage O);
    timers : List Timer;
    spawnedEngines : List C;
};
```


#### Guarded Actions

To recap, a guarded action consists of a _guard_ and an _action_. The guard is a
function that evaluates conditions on the engine environment to decide if the
action should be executed. This guard function has as input the trigger that
caused the guard to be evaluated, and the environment of the engine instance to
determine if the condition to run the action is met. The action is a function
that can update the engine environment to some extent and may declare terms that
will be internally processed as instructions for setting messages to be sent or
for creating new engine instances.


```juvix
type GuardedAction (S I M R O C : Type) := mkGuardedAction {
   guard : Trigger I -> EngineEnvironment S I M -> Maybe R;
   action : Action S I M R O C
};
```

??? info "On the type signature of the guard function"


    In principle, borrowing terminology from Hoare logic, a guard is a
    _precondition_ to run an action. The corresponding predicate is activated by a
    trigger and evaluated within the context of the engine's environment. It then
    returns a boolean when the predicate is satisfied, specifically of type

    ```haskell
    Trigger I -> EngineEnvironment S I M -> Bool;
    ```

    However, as a design choice, guards will return additional data of type R that
    may or may not use the engine environment if the condition is met. Thus, if
    the guard is satisfied, this data (of type R) is assumed to be passed to the
    action function. Then, if the guard is not satisfied, no data is
    returned.

## Engine Families and Instances

The `EngineFamily` type encapsulates the concept of engines within Anoma. As defined,
it clears up that engines are essentially a collection of guarded state-transition
functions. Our type for these families is parameterised by a type for their local states,
a type for their incoming messages, a type for its mailboxes' state, a type for returned
data by the guard functions, and a type for outgoing messages.

```juvix
type EngineFamily (S I M R O C : Type) := mkEngineFamily {
  actions : List (GuardedAction S I M R O C);
};
```

??? info "On the use of `List` in `EngineFamily`"

    In the `EngineFamily` type, we used `List` not just for
    convenience but also because we have not yet established a way to compare or
    sort guarded actions, guards, and Action. Additionally,
    using `List` specifies the order in which the guarded actions will execute when
    multiple guards are met. This behavior might change in the future.

Additionally, we define the `Engine` type, which represents an engine within a family.
A term of this `Engine` type is referred to as an engine instance. Each engine instance
is associated with a specific name and a family of engines, plus a declaration of its own
execution context, that is, the specific state, mailbox cluster, acquaintances, and timers.

```juvix
type Engine (S I M R O C : Type):= mkEngine {
  name : Name;
  family : EngineFamily S I M R O C;
  initEnv : EngineEnvironment S I M;
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


[^1] : Presented as a list for simplicity.