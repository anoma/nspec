---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Nullifier

A resource nullifier is a computed field, the publishing of which marks the resource associated with the nullifier as consumed. 

For a resource `r`, `r.nullifier(nullifierKey) = NullifierHash(nullifierKey, r)`, where `nullifierKey` is a key provided externally.

A resource can be consumed only once. Nullifiers of consumed resources are stored in a public append-only structure called the resource *nullifier set*. This structure is external to the resource machine, but the resource machine can read from it and append to it.

!!! note
    Every time a resource is consumed, it has to be checked that the resource existed before (the resource's commitment is in the commitment tree) and has not been consumed yet (the resource's nullifier is not in the nullifier set).


