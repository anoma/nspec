---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Engine
- Behaviour
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.engine_behaviour;

    import arch.node.types.basics open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.engine_environment open;
    import arch.node.types.anoma_environment as Anoma;
    import arch.node.types.anoma_message as Anoma;
    ```

# Engine behaviour

Each engine processes only one message at a time. The behaviour of an engine is
specified by a finite set of _guards_ and an _action function,_ which both
determine how engine instances react to received messages or timer
notifications.

## Guards

Guards are terms of type `Guard`, which is a function type

--8<-- "./docs/arch/node/types/engine_behaviour.juvix.md:Guard"

where the _trigger_ of type `TimestampedTrigger H` is a term that captures the
message received with a timestamp or a clock notification about timers that have
elapsed during the engine's operation. Guards return data of type `GuardOutput A
L X` if the precondition of the action that they are guarding is met.

Recall that the behaviour is described by a set of guards and an action
function. The guard is a function that evaluates conditions in the engine
environment to determine what action should be performed;
for this, each guard creates an _action label,_
that then is "interpreted" by the action function.

The guard function receives:

- the timestamped trigger that caused guard evaluation,
- the environment of the engine instance, and
- an optional time reference for the starting point of the evaluation of all guards.

Given these inputs, the guard function computes a set of action labels.
The action function then computes the effects of the action label;
besides changes to the engine environment, an action effect comprises sending
messages, creating new engine instances, and updating timers.

## Action function

The input is parameterised by the types for:

- local state (`S`),
- mailbox state (`M`),
- timer handles (`H`),
- matched arguments (`A`),
- action labels (`L`), and
- precomputation results (`X`).

The types of the input and output of an action are
the following two:

- `ActionInput S M H A L X` and
- `ActionEffect S M H A L X`.

The record type `ActionInput S M H A L X` encapsulates the following data:

- A `GuardOutput A L X` term, which includes:

    - Matched arguments, such as those from a received message.
    - An action label that specifies the action to be performed.
    - Precomputation results that are calculated by the guard function and can be reused by the action function.

- The environment of the engine instance.
- The local time of the engine instance when the guard evaluation was triggered.


### GuardOutput

<!-- --8<-- [start:GuardOutput] -->
```juvix
type GuardOutput (A L X : Type) :=
  mkGuardOutput{
    matchedArgs : List A;
    actionLabel : L;
    precomputationTasks : X
  };
```
<!-- --8<-- [end:GuardOutput] -->

### Guard

<!-- --8<-- [start:Guard] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Guard (S M H A L X : Type) : Type :=
  (t : TimestampedTrigger H) ->
  (env : EngineEnvironment S M H) ->
  Option (GuardOutput A L X);
```
<!-- --8<-- [end:Guard] -->

### Action input

<!-- --8<-- [start:ActionInput] -->
```juvix
type ActionInput (S M H A L X : Type) := mkActionInput {
  guardOutput : GuardOutput A L X;
  env : EngineEnvironment S M H;
  timestampedTrigger : TimestampedTrigger H;
};
```
<!-- --8<-- [end:ActionInput] -->

### Utility functions

- Get the message from an `ActionInput`:

    ```juvix
    getMessageFromActionInput {S M H A L X} (input : ActionInput S M H A L X) : Option Anoma.Msg
      := getMessageFromTimestampedTrigger (ActionInput.timestampedTrigger input);
    ```

- Get the sender from an `ActionInput`:

    ```juvix
    getSenderFromActionInput {S M H A L X} (input : ActionInput S M H A L X) : EngineID
      := fromOption (getSenderFromTimestampedTrigger
      (ActionInput.timestampedTrigger input)) unknownEngineID;
    ```

- Get the target from an `ActionInput`:

    ```juvix
    getTargetFromActionInput {S M H A L X} (input : ActionInput S M H A L X) : EngineID
      := fromOption (getTargetFromTimestampedTrigger
      (ActionInput.timestampedTrigger input)) unknownEngineID;
    ```

### Action effect

The `ActionEffect S M H A L X` type defines the results produced by the action,
which can be

- Update its environment (while leaving the name unchanged).
- Produce a set of messages to be sent to other engine instances.
- Set, discard, or supersede timers.
- Define new engine instances to be created.

<!-- --8<-- [start:ActionEffect] -->
```juvix
type ActionEffect (S M H A L X : Type) := mkActionEffect {
  newEnv : EngineEnvironment S M H;
  producedMessages : List EngineMessage;
  timers : List (Timer H);
  spawnedEngines : List Anoma.Env;
};
```
<!-- --8<-- [end:ActionEffect] -->

### Action function

<!-- --8<-- [start:ActionFunction] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
ActionFunction (S M H A L X : Type) : Type :=
  (input : ActionInput S M H A L X) ->
  ActionEffect S M H A L X;
```
<!-- --8<-- [end:ActionFunction] -->


??? info "On creating new engine instances"

    To create new engine instances, we need to specify the following data:

    - A unique name for the new engine instance.
    - The initial state of the engine instance.
    - The corresponding set of guards and the action function.

    The last point is however implicit.

If the guard does not give a result, this means that none of its guarded actions
are triggered.

??? info "On the type signature of the guard function"

    In principle, borrowing terminology from Hoare logic, a guard is a
    _precondition_ to run an action. The corresponding predicate is activated by a
    trigger and evaluated within the context of the engine's environment. It then
    returns a boolean when the predicate is satisfied, specifically of type

    ```haskell
    Trigger H -> EngineEnvironment S M H -> Bool;
    ```

    However, as a design choice, guards will return additional data of type `GuardOutput A L X` that
    may or may not use the engine environment if the condition is met. Thus, if
    the guard is satisfied, this data (of type `GuardOutput A L X`) is assumed to
    be passed to the action function. Then, if the guard is not satisfied, no data
    is returned.

#### Conflict resolution

Finally, `conflictSolver` is a function that takes a finite set of action
labels as input; it outputs a list of action label sets that are pairwise
disjoint and whose union is the input set or is empty, if conflict resolution
fails. And for each element of the output it should be that if applied to this
element, it returns the one element list of the set itself.

```
conflictSolver : Set A -> List (Set A);
```

## The type for engine behaviours

The `EngineBehaviour` type encapsulates the concept of behaviours within Anoma.
Each engine is associated with a specific term of type `EngineBehaviour` that
defines its core dynamics and operational characteristics. The behaviour
determines how the engine processes inputs, manages state, and interacts with
other components. As defined, it clears up that engines are essentially a
collection of guarded state-transition functions. Using the terminology
introduced earlier, an `EngineBehaviour` is a set of guards and an action
function, plus a conflict solver.

<!-- --8<-- [start:EngineBehaviour] -->
```juvix
type EngineBehaviour (S M H A L X : Type) :=
  mkEngineBehaviour {
    guards : List (Guard S M H A L X);
    action : ActionFunction S M H A L X;
    conflictSolver : Set A -> List (Set A);
};
```
<!-- --8<-- [end:EngineBehaviour] -->

!!! info "On the use of `List` for guards in `EngineBehaviour`"

    The `EngineBehaviour` type uses `List` for guards to enable parallel
    processing. This choice acknowledges that guards can be concurrent or
    competing, with the latter requiring priority assignment to resolve
    non-determinism. While guards should form a set, using `List` simplifies the
    implementation and provides an inherent ordering.
