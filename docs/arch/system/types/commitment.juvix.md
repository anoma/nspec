---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - commitment
  - resource-machine
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.commitment;
    import prelude open;
    import arch.node.types.crypto open;
    ```

# Commitment

## Purpose

Commitments prove the existence of a value without revealing it. In the resource
machine, they prove the existence of resources. Commitments are stored in the
resource machine's state within a [[CommitmentTree|commitment tree]] for
querying.

## `Commitment`

```juvix
type Commitment A := mkCommitment@{
  committed : A;
  commitment : Digest;
};
```

???+ quote "Arguments"

    `committed`
    : The value that is committed to.

    `commitment`
    : The hash of the value.

???+ quote "Auxiliary Juvix code: Instances"

    ```juvix
    deriving
    instance
    CommitmentEq {A} {{Eq A}} : Eq (Commitment A);
    ```

    ```juvix
    deriving
    instance
    CommitmentOrd {A} {{Ord A}} : Ord (Commitment A);
    ```

### `makeCommitment`

```juvix
makeCommitment {A} (a : A) : Commitment A :=
  mkCommitment@{
    committed := a;
    commitment := hash a;
  };
```


## Properties

!!! todo

    Add properties of the commitment.

