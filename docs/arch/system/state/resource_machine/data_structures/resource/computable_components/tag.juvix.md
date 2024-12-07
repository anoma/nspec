---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.resource.computable_components.tag;
```

# Resource tag

The resource tag is used to identify a resource when checking constraints
without referring to the resource's plaintext directly: `tag(Resource, Bool) ->
Commitment or Nullifier`.

For created resources: `r.tag(consumed=False) = r.commitment()`; for consumed
resources: `r.tag(consumed=True) = r.nullifier(nullifierKey)`
