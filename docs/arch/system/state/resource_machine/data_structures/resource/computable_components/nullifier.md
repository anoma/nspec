---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Nullifier

A resource nullifier is a computed field, the publishing of which marks the resource associated with the nullifier as consumed.

For a resource `r`, `r.nullifier(nullifierKey) = nullifierHash(nullifierKey, r)`, where `nullifierKey` is a key provided externally.
<!--ᚦ«how is the nullifierKey related to the resource, e.g.,  1:1/1:many/many:1 ? »-->

A resource can be consumed only once. Nullifiers of consumed resources are stored in a public append-only structure called the resource *nullifier set*. This structure is external to the resource machine, but the resource machine can read from it and append to it.
<!--ᚦ«link to nullifier set»-->
<!--ᚦ«How does consumption "directly" imply addition to the nullifier set?»-->
<!--ᚦ«"but the resource machine can read from it and append to it."
How does it append to it (and is stateless at the same time)?
»-->

!!! note

    Every time a resource is consumed, it has to be checked that the resource existed before (the resource's commitment is in the commitment tree) and has not been consumed yet (the resource's nullifier is not in the nullifier set).
    <!--ᚦ«commitment tree → accumulator ? »-->


