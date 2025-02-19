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
  - node-architecture
  - types
  - crypto
  - prelude
---

??? code "Juvix imports"
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

### `PrivateKey`
### `PrivateKey`

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

### `SecretKey`

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

### ``Signature``

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

### `hash`

```juvix
axiom hash {A} : A -> Digest;
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
