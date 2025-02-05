---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - types
  - crypto
  - prelude
---

??? code "Juvix imports"

    ```juvix
    module arch.node.types.crypto;
    import prelude open;
    ```

# Cryptographic primitives

### `PublicKey`

Public key for public-key cryptography.

```juvix
type PublicKey :=
  | Curve25519PubKey ByteString
  ;

instance
PublicKeyOrd : Ord PublicKey :=
  mkOrd@{
    cmp := \{_ _ := Equal};
  };
```

### `PrivateKey`

Private key for public-key cryptography.

```juvix
type PrivateKey :=
  | Curve25519PrivKey ByteString
  ;

instance
PrivateKeyOrd : Ord PrivateKey :=
  mkOrd@{
    cmp := \{_ _ := Equal};
  };
```

### `SecretKey`

Secret key for secret-key cryptography.

```juvix
type SecretKey :=
  | ChaCha20Key
  ;
```

### `Signature`

Cryptographic signature.

```juvix
type Signature :=
  | Ed25519Signature ByteString
```

### `Digest`

Message digest.
Output of a cryptographic hash function.

```juvix
type Digest :=
  | Blake3Digest ByteString
  ;
```
