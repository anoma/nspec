---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.basics;
    import prelude open public;
    import prelude open using {Hash} public;
    import node_architecture.types.anoma_message as Anoma;
    import node_architecture.identities open;
    ```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[Juvix Base Prelude](./../prelude.juvix.md). (1)
{ .annotate }

1. :woman_raising_hand: If you are unfamiliar with Juvix,
please refer to the [Juvix documentation](https://docs.juvix.org/latest/tutorials/learn.html).

## Basic types

### RelTime

Relative time.
In seconds from now.

```juvix
syntax alias RelTime := Nat;
```

### AbsTime

Absolute time.
In minutes since epoch (2024-01-01 00:00).

```juvix
syntax alias AbsTime := Nat;
```

### Time

Either absolute or relative time.

```juvix
Time : Type := Either RelTime AbsTime;
```

### Version

Semantic version number (major.minor.patch).

```juvix
type Version : Type :=
  mkVersion {
    major : Nat;
    minor : Nat;
    patch : Nat;
  };
```

## Cryptographic primitives

### Public key

```juvix
type PublicKey :=
  | Curve25519PubKey
  ;
```

### Private key

```juvix
type PrivateKey :=
  | Curve25519PrivKey
  ;
```

### Signature

Cryptographic signature.

```juvix
type Signature :=
  | Ed25519Signature
```

### Digest

Message digest.
Output of a cryptographic hash function.

```juvix
type Digest :=
  | Blake3Digest
  ;
```
