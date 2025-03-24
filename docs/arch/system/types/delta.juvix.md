---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - delta
  - resource-machine
  - type
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.delta;
    import prelude open;
    import arch.system.state.resource_machine.prelude open;
    ```

# Resource Delta

A **delta** is a cryptographic commitment to the resource’s quantity (and
possibly other data). The Resource Machine can use this delta to track and
verify resource balances across different structures such as compliance units,
actions, or transactions.


## HasDelta Trait

We define a *HasDelta* trait for data types that can compute a `DeltaHash`:

```juvix
trait
type HasDelta (A : Type) :=
  mkHasDelta@{
    delta : A -> DeltaHash
  };
```
