---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Nullifier

A resource nullifier is a computed field, the publishing of which consumes the associated with the nullifier resource. For a resource $r$, the nullifier is computed from the resource's plaintext and a key called a nullifier key: $r.nf = h_{nf}(nk, r)$. A resource can be consumed only once. Nullifiers of consumed resources are stored in a public add-only structure called the resource nullifier set ($NFset$). This structure is external to the resource machine, but the resource machine can read from it.

> Every time a resource is consumed, it has to be checked that the resource existed before (the resource's commitment is in the $CMtree$) and has not been consumed yet (the resource's nullifier is not in the $NFset$).

The nullifier set must support the following functionality:

- `WRITE(nf)` adds an element to the nullifier set.
- `EXISTS(nf)` checks if the element is present in the set, returning a boolean.
