---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- Engine
- Behaviour
- Juvix
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.types.engine;
    import prelude open;
    import node_architecture.types.identities open;
    import node_architecture.types.engine_environment open public;
    import node_architecture.types.engine_behaviour open public;
    ```

# Engine type

The `Engine` type encapsulates the concept of engines within Anoma. As
defined, it clears up that engines are essentially a collection of guarded
state-transition functions. Our type for these families is parameterised by a
type for their local states, a type for their mailboxes' state, a type for time
handles, a type for action-label action, and a type for the precomputation.
We usually refer to the type for the local states as `S`, for the mailboxes' state
as `M`, for the time handles as `H`, for the action-label as `A`, for the precomputation
as `L`, and for the external inputs as `X`.

```juvix
type EngineBehaviour (S M H A L X : Type) := mkEngineBehaviour {
  guards : List (Guard S M H A L X);
  action : ActionFunction S M H A L X;
  conflictSolver : Set A -> List (Set A);
};
```

!!! info "On the use of `List` for guards in `EngineFamily`"

    The `EngineFamily` type uses `List` for guards to enable parallel
    processing. This choice acknowledges that guards can be concurrent or
    competing, with the latter requiring priority assignment to resolve
    non-determinism. While guards should form a set, using `List` simplifies the
    implementation and provides an inherent ordering.

## Engine instance type

Additionally, we define the `Engine` type, which represents an engine within a family.
A term of this `Engine` type is referred to as an engine instance. Each engine instance
is associated with a specific name and a family of engines, plus a declaration of its own
execution context, that is, the specific state, mailbox cluster, acquaintances, and timers.

```juvix
type Engine (S M H A L X : Type) := mkEngine {
  name : EngineName;
  behaviour : EngineBehaviour S M H A L X;
  initEnv : EngineEnvironment S M H;
};
```

!!! example "Voting Engine Family"

    As an example, we could define an engine family for voting:

    - `S` could be a record with fields like `votes`, `voters`, and `results`.
    - The engine-specific message type might be a coproduct of `Vote` and `Result`.
    - The guarded actions may include actions like:
        - `storeVote` to store a vote in the local state,
        - `computeResult` to compute the result of the election, and
        - `announceResult` to send the result to some other engine instances.

    With each different election or kind of voters, we obtain a new engine instance,
    while the underlining voting system, the voting engine family, remains the same.

!!! note

    Both the `EngineFamily` and `Engine` types are parameterised by several types. When
    not used in the context of a new engine family declaration, these types can be
    replaced by the unit type `Unit`.
