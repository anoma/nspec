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

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.crypto;
    import prelude open;
    ```

## Cryptographic primitives

### Public key

Public key for public-key cryptography.

```juvix
type PublicKey :=
  | Curve25519PubKey ByteString
  ;
```

??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    PublicKeyEq : Eq PublicKey;
    ```

    ```juvix
    instance
    PublicKeyOrd : Ord PublicKey :=
      mkOrd@{
        cmp := \{_ _ := Equal};
      };
    ```

### Private key

Private key for public-key cryptography.

```juvix
type PrivateKey :=
  | Curve25519PrivKey ByteString
  ;
```

??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    PrivateKeyEq : Eq PrivateKey;

    instance
    PrivateKeyOrd : Ord PrivateKey :=
      mkOrd@{
        cmp := \{_ _ := Equal};
      };
    ```

### Secret key

Secret key for secret-key cryptography.

```juvix
type SecretKey :=
  | ChaCha20Key
  ;
```

??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    SecretKeyEq : Eq SecretKey;

    deriving
    instance
    SecretKeyOrd : Ord SecretKey;
    ```

### Signature

Cryptographic signature.

```juvix
type Signature :=
  | Ed25519Signature ByteString
```

### Digest

Message digest.
Output of a cryptographic hash function.

```juvix
type Digest :=
  | Blake3Digest ByteString
  ;
```

??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    DigestEq : Eq Digest;

    instance
    DigestOrd : Ord Digest :=
      mkOrd@{
        cmp := \{(Blake3Digest a) (Blake3Digest b) := Equal};
      };
    ```
