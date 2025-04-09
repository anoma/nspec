---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.data_structures.resource.computable_components.nullifier;
```

# Nullifier

A resource nullifier is computed from a [[Resource|resource object]] and a nullifier key. If it is published as element of the [[Nullifier set|nullifier set]] of the external global state, the resource associated with the nullifier is marked as consumed. Thus, knowledge of the resource nullifier is a necessary condition to consume a non-ephemeral resource (see also [[Roles and requirements#reliable-nullifier-key-distribution|Reliable nullifier key distribution]]).

For a resource `r`, `r.nullifier(nullifierKey) = nullifierHash(nullifierKey, r)`, where `nullifierKey` is a key provided externally.

A resource can be consumed at most once. Nullifiers of consumed resources are stored in a public append-only structure called the resource *nullifier set*. This structure is external to the resource machine, but the resource machine can read from it and append to it.

!!! note

    Whenever a non-ephemeral resource is to be consumed by a [[Transaction|transaction]], it has to be checked that the resource existed before and has not been consumed yet, i.e., the resource's commitment is in the commitment tree, but the resource's nullifier is not in the nullifier set, yet.
