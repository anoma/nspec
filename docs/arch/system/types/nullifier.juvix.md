---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - nullifier
  - resource-machine
  - state
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.nullifier;
    import prelude open;
    import arch.system.types.resource open;
    import arch.system.types.nullifierkey open;
    import arch.node.types.crypto open;
    ```

# Nullifiers

A *resource nullifier* or *nullifier* for short is a term of type `Nullifier`.
Each nullifier is data consisting of a `key` and the `resource` it is
associated with.

## `Nullifier`

```juvix
type Nullifier := mkNullifier {
  key : NullifierKey;
  resource : Resource;
};
```

???+ quote "Arguments"

    `key`
    : identifier of the nullifier

    `resource`
    : the resource that is presumed to be consumed

??? quote "Auxiliary Juvix code: Instances"

    ```juvix
    deriving
    instance
    nullifierEq : Eq Nullifier;
    ```

    ```juvix
    deriving
    instance
    nullifierOrd : Ord Nullifier;
    ```

## Purpose

Nullifiers prevent double-spending by:

1. Uniquely identifying *consumed resources* when stored in **the** nullifier
set part of the [[State|state]].

2. Requiring two factors to consume a resource, that is:

  - A nullifier key matching the resource's nullifier key commitment.

  - The resource nullifier must not exist in the [[Nullifier Set|nullifier set]].

## Properties

--8<-- "./nullifier_properties.juvix.md:properties"
