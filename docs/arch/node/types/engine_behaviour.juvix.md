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
    import arch.node.types.engine_config open;
    import arch.node.types.engine_environment open;
    ```

# Engine behaviour

Each engine processes only one message at a time. The behaviour of an engine is
specified by a finite set of _guards_ and an _action function,_ which both
determine how engine instances react to received messages or timer
notifications.

## Guards

Guards are terms of type `Guard`, which is a function type, where the _trigger_
of type `TimestampedTrigger H AM` is a term that captures the message received with
a timestamp or a clock notification about timers that have elapsed during the
engine's operation. Guards return data of type `GuardOutput A` if the
precondition of the action that they are guarding is met.

Recall that the behaviour is described by a set of guards and an action
function. The guard is a function that evaluates conditions in the engine
environment to determine what action should be performed; for this, each guard
creates an _action label,_ that then is "interpreted" by the action function.

The guard function receives three arguments:

- the timestamped trigger that caused guard evaluation;
- the unchanging engine configuration; and
- the current environment of the engine instance.

Given these inputs, the guard function computes an action label, which encodes

- all information necessary to infer how the engine will react
- additional information on how this action contributes to properties of the
Anoma protocol instance the engine is part of.

The action function then computes the effects of the action label;
besides changes to the engine environment, an action effect comprises sending
messages, creating new engine instances, and updating timers.

## Actions

### `Action`

The input of the action function is parameterised by the types for:

- `C`: engine configuration,
- `S`: local state,
- `B`: mailbox state,
- `H`: timer handles,
- `A`: action arguments,
- `AM`: type for all engine messages (`Msg`),
- `AC`: type for all engine configurations (`Cfg`), and
- `AE`: type for all engine environments (`Env`).

The `Action` function receives as argument the `ActionInput`,
and returns the `ActionEffect`.

<!-- --8<-- [start:ActionFunction] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Action (C S B H A AM AC AE : Type) : Type :=
  (input : ActionInput C S B H A AM) ->
  Option (ActionEffect S B H AM AC AE);
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
    Trigger H AM -> EngineEnv S B H AM -> Bool;
    ```

    However, as a design choice, guards will return additional data of type `GuardOutput A` that
    may or may not use the engine environment if the condition is met. Thus, if
    the guard is satisfied, this data (of type `GuardOutput A`) is assumed to
    be passed to the action function. Then, if the guard is not satisfied, no data
    is returned.

### `ActionInput`

The `ActionInput` contains:

- the action arguments,
- the engine configuration,
- the engine environment, and
- the timestamped trigger that caused the guard evaluation.

<!-- --8<-- [start:ActionInput] -->
```juvix
type ActionInput C S B H A AM :=
  mkActionInput@{
    args : A;
    cfg : EngineCfg C;
    env : EngineEnv S B H AM;
    trigger : TimestampedTrigger H AM;
  };
```
<!-- --8<-- [end:ActionInput] -->

### `ActionEffect`

The `ActionEffect S B H AM AC AE` type defines the effects produced by the
action. The action can perform any of the following:

- Update the engine environment.
- Produce a set of messages to be sent to other engine instances.
- Set, discard, or supersede timers.
- Define new engine instances to be created.

<!-- --8<-- [start:ActionEffect] -->
```juvix
type ActionEffect S B H AM AC AE :=
  mkActionEffect@{
    env : EngineEnv S B H AM;
    msgs : List (EngineMsg AM);
    timers : List (Timer H);
    engines : List (Pair AC AE);
  };
```
<!-- --8<-- [end:ActionEffect] -->

### `ActionExec`

<!-- --8<-- [start:ActionExec] -->
```juvix
type ActionExec C S B H A AM AC AE :=
  | Seq (List (Action C S B H A AM AC AE))
  ;
```
<!-- --8<-- [end:ActionExec] -->

### `Guard`

<!-- --8<-- [start:Guard] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Guard (C S B H A AM AC AE : Type) : Type :=
  (trigger : TimestampedTrigger H AM) ->
  (cfg : EngineCfg C) ->
  (env : EngineEnv S B H AM) ->
  Option (GuardOutput C S B H A AM AC AE);
```
<!-- --8<-- [end:Guard] -->

### `GuardOutput`

The guard output defines an action sequence, the programmatic action to be
performed, and action arguments.

<!-- --8<-- [start:GuardOutput] -->
```juvix
type GuardOutput C S B H A AM AC AE :=
  mkGuardOutput@{
    action : ActionExec C S B H A AM AC AE;
    args : A;
  };
```
<!-- --8<-- [end:GuardOutput] -->

### `GuardEval`

<!-- --8<-- [start:GuardEval] -->
```juvix
type GuardEval C S B H A AM AC AE :=
  | First (List (Guard C S B H A AM AC AE))
  | Any (List (Guard C S B H A AM AC AE))
  ;
```
<!-- --8<-- [end:GuardEval] -->

The `GuardEval` type defines the criteria for evaluating actions associated with
guards inside the given list. The evaluation strategies are as follows:

- With `First`, we say that the first guard in the provided list that holds,
i.e., yields a result, upon sequential evaluation is selected, its associated
action is performed, and the evaluation stops.
- With `Any`, we say that any guard in the provided list that holds upon
sequential evaluation is selected, their associated actions are performed, and
the evaluation stops.

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
type EngineBehaviour C S B H A AM AC AE :=
  mkEngineBehaviour@{
    guards : GuardEval C S B H A AM AC AE;
  };
```
<!-- --8<-- [end:EngineBehaviour] -->
