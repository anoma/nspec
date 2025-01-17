
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - resource-machine
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.tag;

    import arch.system.types.commitment open;
    import arch.system.types.nullifier open;
    ```

# Tags

A **tag** is a term of type `Tag`.

## `Tag`

```juvix
type Tag A :=
 | TagCommitment (Commitment A)
 | TagNullifier Nullifier
 ;
```

