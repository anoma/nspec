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
    module arch.node.types.crypto;
    import prelude open;
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
