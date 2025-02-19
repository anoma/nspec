---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - nullifier
  - resource-machine
  - state
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.nullifier_properties;
    import prelude open;
    import arch.system.types.resource open;
    import arch.system.types.nullifierkey open;
    import arch.system.types.state open;
    import arch.system.types.nullifier open;
    import arch.node.types.crypto open;
    ```

# Nullifier Properties

<!-- --8<-- [start:properties] -->

??? quote "Auxiliary Juvix code: Axioms"

    ```juvix
    axiom computeNullifier : Resource -> NullifierKey -> Digest;
    axiom nullifierHash : Nullifier -> Digest;
    ```

!!! todo

    How are we supposed to define the `computeNullifier` and `nullifierHash`
    functions?

The following properties must hold true to consider a nullifier valid:

### Nullifier key must match the resource's nullifier key commitment

```juvix
match-nullifier-key
  (r : Resource)
  (nk : NullifierKey) : Bool :=
  let n := mkNullifier@{key := nk; resource := r} in
  (computeNullifier r nk) == (nullifierHash n)
```

### Nullifier must not exist in the [[Nullifier Set|nullifier set]]

```
unique-nullifier-property
  (s : State)
  (r : Resource)
  (nk : NullifierKey) : Bool :=
  let nullifier := mkNullifier@{key := nk; resource := r};
      nullifierSet : Set Nullifier := State.nullifierSet s;
      cond (other : Nullifier) : Bool := (Set.isMember other nullifierSet) && (other == nullifier)
  in not (all cond (n in nullifierSet));
```

!!! todo

    Typecheck the `unique-nullifier-property` produces an error message stating that
    `nullifierSet` is of type `Set Nullifier` and not `Set NullifierKey`.
    Apparently, it is an alias issue.

<!-- --8<-- [end:properties] -->
