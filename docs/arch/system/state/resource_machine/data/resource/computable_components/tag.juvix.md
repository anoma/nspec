---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data.resource.computable_components.tag;
import arch.system.state.resource_machine.data.resource.definition
open;
```

# Resource tag

The resource tag is used to identify a resource when checking constraints
without referring to the resource's plaintext directly.


```juvix
axiom Commitment : Type;
axiom Nullifier : Type;
--- The reference to the ;Resource;.
type Tag :=
  | Created Commitment
  | Consumed Nullifier;
```


For created resources: `r.tag(consumed=False) = r.commitment()`; for consumed
resources: `r.tag(consumed=True) = r.nullifier(nullifierKey)`
