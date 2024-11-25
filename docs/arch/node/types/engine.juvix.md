---
icon: octicons/gear-16
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
    import arch.node.types.engine_config open public;
    import arch.node.types.engine_environment open public;
    import arch.node.types.engine_behaviour open public;
    ```

# The type for engines

An **engine** is a computational unit with a specific name and [[Engine Behaviour|behaviour]],
plus an initial [[Engine Environment|environment]],
which comprises the specific state, the mailbox cluster,
the acquaintances, and the timers.

We refer to the type of engines as `Engine`,
instantiated with the following type parameters:

- `C`: the type for the read-only engine configuration,
- `S`: the type for the local state,
- `M`: the type for the mailbox state,
- `H`: the type for the timer handles,
- `L`: the type for the action labels,
- `A`: the type for the action arguments.

Each engine, not its type, is associated with:

- a specific configuration, which contains the engine name (unique across the system), node ID, and engine-specific configuration,
- a declaration of its own [[Engine Environment|execution context]], that is,
  the specific local state, the mailbox cluster, the acquaintances, and the timers,
- as well as a specific [[Engine Behaviour|behaviour]].

```juvix
type Engine (C S M H L A : Type) := mkEngine {
  cfg : EngineConfig C;
  env : EngineEnv S M H;
  behaviour : EngineBehaviour C S M H L A;
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
