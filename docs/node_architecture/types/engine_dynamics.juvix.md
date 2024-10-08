---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Engine-Dynamics
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.engine_dynamics;
    import node_architecture.basics open;
    import node_architecture.types.anoma_message as Anoma;
    import node_architecture.types.engine_environment open;
    import node_architecture.types.anoma_environment as Anoma;
    ```

# Engine dynamics

Each engine processes only one message at a time. The behaviour of an engine is
specified by a finite set of _guards_ and an _action function,_ which determine
how engine instances react to received messages or timer notifications.

## Guards

Guards are terms of type `Guard`, which is a function type

--8<-- "./docs/node_architecture/types/engine_dynamics.juvix.md:whole-guard-type"

where the _trigger_ of type `TimestampedTrigger I H` is a term that captures the
message received with a timestamp or
a clock notification about timers that have elapsed during the engine's operation.
Guards return data of type `GuardOutput A L X`
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
besides changes to the engine environment,
an action effect comprises sending messages, creatting engines, and updating timers.

## Action function

The input is parameterised by the types for: local state (`S`), incoming
messages (`I`), mailbox state (`M`), timer handles (`H`), matched arguments
(`A`), action labels (`L`), and precomputation results (`X`). The types of the
input and output of an action are the following two:

- `ActionInput S I M H A L X` and
- `ActionEffect S I M H A L X`.

The record type `ActionInput S I M H A L X` encapsulates the following data:

- A term of type `GuardOutput A L X`, which represents
  - the matched arguments, e.g., from a received message,
  - the action label that determines the action to be performed
  - other (expensive) precomputation results that
    the guard function has to calculate and can be resued by the action function.
- The environment of the corresponding engine instance.
- The local time of the engine instance when guard evaluation was triggered.

```juvix
type GuardOutput (A L X : Type) :=
  mkGuardOutput{
    args : List A;
    label : L;
    other : X
  };
```

<!-- --8<-- [start: whole-guard-type] -->
```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
Guard (S M H A L X : Type) : Type :=
  (t : TimestampedTrigger H) -> (env : EngineEnvironment S M H)-> Maybe (GuardOutput A L X);
```
<!-- --8<-- [end: whole-guard-type] -->

### Action input


```juvix
type ActionInput (S M H A L X : Type) := mkActionInput {
  guardOutput : GuardOutput A L X;
  env : EngineEnvironment S M H;
  timestampedTrigger : TimestampedTrigger H; -- TODO: do we need this?
};
```

### Action effect

The `ActionEffect S I M H A L X` type defines the results produced by the
action, which can be

- Update its environment (while leaving the name unchanged).
- Produce a set of messages to be sent to other engine instances.
- Set, discards, or supersede timers.
- Define new engine instances to be created.4

```juvix
type ActionEffect (S M H A L X : Type) := mkActionEffect {
  newEnv : EngineEnvironment S M H;
  producedMessages : List EnvelopedMessage;
  timers : List (Timer H);
  spawnedEngines : List Anoma.Env;
};
```


```juvix
{-# isabelle-ignore: true #-} -- TODO: remove this when the compiler is fixed
ActionFunction (S M H A L X : Type) : Type :=
  (input : ActionInput S M H A L X) ->
  ActionEffect S M H A L X;
```

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
    Trigger I H -> EngineEnvironment S I M H -> Bool;
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
