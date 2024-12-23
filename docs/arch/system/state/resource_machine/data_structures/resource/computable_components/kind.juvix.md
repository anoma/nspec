---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.resource.computable_components.kind;
```

# Kind

For a resource `r`, its kind is computed as: `r.kind() = kindHash(r.labelRef, r.logicRef)`.

