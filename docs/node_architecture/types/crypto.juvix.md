## Cryptographic primitives

??? note "Juvix imports"

    ```juvix
    module node_architecture.types.crypto;
    import prelude open;
    ```

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
