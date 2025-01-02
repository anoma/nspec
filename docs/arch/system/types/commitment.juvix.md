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

## `Commitment`

```juvix
type Commitment A := mkCommitment@{
  value : A;
  hash : Digest;
};
```

!!! todo

    Determine if the type parameter is necessary, or it should be just
    String/Bytestring or something else.

???+ quote "Arguments"

    `value`
    : The value that is committed to.

    `hash`
    : The hash of the value.

## Purpose

Commitments are used to prove the existence of a value without revealing the
value itself. In the context of the resource machine, they are used to prove the
existence of resources. Precisely, commitments are meant to be stored in the
state of the resource machine in a [[CommitmentTree|commitment tree]] to be
queried by the resource machine.

## Properties

!!! todo

    Add properties of the commitment.

??? quote "Auxiliary Juvix code"

    ```juvix
    instance
    Commitment-Eq {A} {{Eq A}} : Eq (Commitment A)
      := mkEq@{
        eq := \{c1 c2 :=
          Commitment.hash c1 == Commitment.hash c2
        }
      };
    ```
