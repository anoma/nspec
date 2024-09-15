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
    module node_architecture.types.engine_family;
    import node_architecture.basics open;
    import node_architecture.types.anoma_message as Anoma;
    import node_architecture.types.engine_environment open public;
    import node_architecture.types.engine_dynamics open public;
    ```

# Engine family type

The `EngineFamily` type encapsulates the concept of engines within Anoma. As
defined, it clears up that engines are essentially a collection of guarded
state-transition functions. Our type for these families is parameterised by a
type for their local states, a type for their engine-specific messages, a type
for their mailboxes' state, a type for time handles, a type for action-label
action,


```juvix
type EngineFamily (S I M H A L X : Type) := mkEngineFamily {
  guards : List (Guard S I M H A L X);
  action : ActionFunction S I M H A L X;
  conflictSolver : Set A -> List (Set A);
};
```

!!! todo "On the use of `Set` for guards in `EngineFamily`"

    In the `EngineFamily` type, we used `Set` as it allows for the possibility that
    several guards are processed in parallel. However, the specification of an
    engine family must describe when guards are to be considered concurrent and when
    they are competing. In the latter case, we can assign priorities to guards to
    resolve unwanted non-determinism.

    The guards must form a set. However, this also entails, there is ordering
    notion for the elements of this set. For practical reasons and to maintain simplicity,
    we opt to use `List` instead of `Set` in the type for guards.

## Engine instance type

Additionally, we define the `Engine` type, which represents an engine within a family.
A term of this `Engine` type is referred to as an engine instance. Each engine instance
is associated with a specific name and a family of engines, plus a declaration of its own
execution context, that is, the specific state, mailbox cluster, acquaintances, and timers.

```juvix
type Engine (S I M H A L X : Type) := mkEngine {
  name : Name;
  family : EngineFamily S I M H A L X;
  initEnv : EngineEnvironment S I M H;
};
```

!!! example "Voting Engine Family"

    As an example, we could define an engine family for voting:

    - `S` could be a record with fields like `votes`, `voters`, and `results`.
    - The incomming message type might be a coproduct of `Vote` and `Result`.
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
