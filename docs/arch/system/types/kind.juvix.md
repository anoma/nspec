---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - kind
  - resource-machine
  - type
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.kind;
    import prelude open;
    import arch.system.state.resource_machine.prelude open;
    ```

# Kind

A resource’s *kind* distinguishes its fungibility domain. A kind is produced as the digest of two
digests from the resouce; it's label and its logic.

## Computation

We assume an axiomatic function to combine a label and logic hash into a delta‐value.

```juvix
axiom kindHash : LabelHash -> LogicHash -> KindHash;
```
