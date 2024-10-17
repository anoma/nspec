---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
- Cryptography
- Crypto
---

??? note "Juvix imports"

    ```juvix
    module node_architecture.types.crypto;
    import prelude open;
    import Stdlib.Trait.Ord open using {Ordering; Ord; mkOrd; EQ};
    ```

## Cryptographic primitives

### Public key

```juvix
type PublicKey :=
  | Curve25519PubKey
  ;

instance
PublicKeyOrd : Ord PublicKey :=
  mkOrd@{
    cmp := \{_ _ := EQ};
  };
```

### Private key

```juvix
type PrivateKey :=
  | Curve25519PrivKey
  ;

instance
PrivateKeyOrd : Ord PrivateKey :=
  mkOrd@{
    cmp := \{_ _ := EQ};
  };
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
