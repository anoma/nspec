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
    import arch.node.types.engine_environment open public;
    import arch.node.types.engine_behaviour open public;
    ```

# The type for engines

An **engine** is a computational unit with a specific name and [[Engine Behaviour|behaviour]], plus
an initial [[Engine Environment|environment]], which comprises the specific state, the mailbox cluster,
the acquaintances, and the timers. We refer to the type of engines as `Engine`,
instantiated with the types for the local states, the mailboxes' state, the
time handles, the action-label action.
We use the following notation to denote these type parameters:

- `S` the type for the local states,
- `M` the type for the mailboxes' state,
- `H` the type for the time handles,
- `L` the type for the action label,
- `A` the type for the action args.

Each engine, not its type, is associated with:

- a specific name (unique across the system),
- a specific [[Engine Behaviour|behaviour]], and
- a declaration of its own [[Engine Environment|execution context]], that is, the
  specific state, the mailbox cluster, the acquaintances, and the timers.

```juvix
type Engine (S M H A : Type) := mkEngine {
  initEnv : EngineEnv S M H;
  behaviour : EngineBehaviour S M H A;
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
