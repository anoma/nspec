---
icon: material/animation-play
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
elapsed during the engine's operation. Guards return data of type `GuardOutput A`
if the precondition of the action that they are guarding is met.

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
- action arguments (`A`).

The types of the input and output of an action are
the following two:

- `ActionInput S M H A`,
- `ActionEffect S M H A`.

The record type `ActionInput S M H A` encapsulates the following data:

- A `GuardOutput A` term, which includes:

    - action arguments (`A`).

- The environment of the engine instance.
- The local time of the engine instance when the guard evaluation was triggered.

### `Exec`

Execution order of functions,
such as guard or action functions.

```juvix
type Exec F :=
  | End
  | Seq F (Exec F)
  | Par F (Exec F)
  ;
```

### Action effect

The `ActionEffect S M H A` type defines the results produced by the action,
which can be

- Update its environment (while leaving the name unchanged).
- Produce a set of messages to be sent to other engine instances.
- Set, discard, or supersede timers.
- Define new engine instances to be created.

<!-- --8<-- [start:ActionEffect] -->
```juvix
type ActionEffect (S M H A : Type) := mkActionEffect {
  env : EngineEnvironment S M H;
  msgs : List EngineMsg;
  timers : List (Timer H);
  engines : List Anoma.Env;
};
```
<!-- --8<-- [end:ActionEffect] -->

### Action

<!-- --8<-- [start:ActionFunction] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Action (S M H A : Type) : Type :=
  (args : A) ->
  (tt : TimestampedTrigger H) ->
  (env : EngineEnvironment S M H) ->
  Option (ActionEffect S M H A);
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

    However, as a design choice, guards will return additional data of type `GuardOutput A` that
    may or may not use the engine environment if the condition is met. Thus, if
    the guard is satisfied, this data (of type `GuardOutput A`) is assumed to
    be passed to the action function. Then, if the guard is not satisfied, no data
    is returned.

### `Guard`

<!-- --8<-- [start:Guard] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Guard (S M H A : Type) : Type :=
  (tt : TimestampedTrigger H) ->
  (env : EngineEnvironment S M H) ->
  Option (GuardOutput S M H A);
```
<!-- --8<-- [end:Guard] -->

### `GuardOutput`

<!-- --8<-- [start:GuardOutput] -->
```juvix
type GuardOutput (S M H A : Type) :=
  mkGuardOutput{
    actions : Exec (Action S M H A);
    args : A;
  };
```
<!-- --8<-- [end:GuardOutput] -->

## The type for engine behaviours

The `EngineBehaviour` type encapsulates the concept of behaviours within Anoma.
Each engine is associated with a specific term of type `EngineBehaviour` that
defines its core dynamics and operational characteristics. The behaviour
determines how the engine processes inputs, manages state, and interacts with
other components. As defined, it clears up that engines are essentially a
collection of guarded state-transition functions. Using the terminology
introduced earlier, an `EngineBehaviour` is a set of guards and an action function.

<!-- --8<-- [start:EngineBehaviour] -->
```juvix
type EngineBehaviour (S M H A : Type) :=
  mkEngineBehaviour {
    guards : Exec (Guard S M H A);
};
```
<!-- --8<-- [end:EngineBehaviour] -->

!!! info "On the use of `List` for guards in `EngineBehaviour`"

    The `EngineBehaviour` type uses `List` for guards to enable parallel
    processing. This choice acknowledges that guards can be concurrent or
    competing, with the latter requiring priority assignment to resolve
    non-determinism. While guards should form a set, using `List` simplifies the
    implementation and provides an inherent ordering.
