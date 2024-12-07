---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data.resource.computable_components.introduction;
```

# Computable components

Resource computable components are the components that are not a resource
component but can be derived from the resource components, other computable
components, and possibly some extra data.

Resources have four computable components:

1. [`r.commitment()`](resource_commitment.md) 2.
[`r.nullifier(nullifierKey)`](nullifier.md) 3. [`r.kind()`](kind.md) 4.
[`r.delta()`](delta.md)
