---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Computable components

Resource computable components are the components that are not a resource component but can be derived from the resource components, other computable components, and possibly some extra data.

Resources have four computable components:

1. [[Resource Commitment]]
2. [[Nullifier]]
3. [[Kind]]
4. [[Delta]]

### Tag

The resource *tag* is used to identify a resource when checking constraints without referring to the resource's plaintext directly: `tag(Resource, Bool) -> Commitment or Nullifier`.

For created resources: `r.tag(consumed=False) = r.commitment()`; for consumed resources: `r.tag(consumed=True) = r.nullifier(nullifierKey)`