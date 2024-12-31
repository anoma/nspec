---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.nullifierkey;
    import prelude open;
    import arch.node.types.crypto open;
    ```

# Nullifier Key

A *resource nullifier key* is of type `NullifierKey`. A nullifier key is data
used to compute the nullifier of a resource and expected to be unique for each
resource.

## `NullifierKey`

```juvix
type NullifierKey := mkNullifierKey {
  key : SecretKey;
};
```

???+ quote "Arguments"

    `key`
    : an external secret key.


??? quote "Auxiliary Juvix code: Instances"

    ```juvix
    deriving
    instance
    nullifierKeyEq : Eq NullifierKey;
    ```

    ```juvix
    deriving
    instance
    nullifierKeyOrd : Ord NullifierKey;
    ```

## Purpose

The publishing of a resource nullifier key marks the resource associated with
the nullifier as consumed.
