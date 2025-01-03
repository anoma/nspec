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

Commitments are used to prove the existence of a value without revealing the
value itself. In the context of the resource machine, they are used to prove the
existence of resources. Precisely, commitments are meant to be stored in the
state of the resource machine in a [[CommitmentTree|commitment tree]] to be
queried by the resource machine.

## `Commitment`

```juvix
type Commitment A := mkCommitment@{
  value : A;
  hash : Digest;
};
```

???+ quote "Arguments"

    `value`
    : The value that is committed to.

    `hash`
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
    value := a;
    hash := hash a;
  };
```


## Properties

!!! todo

    Add properties of the commitment.

