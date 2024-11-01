---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- engine-behaviour
- engine-type
- juvix
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.engine;
    import prelude open;
    import arch.node.types.identities open;
    import arch.node.types.engine_environment open public;
    import arch.node.types.engine_behaviour open public;
    ```

# Engine

An **engine** is a computational unit with a specific name and behaviour, plus
an initial environment, which comprises the specific state, the mailbox cluster,
the acquaintances, and the timers. The type of engines is `Engine`, instantiated
with the types for the local states, the mailboxes' state, the time handles, the
action-label action, and the precomputation. We use the following notation to
denote these type parameters:

- `S` the type for the local states,
- `M` the type for the mailboxes' state,
- `H` the type for the time handles,
- `A` the type for the action-label,
- `L` the type for the precomputation, and
- `X` the type for the external inputs.

To define the type for engine instances, we first need to define the type for
engine behaviours.

## The type for engine behaviours

The `EngineBehaviour` type encapsulates the concept of behaviours within Anoma.
As defined, it clears up that engines are essentially a collection of guarded
state-transition functions.

```juvix
type EngineBehaviour (S M H A L X : Type) := mkEngineBehaviour {
  guards : List (Guard S M H A L X);
  action : ActionFunction S M H A L X;
  conflictSolver : Set A -> List (Set A);
};
```

!!! info "On the use of `List` for guards in `EngineBehaviour`"

    The `EngineBehaviour` type uses `List` for guards to enable parallel
    processing. This choice acknowledges that guards can be concurrent or
    competing, with the latter requiring priority assignment to resolve
    non-determinism. While guards should form a set, using `List` simplifies the
    implementation and provides an inherent ordering.

## The type for engines

An *engine* is a term of type `Engine` instantiated with the types for the local
states, the mailboxes' state, the time handles, the action-label action, and the
precomputation. Each engine, not its type, is associated with:

- a specific name (unique across the system),
- a specific behaviour, and
- a declaration of its own execution context, that is, the specific state, the
  mailbox cluster, the acquaintances, and the timers.

```juvix
type Engine (S M H A L X : Type) := mkEngine {
  name : EngineName;
  behaviour : EngineBehaviour S M H A L X;
  initEnv : EngineEnvironment S M H;
};
```

!!! example "Voting Engine"

    As an example, we could define an engine type for a voting system:

    - `S` could be a record with fields like `votes`, `voters`, and `results`.
    - The engine-specific message type might be a coproduct of `Vote` and `Result`.
    - The behaviour of this engine may include guarded actions such as:
        - `storeVote` to store a vote in the local state,
        - `computeResult` to compute the result of the election, and
        - `announceResult` to send the result to some other engine instances.

    With each different election or kind of voters, we obtain a new engine instance,
    while the underlining voting system, the voting engine family, remains the same.
