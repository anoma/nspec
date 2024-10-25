---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module system_architecture.identity.identity;
    import prelude open;
    import Stdlib.Data.Nat as Nat open using {Nat; +; *; <=} public;
    import Stdlib.Trait.Eq as Eq open using {==} public;
    import Stdlib.Trait.Ord as Ord open using {Ordering; EQ} public;
    ```

# Identity Architecture

??? note "Type definitions"

    ```juvix
    type OrdKey (OrdKey : Type) :=
      mkOrdkey {
          compare : OrdKey -> OrdKey -> Ordering
      };
    ```

    ```juvix
    type HASH (OrdKeyType Hashable : Type) :=
      mkHASH {
        ordKey : OrdKey OrdKeyType;
        hash : Hashable -> OrdKeyType
      };
    ```

    ```juvix
    -- Note: instance of this with Data.Map should be made
    type OrdMap (OrdKeyType : Type) (MapCon : Type -> Type) :=
      mkOrdMap {
        ordKey : OrdKey OrdKeyType;
        empty : {a : Type} -> MapCon a;
        map : {a b : Type} -> (a -> b) -> MapCon a -> MapCon b;
        insert : {a : Type} -> Pair (MapCon a) (Pair OrdKeyType a) -> MapCon a;
        foldl : {a b : Type} -> (Pair a b -> b) -> b -> MapCon a -> b;
        intersectWith : {a b c : Type} -> (Pair a b -> c) -> Pair (MapCon a) (MapCon b) -> MapCon c;
        all : {a : Type} -> (a -> Bool) -> MapCon a -> Bool
        -- Bunch of stuff, see https://www.smlnj.org/doc/smlnj-lib/Util/sig-OrdMap.html
      };
    ```

The base abstraction of the protocol is a knowledge-based identity
 interface, where the identity of an agent is defined entirely on the
 basis of whether or not they know some secret information.

Agents can use private information (likely randomness) to create an
 _internal identity_, from which they can derive an
 _external identity_ to which it corresponds.
The external identity can be shared with other parties.
The agent who knows the internal identity can sign messages, which any
 agent who knows the external identity can verify, and any agent who
 knows the external identity can encrypt messages which the agent with
 knowledge of the internal identity can decrypt.
This identity interface is independent of the particular cryptographic
 mechanisms, which may vary.

## Identity Interface

### Internal Identity

An internal identity includes private information necessary for signing and
 decryption. Formally, an internal identity has two parts: a Signer and a
Decryptor.

#### Signer Juvix Type

A signature describing a type `SignerType` that can cryptographically
 `sign` (or credibly commit) to something (a `Signable`), forming a
 `Commitment`.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature) keys,
  which should be able to sign anything that can be marshaled into a
  bitstring.

Properties:

- In general, every `S : Signer` needs a corresponding `V : Verifier`, and
  every `s : SignerType` needs a corresponding `v : VerifierType`, such that:

  - For any message `m` : `verify v m x = (x = (sign s m))`

  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.

```juvix
type Signer (SignerType Signable Commitment : Type) :=
  mkSigner {
    sign : SignerType -> Signable -> Commitment
  };
```

#### Decryptor Juvix Type

A signature describing a type `DecryptorType` that can cryptographically
 `decrypt` something (a `Ciphertext`), resulting in a `Plaintext`
 (or `none`, if decryption fails).
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be unmarshaled from a bitstring.

Properties:

- a computationally bounded adversary should not be able to
  approximate `decrypt d` without knowledge of `d`.

- `decrypt` should take polynomial time (in the size of its inputs)

- Each `D : Decryptor` should have a corresponding `E : Encryptor`, and
  each `d : DecryptorType` has a corresponding `e : EncryptorType` such
  that:

  - for all `c : Ciphertext`, `p : Plaintext`:
    `decrypt d c = Some p` iff `c = encrypt e p`

  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption"

```juvix
type Decryptor (DecryptorType Plaintext Ciphertext : Type) :=
  mkDecryptor {
    decrypt : DecryptorType -> Ciphertext -> Option Plaintext
  }
```

#### Internal Identity Juvix Type

An Internal Identity structure simply specifies everything specified by
both Signer and Decryptor.

An Internal Identity structure specifies the necessary types and
 functions for both a Signer and a Decryptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) private keys,
 which should be able to decrypt integers into anything that can be
 unmarshaled from a bitstring, and sign anything which can be
 marshaled into a bytestring to form an integer.

An internal_identity includes:

- a type `SignerType` that can cryptographically
  `sign` (or credibly commit) to something (a `Signable`), forming a
  `Commitment`.

- a type `DecryptorType` that can cryptographically `decrypt` something
  (a `Ciphertext`), resulting in a `Plaintext`
  (or `none`, if decryption fails).

Properties are inherited from `Signer` and `Decryptor`.

```juvix
type InternalIdentity (SignerType Signable Commitment DecryptorType Plaintext Ciphertext : Type) :=
  mkInternalIdentity {
    signer : Signer SignerType Signable Commitment;
    decryptor : Decryptor DecryptorType Plaintext Ciphertext
  }
```

### External Identity

An external identity includes only public information. An external identity can
verify signatures produced by an internal identity, and encrypt messages the
internal identity can then decrypt. Formally, an external identity has two parts:
a verifier and an Encryptor. Each is _hashable_: any
[structure](https://www.cs.cornell.edu/riccardo/prog-smlnj/notes-011001.pdf#page=59)
specifying verifier and Encryptor types must also specify a hash function, so
that external identities can be specified by hash.

#### Verifier Juvix Type

A signature describing a type `VerifierType` that can cryptographically
 `verify` that a `Commitment` (or cryptographic signature) corresponds
 to a given message (a `Signable`), and was signed by the `SignerType`
 corresponding to this `VerifierType`.
A `VerifierType` can be hashed (producing a unique identifier), so a
 structure with signature `Verifier` must specify a `VerifierHash`
 structure defining a suitable `hash` function.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature)
 identities.

Properties:

- In general, every `V : Verifier` needs a corresponding `S : Signer`, and
  every `s : SignerType` needs a corresponding `v : VerifierType`, such that:

  - For any message `m` : `verify v m x = (x = (sign s m))`

  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.

```juvix
type Verifier (OrdKey VerifierType Signable Commitment : Type) :=
  mkVerifier {
    verify : VerifierType -> Signable -> Commitment -> Bool;
    verifierHash : HASH OrdKey VerifierType
  }
```

#### Encryptor Juvix Type

A signature describing a type `EncryptorType` that can cryptographically
 `encrypt` a `Plaintext` (message) to create a `Ciphertext` readable
 only by the corresponding `DecryptorType`.
An `EncryptorType` can be hashed (producing a unique identifier), so a
 structure with signature `Encryptor` must specify an `encryptorHash`
 structure defining a suitable hash function.
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be  unmarshaled from a bitstring.

Properties:

- `encrypt` should take polynomial time (in the size of its inputs)

- Each `E : Encryptor` should have a corresponding `D : Decryptor`, and
  each `d : DecryptorType` has a corresponding `e : EncryptorType` such
  that:

  - for all `c : Ciphertext`, `p : Plaintext`:
    `decrypt d c = Some p` iff `c = encrypt e p`

  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption."
    In an asymmetric cryptosystem, a computationally bounded adversary
    should not be able to approximate `d` knowing only `e`.

```juvix
type Encryptor (OrdKey EncryptorType Plaintext Ciphertext : Type) :=
  mkEncryptor {
    encrypt : EncryptorType -> Plaintext -> Ciphertext;
    encryptorHash : HASH OrdKey EncryptorType
  }
```

#### External Identity Juvix Type

An External Identity structure specifies the necessary types and
 functions for both a Verifier and an Encryptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) public keys.

An external_identity includes:

- a type `VerifierType` that can cryptographically `verify` that a
  `Commitment` (or cryptographic signature) corresponds to a given
  message (a `Signable`), and was signed by the `SignerType`
  corresponding to this `VerifierType`.

- a type `EncryptorType` that can cryptographically `encrypt` a
  `Plaintext` (message) to create a `Ciphertext` readable only by the
  corresponding `DecryptorType`.

Properties are inherited from `Verifier` and `Encryptor`.

```juvix
type ExternalIdentity (
    VerifierOrdKeyType VerifierType Signable Commitment
    EncryptorOrdKeyType EncryptorType Plaintext Ciphertext : Type) :=
  mkExternalIdentity {
    verifier : Verifier VerifierOrdKeyType VerifierType Signable Commitment;
    encryptor : Encryptor EncryptorOrdKeyType EncryptorType Plaintext Ciphertext
  };
```

### Identity Juvix Type

An Identity structure, formally, specifies all the types for
 corresponding internal and external identities.
So, for a given Identity structure `I`, its `VerifierType` should be the
 type of objects that can verify `Commitment`s produced by a
 corresponding object of type `SignerType`.
Likewise, its `DecryptorType` should be the type of objects that can decrypt
 `Ciphertext`s produced by a corresponding object of type
 `EncryptorType`.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
 public / private keys sytems.

An Identity includes:

- a type `SignerType` that can cryptographically `sign` (or credibly commit) to something (an `InternalSignable`), forming an `InternalCommitment`.

- a type `DecryptorType` that can cryptographically `decrypt` something (an `InternalCiphertext`), resulting in an `InternalPlaintext` (or `none`, if decryption fails).

- a type `VerifierType` that can cryptographically `verify` that an `ExternalCommitment` (or cryptographic signature) corresponds to a given message (an `ExternalSignable`), and was signed by the `SignerType` corresponding to this `VerifierType`.

- a type `EncryptorType` that can cryptographically `encrypt` an `ExternalPlaintext` (message) to create an `ExternalCiphertext` readable only by the corresponding `DecryptorType`.

Properties are inherited from `Verifier`, `Encryptor`, `Signer`, and `Decryptor`.

```juvix
type Identity (
  SignerType InternalSignable InternalCommitment
  DecryptorType InternalCiphertext InternalPlaintext
  VerifierOrdKeyType
  VerifierType ExternalSignable ExternalCommitment
  EncryptorOrdKeyType
  EncryptorType ExternalPlaintext ExternalCiphertext
 : Type) :=
  mkIdentity {
    internalIdentity : InternalIdentity SignerType InternalSignable InternalCommitment DecryptorType InternalPlaintext InternalCiphertext;
    externalIdentity : ExternalIdentity VerifierOrdKeyType VerifierType ExternalSignable ExternalCommitment EncryptorOrdKeyType EncryptorType ExternalPlaintext ExternalCiphertext
  };
```

## SignsFor Relation

Some identities may have the authority to sign statements on behalf of other
 identities. For example, _Alice_ might grant _Bob_ the authority to sign
arbitrary messages on her behalf. We write this relationship as _Bob_ `signsFor`
 _Alice_.

In general, `signsFor` is a partial order over identities. This means
`signsFor` is transitive: if _A_ `signsFor` _B_ and _B_ `signsFor` _C_, then _A_
 `signsFor` _C_. The `signsFor` relation becomes especially useful with regard
to [composed identities, discussed below](#composition).

### SignsFor Evidence

We do not specify all the ways one might know if one identity `signsFor`
another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As one simple form of
evidence, we can specify a format for signed statements from _B_ that proves
some specified _A_ `signsFor` _B_.

Note that `signsFor` evidence cannot be revoked, and so a `signsFor` relation is
not _stateful_: it cannot depend on the current state of, for example, a
blockchain.

#### SignsFor Juvix Type

Formally, a `signsFor` relation requires a type of evidence, and a
 `Verifier` structure.
This codifies a belief about what `VerifierType`'s `Commitments` are
 "at least as good as" another `VerifierType`'s.
Evidence can be signed statements, proofs, or even local state about beliefs.

For example, suppose `Alice` wants to grant authority to `Bob` to
 `sign` on her behalf.
Nodes who want to take this into account might accept some sort of
 `e : Evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `signsFor e (Bob, Alice)`.

Note that `signsFor` is not symmetric: `signsFor e (x,y)` does not
 imply that any `z` exists such that `signsFor z (y,x)`.

```juvix
type SignsFor (OrdKey VerifierType Signable Commitment Evidence : Type) :=
  mkSignsFor {
    verifier : Verifier OrdKey VerifierType Signable Commitment;
    signsFor : Evidence -> (Pair VerifierType VerifierType) -> Bool
  };
```

### SignsFor Equivalence

We can also define a kind of identity _equivalence_ : _A_ `signsSameAs` _B_
 precisely when _A_ `signsFor` _B_ and _B_ `signsFor` _A_. This means that (in
 general), if you want to sign a message as _A_, but for whatever reason it's
cheaper to sign a message as _B_, it's safe to just use _B_ instead, and vice
 versa.

## ReadsFor Relation

Similar to `signsFor`, it is useful to sometimes note that one identity can read
 information encrypted to another identity. For example, suppose _Alice_ gives
her private `DecryptorType` to _Bob_, and wants to let everyone know that _Bob_ can
 now read anything encrypted to _Alice_. Nodes who want to take this into
 account might accept some sort of `evidence`, perhaps a signed statement from
_Alice_, so that they can recognize that _Bob_ `readsFor` _Alice_.

Like `signsFor`, `readsFor` is a partial order over identities. This means
`readsFor` is transitive: if _A_ `readsFor` _B_ and _B_ `readsFor` _C_, then _A_
 `readsFor` _C_. The `readsFor` relation becomes especially useful with regard
to [composed identities, discussed below](#composition).

### ReadsFor Evidence

We do not specify all the ways one might know if one identity `readsFor`
 another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As one simple form of
 evidence, we can specify a format for signed statements from _B_ that proves
_A_ `readsFor` _B_.

#### ReadsFor Juvix Type

Formally, a `readsFor` relation requires a type of evidence, and an
 `Encryptor` structure.
This codifies a belief about what `Decryptor`s can read other
 `Encryptor`s ciphertext.
Evidence can be signed statements, proofs, or even local state about beliefs.

Specifically, if a node expresses a `readsFor` relation, and
 `readsFor e (x,y)`, then the node believes that any node knowing the
 decryptor corresponding to `x` can decrypt `encrypt y p`.
If there is some Plaintext `p` such that some node knowing a decryptor
 corresponding to `x` cannot read `encrypt y p`, then the node's
 beliefs, as encoded in the `readsFor` relation, are incorrect.

For example, suppose `Alice` gives her private `DecryptorType` to `Bob`,
 and wants to let everyone know that `Bob` can now read anything
 encrypted to `Alice`.
Nodes who want to take this into account might accept some sort of
 `e : Evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `readsFor e (Bob, Alice)`.

Note that `readsFor` is not symmetric: `readsFor e (x,y)` does not
 imply that any `z` exists such that `readsFor z (y,x)`.

```juvix
type ReadsFor (OrdKey EncryptorType Plaintext Ciphertext Evidence : Type) :=
  mkReadsFor {
    encryptor : Encryptor OrdKey EncryptorType Plaintext Ciphertext;
    readsFor : Evidence -> (Pair EncryptorType EncryptorType) -> Bool
  }
```

### Equivalence

We can also define a kind of identity _equivalence_: _A_ `readsSameAs` _B_
precisely when _A_ `readsFor` _B_ and _B_ `readsFor` _A_. This means that, in
general, if you want to encrypt a message to _A_, but for whatever reason it's
cheaper to encrypt a message for _B_, it's safe to just use _B_ instead, and
vice versa.

In total, _A_ `equivalent` _B_ when _A_ `readsSameAs` _B_ and _A_ `signsSameAs`
_B_. This means that (in general) _A_ and _B_ can be used interchangeably.

## Composition

There are a variety of ways to refer to groups of identities as
 single, larger identities.

### Threshold Composition

Suppose we want an identity _M_ that refers to any majority from a
 set of shareholders.
A signature from _M_ would require that a majority of shareholders
 participated in signing, and encrypting information for _M_ would
 require that a majority of shareholders participate in decryption.
To construct _M_, we start with a set of shareholder identities, each
 paired with a _weight_ (their share), and define a weight threshold
 which specifies the minimum weight for a "majority."

There are several ways we could imagine constructing Threshold
 Composition Identities, but without specifying _anything_ about the
 underlying identities:

- A threshold composition identity signature is a map from (hashes of)
   external identities, to signatures.
  To verify a signature for some message `x`, we verify each signature
   with `x` and its external identity, and check that the weights of
   the external identities sum to at least the threshold.

- A threshold composition identity encrypted message is a map from
   (hashes of) external identities, to ciphertexts.
  To decrypt, any subset of internal identities with weights summing
   to at least the threshold must decrypt their corresponding
   ciphertexts, and the resulting plaintexts must be combined using an
   erasure coding scheme.

#### Threshold Composition Juvix Type (Signer and verifier)

A `ThresholdCompose` `VerifierType` consists of a
 threshold (`Nat`), and a set of `VerifierType`s, each paired with a
 weight (`Nat`).
 (this set is encoded as a `Map.map` from hashes of `verifiers` to
  `Pair Nat VerifierType` pairs).
`Commitments` are simply `Map`s from hashes of the underlying
 identities to `Commitments` signed by that identitity.
A `Commitment` verifies iff the set of valid Commitments included
 correspond to a set of `verifiers` whose weights sum to at least
 the threshold.
Note that this satisfies both signatures `Verifier` and `Signer`.

In general, `ThresholdCompose` `SignerType`s and `VerifierType`s may not be
 used much directly.
Instead, nodes can make more efficient identities (using cryptographic
 signature aggregation techniques), and express their relationship to
 `ThresholdCompose` `VerifierType`s as a `SignsFor` relationship.
This will let nodes reason about identities using simple
 `ThresholdCompose` `VerifierType`s, while actually using more efficient
 implementations.

Formally, to specify a `ThresholdCompose`, we need:

- `verifier`, the structure of the underlying `Verifiers`.

- `signer`, the corresponding structure of the underlying `Signers`.

- `map : OrdMap`, to be used to encode weights and `Commitment`s.
  (Note that this needs the `OrdKey` to be the hash type of the
   underlying `verifier`)

- `thresholdComposeHash`, which specifies a `hash` function that can
   hash our composed `VerifierType`s (type `ComposeHashable VerifierType MapCon`).

```juvix
type ComposeHashable (VerifierType : Type) (MapCon : Type -> Type) :=
  mkComposeHashable {
    threshold : Nat;
    weights : MapCon (Pair Nat VerifierType)
  };
```

A `ThresholdCompose` structure provides:

- `map : OrdMap` the underlying `OrdMap` used in
   `VerifierType` and `Commitment`

- `underlyingVerifier : Verifier` the structure describing
   the types of the underlying `VerifierType`s which can be composed.

- `underlyingSigner : Signer` the structure describing
   the types of the underlying `SignerType`s which can be composed.

- `VerifierHash : HASH` describes the hash function for
   hashing these composed `verifiers`

- The `SignerType` type of the composed verifiers is the type of composed signers.
   These are just `MapCon Commitment`, meaning each is
   stored under the hash of the corresponding
   `VerifierType`.
   This `SignerType` does not need to encode weights or threshold.

- The `VerifierType` type of composed verifiers. These are
   `ComposeHashable VerifierType MapCon`

- The `Signable` type , being the type of message that can be signed. This is
   exactly the same as what the underlying verifiers can sign
   (`Signable` of `underlyingVerifier`).

- The `Commitment` type describes composed signatures, these are a
   `MapCon` from hashes of underlying verifiers to signatures
   (`Commitment` of `underlyingVerifier`)

- The `sign` function creates a `Commitment` using all
   `underlyingSigner` `SignerType`s in the composed `SignerType`.

- The `verify` function returns true iff the set of valid Commitments included
   correspond to a set of `underlyingVerifier` `VerifierType`s whose weights
   sum to at least the threshold.

- The `signerCompose` function constructs a composed `SignerType` from a list of
   `Pair VerifierType SignerType` pairs.
   Note that each `SignerType` must be paired with its correct `VerifierType`,
    or the composed `SignerType` will not produce verifiable
    `Commitment`s.

- The `verifierCompose` function is useful for constructing the composition of
   a list of verifiers.
  Returns a composed `VerifierType`.
  Its arguments are:

  - the threshold (`Nat`)

  - a `list` of weights(`Nat`), `VerifierType` pairs.

- The `verifierAnd` function creates a composed `VerifierType` that is the "&&" of
   two input verifiers: a `SignerType` must encode the information of the
   signers for *both* `x` and `y` to sign statements `verifierAnd x y`
   will verify.

- The `verifierOr` function creates a composed `VerifierType` that is the "||" of
   two input verifiers: a `SignerType` must encode the information of the
   signers for *either* `x` or `y` to sign statements `verifierOr x y`
   will verify.

```juvix
type ThresholdCompose
  ( OrdKey : Type ) ( MapCon : Type -> Type )
  ( VerifierType Signable Commitment SignerType VerifierHashOrdKeyType : Type)
  :=
  mkThresholdCompose {
    map : OrdMap OrdKey MapCon;
    underlyingVerifier : Verifier OrdKey VerifierType Signable Commitment;
    underlyingSigner : Signer SignerType Signable Commitment;
    verifierHash : HASH VerifierHashOrdKeyType (ComposeHashable VerifierType MapCon);

    sign : MapCon SignerType -> Signable -> MapCon Commitment;
    verify : (ComposeHashable VerifierType MapCon) -> Signable -> MapCon Commitment -> Bool;
    signerCompose : List (Pair VerifierType SignerType) -> MapCon SignerType;
    verifierCompose : Nat -> List (Pair Nat VerifierType) -> (ComposeHashable VerifierType MapCon);
    verifierAnd : VerifierType -> VerifierType -> (ComposeHashable VerifierType MapCon);
    verifierOr : VerifierType -> VerifierType -> (ComposeHashable VerifierType MapCon);
  };
```

```juvix
projectVerifier
  { MapCon : Type -> Type }
  { OrdKey VerifierType Signable Commitment SignerType VerifierHashOrdKeyType : Type }
  ( tc : ThresholdCompose OrdKey MapCon VerifierType Signable Commitment SignerType VerifierHashOrdKeyType ) :
  Verifier VerifierHashOrdKeyType (ComposeHashable VerifierType MapCon) Signable (MapCon Commitment) :=
  mkVerifier@{
    verify := ThresholdCompose.verify tc;
    verifierHash := ThresholdCompose.verifierHash tc;
  };
```

```juvix
ThresholdComposeFunctor
  { MapCon : Type -> Type }
  { OrdKey VerifierType Signable Commitment SignerType VerifierHashOrdKeyType : Type }
  (verifier : Verifier OrdKey VerifierType Signable Commitment)
  (signer : Signer SignerType Signable Commitment)
  (mapIn : OrdMap OrdKey MapCon)
  (thresholdComposeHash : HASH VerifierHashOrdKeyType (ComposeHashable VerifierType MapCon)) :
  ThresholdCompose
    OrdKey MapCon
    VerifierType Signable Commitment
    SignerType
    VerifierHashOrdKeyType
  :=
  mkThresholdCompose@{
    map := mapIn;
    underlyingVerifier := verifier;
    underlyingSigner := signer;
    verifierHash := thresholdComposeHash;
    sign := \ {s m := OrdMap.map map \ { i := Signer.sign underlyingSigner i m } s};
    verify := \ {
      | (mkComposeHashable t ws) s c := (
          t <= (
            OrdMap.foldl map \{(mkPair x y) := x + y} 0 (
              OrdMap.intersectWith map (
                \{ | (mkPair (mkPair w v) x) :=
                      ite (Verifier.verify underlyingVerifier v s x) w 0
                }
            ) (mkPair ws c)))
      )
    };

    signerCompose := \{ l :=
        foldl
        \{ m (mkPair v s) :=
          OrdMap.insert map (mkPair m (mkPair (
            HASH.hash (Verifier.verifierHash underlyingVerifier) v
          ) s))
        }
        (OrdMap.empty map) l
    };

    verifierCompose := \{
      threshold weights :=
        (mkComposeHashable threshold
          (foldl
            \ { m (mkPair w v) :=
              OrdMap.insert map (mkPair m (mkPair (
                HASH.hash (Verifier.verifierHash underlyingVerifier) v
              ) (mkPair w v)))
            }
            (OrdMap.empty map) weights
        ))
    };

    verifierAnd := \{ x y := verifierCompose 2 [(mkPair 1 x); (mkPair 1 y)]};
    verifierOr := \{ x y := verifierCompose 1 [(mkPair 1 x); (mkPair 1 y)] };
  };
```

While this construction is rather naive, it is general, and crucially, we can reason about
 equivalence with any number of more interesting schemes:

- We can show that a threshold RSA signature scheme `signsSameAs` as a Threshold Composition
   Identity.

- We can show that a secret sharing scheme `readsSameAs` a Threshold Composition Identity.

By phrasing our discussion in terms of equivalence and Threshold Composition Identities, we can
 abstract over the actual cryptography used. We can also derive some `signsFor` and `readsFor`
 relations that must hold, by looking at the relations that must hold for Threshold Composition
Identities:

#### `signsFor` Threshold Composition

Like any identity, Threshold Composition Identities can define any number of ways to delegate
signing power, or be delegated signing power. However, some cases should always hold: _A_
`signsFor` _B_ if every identity in _A_ has no more weight (divided by threshold) than identities
it `signsFor` in _B_. This implies that any collection of identities that can sign as _A_ can also
sign as _B_.

 A `signsFor` relation for easy comparison of
  `ThresholdCompose` `VerifierType`s
 _x_ `signsFor` _y_ if every underlying VerifierType in _x_ has no more
  weight (divided by threshold) as verifiers it `signsFor` in y.
This implies that anything which can sign as _x_ can also sign
 as _y_.

This requires an underlying `S : SignsFor` for comparing the weighted
 signers in _x_ and _y_, which in turn may require evidence.
No additional evidence is required.

Other parameters necessary to define the `ThresholdCompose`
 `verifiers` include:

- `signer`, the corresponding structure of the underlying `signers`.

- `map : OrdMap`, to be used to encode weights and `Commitment`s.
  (Note that this needs `OrdKey` to be the hash type of the
   underlying `verifier`)

- `thresholdComposeHash`, which specifies a `hash` function that can
   hash our composed `VerifierType`s (type
   `ComposeHashable VerifierType MapCon`).

```juvix
type ThresholdComposeSignsFor
  ( OrdKey VerifierType Signable Commitment Evidence : Type )
  ( MapCon : Type -> Type )
  ( VerifierHashOrdKeyType )
  :=
  mkThresholdComposeSignsFor {
    underlyingSignsFor : SignsFor OrdKey VerifierType Signable Commitment Evidence;
    verifier : ThresholdCompose OrdKey MapCon VerifierType Signable Commitment VerifierType VerifierHashOrdKeyType;
    signsFor : Evidence -> Pair (ComposeHashable VerifierType MapCon) (ComposeHashable VerifierType MapCon) -> Bool;
  };
```

```juvix
projectSignsFor
  { OrdKey VerifierType Signable Commitment Evidence : Type }
  { MapCon : Type -> Type }
  { VerifierHashOrdKeyType : Type }
  ( tc : ThresholdComposeSignsFor OrdKey VerifierType Signable Commitment Evidence MapCon VerifierHashOrdKeyType ) :
  SignsFor VerifierHashOrdKeyType (ComposeHashable VerifierType MapCon) Signable (MapCon Commitment) Evidence :=
  mkSignsFor@{
    verifier := projectVerifier (ThresholdComposeSignsFor.verifier tc);
    signsFor := ThresholdComposeSignsFor.signsFor tc;
  };
```

```juvix
ThresholdComposeSignsForFunctor
  { OrdKey VerifierType Signable Commitment Evidence : Type }
  { MapCon : Type -> Type }
  { VerifierHashOrdKeyType : Type }
  ( S : SignsFor OrdKey VerifierType Signable Commitment Evidence )
  ( signer : Signer VerifierType Signable Commitment)
  ( map : OrdMap OrdKey MapCon )
  ( thresholdComposeHash : HASH VerifierHashOrdKeyType (ComposeHashable VerifierType MapCon) ) :
  ThresholdComposeSignsFor OrdKey VerifierType Signable Commitment Evidence MapCon VerifierHashOrdKeyType
  :=
  mkThresholdComposeSignsFor@{
    underlyingSignsFor := S;
    verifier := ThresholdComposeFunctor (SignsFor.verifier underlyingSignsFor) signer map thresholdComposeHash;
    signsFor := \{
      e (mkPair (mkComposeHashable t0 w0) (mkComposeHashable t1 w1)) :=
        OrdMap.all map
          \{ (mkPair w v) :=
              (w * t1) <=
              ((OrdMap.foldl map
                \{ (mkPair (mkPair x v1) s) :=
                    ite (SignsFor.signsFor underlyingSignsFor e (mkPair v v1)) (x + s) s
                }
                0 w1
                ) * t0)
          }
          w0
    };
  };
```

#### `Encryptor` Threshold Composition

 DANGER: NOT YET IMPLEMENTED

 Implementing this requires secret sharing.
 The threshold composed `encryptor` is a threshold, and a set of weights
 paired with `UnderlyingEncryptor.encryptor`s. There are stored in a `Map.map`
 under their hashes, to ensure uniqueness.

 The idea is that an encrypted `plaintext` should only be
 decryptable by a `decryptor` that encodes the information from a
 set of `decryptor`s corresponding to a set of `encryptor`s whose
 weight sums to at least the threshold.

```juvix
type ThresholdComposeEncryptor
  (OrdKey EncryptorType Plaintext Ciphertext : Type)
  (MapCon : Type -> Type)
  (EncryptorHashOrdKeyType : Type)
  :=
  mkThresholdComposeEncryptor {
    map : OrdMap OrdKey MapCon;
    underlyingEncryptor : Encryptor OrdKey EncryptorType Plaintext Ciphertext;
    encryptorHash : HASH EncryptorHashOrdKeyType (ComposeHashable EncryptorType MapCon);
    compose : Nat -> List (Pair Nat EncryptorType) -> ComposeHashable EncryptorType MapCon;
    encrypt : (ComposeHashable EncryptorType MapCon) -> Plaintext -> Ciphertext;
  };
```

```juvix
projectEncryptor
  {OrdKey EncryptorType Plaintext Ciphertext : Type}
  {MapCon : Type -> Type}
  {EncryptorHashOrdKeyType : Type}
  (tc : ThresholdComposeEncryptor OrdKey EncryptorType Plaintext Ciphertext MapCon EncryptorHashOrdKeyType) :
  Encryptor EncryptorHashOrdKeyType (ComposeHashable EncryptorType MapCon) Plaintext Ciphertext
  :=
  mkEncryptor@{
    encrypt := ThresholdComposeEncryptor.encrypt tc;
    encryptorHash := ThresholdComposeEncryptor.encryptorHash tc;
  };
```

```juvix
axiom encrypt_DUMMY :
  {EncryptorType Plaintext Ciphertext : Type} -> {MapCon : Type -> Type} ->
  (ComposeHashable EncryptorType MapCon) -> Plaintext -> Ciphertext;
```

```juvix
ThresholdComposeEncryptorFunctor
  {OrdKey EncryptorType Plaintext Ciphertext : Type}
  {MapCon : Type -> Type}
  {EncryptorHashOrdKeyType : Type}
  (encryptor : Encryptor OrdKey EncryptorType Plaintext Ciphertext)
  (mapIn : OrdMap OrdKey MapCon)
  (thresholdComposeHash : HASH EncryptorHashOrdKeyType (ComposeHashable EncryptorType MapCon)) :
  ThresholdComposeEncryptor OrdKey EncryptorType Plaintext Ciphertext MapCon EncryptorHashOrdKeyType
  := mkThresholdComposeEncryptor@{
    map := mapIn;
    underlyingEncryptor := encryptor;
    encryptorHash := thresholdComposeHash;
    compose := \{
      t w :=
        mkComposeHashable@{
          threshold := t;
          weights :=
            foldl
              \{m (mkPair w e) :=
                OrdMap.insert map (mkPair m (mkPair (HASH.hash (Encryptor.encryptorHash underlyingEncryptor) e) (mkPair w e)))
              }
              (OrdMap.empty map) w
        }
    };
    encrypt := encrypt_DUMMY;
  };
```

#### `readsFor` Threshold Composition

Like any identity, ThresholdCompositionIdentities can have arbitrary
 `readsFor` relationships.
However, some cases should always hold : _A_ `readsFor` _B_ if every
 identity in _A_ has no more weight (divided by threshold) than
 identities it `readsFor` in _B_.
This implies that any collection of identities that can read messages
 encrypted with _A_ can also read messages encrypted as _B_.

 A `readsFor` relation for easy comparison of
  `ThresholdComposeEncryptor` `EncryptorType`s
 _x_ `readsFor` _y_ if every underlying `EncryptorType` in _x_ has no more
  weight (divided by threshold) as encryptors it `readsFor` in y.
This implies that anything which can decrypt as _x_ can also decrypt
 as _y_.

This requires an underlying `R : ReadsFor` for comparing the weighted
 encryptors in  _x_ and _y_, which in turn may require evidence.
No additional evidence is required.

```juvix
type ThresholdComposeReadsFor
  ( OrdKey EncryptorType Plaintext Ciphertext Evidence : Type )
  ( MapCon : Type -> Type )
  ( EncryptorHashOrdKeyType : Type )
  :=
  mkThresholdComposeReadsFor {
    underlyingReadsFor : ReadsFor OrdKey EncryptorType Plaintext Ciphertext Evidence;
    encryptor : ThresholdComposeEncryptor OrdKey EncryptorType Plaintext Ciphertext MapCon EncryptorHashOrdKeyType;
    readsFor : Evidence -> Pair (ComposeHashable EncryptorType MapCon) (ComposeHashable EncryptorType MapCon) -> Bool;
  };
```

```juvix
projectReadsFor
  { OrdKey VerifierType Signable Commitment Evidence : Type }
  { MapCon : Type -> Type }
  { EncryptorHashOrdKeyType : Type }
  ( tc : ThresholdComposeReadsFor OrdKey VerifierType Signable Commitment Evidence MapCon EncryptorHashOrdKeyType ) :
  ReadsFor EncryptorHashOrdKeyType (ComposeHashable VerifierType MapCon) Signable Commitment Evidence :=
  mkReadsFor@{
    encryptor := projectEncryptor (ThresholdComposeReadsFor.encryptor tc);
    readsFor := ThresholdComposeReadsFor.readsFor tc;
  };
```

```juvix
ThresholdComposeReadsForFunctor
  { OrdKey EncryptorType Plaintext Ciphertext Evidence : Type }
  { MapCon : Type -> Type }
  { EncryptorHashOrdKeyType : Type }
  ( r : ReadsFor OrdKey EncryptorType Plaintext Ciphertext Evidence )
  ( map : OrdMap OrdKey MapCon )
  ( thresholdComposeHash : HASH EncryptorHashOrdKeyType (ComposeHashable EncryptorType MapCon) ) :
  ThresholdComposeReadsFor OrdKey EncryptorType Plaintext Ciphertext Evidence MapCon EncryptorHashOrdKeyType
  :=
  mkThresholdComposeReadsFor@{
    underlyingReadsFor := r;
    encryptor := ThresholdComposeEncryptorFunctor (ReadsFor.encryptor underlyingReadsFor) map thresholdComposeHash;
    readsFor := \{
      e (mkPair (mkComposeHashable t0 w0) (mkComposeHashable t1 w1)) :=
        OrdMap.all map
          \{ (mkPair w v) :=
              (w * t1) <=
              ((OrdMap.foldl map
                \{ (mkPair (mkPair x v1) s) :=
                    ite (ReadsFor.readsFor underlyingReadsFor e (mkPair v v1)) (x + s) s
                }
                0 w1
              ) * t0)
          }
          w0
    };
  }
```

### "And" Identities

We can compose identities with conjunction: _A_ `&&` _B_ is the identity which requires an agent to
have both _A_'s internal identity and _B_'s internal identity to sign or decrypt. It represents _A_
and _B_ working together. In practice, _A_ `&&` _B_ can be defined as a special case of Threshold
composition (see `verifierAnd` above).

### "Or" Identities

We can compose identities with disjunction as well: _A_ `||` _B_
requires an agent to have either _A_'s internal identity or _B_'s internal identity. It represents
either _A_ or _B_, without specifying which. In practice, _A_ `||` _B_ can be defined as a special
case of Threshold Composition (see `verifierOr` above).

In principle, we could define things differently: Threshold Composition could be defined using `&&`
and `||` as primitives, by building a disjunction of every possible conjunction that satisfies the
threshold. In several important cases, however, this takes much more space to express, so we use the
equally general and more numerically efficient threshold composition abstraction.

### Opaque Composition

A group of agents can also compose an opaque identity such that composition information is not available
to the outside. One example would be using distributed key generation and a threshold
cryptosystem [e.g. Threshold RSA](https://iacr.org/archive/eurocrypt2001/20450151.pdf). Here the
agents compute _one_ RSA keypair together, with only shares of the private key being generated by
each agent. Decryption of messages encrypted to the single public key then requires cooperation of
a subset of agents holding key shares, fulfilling the threshold requirements. This group would have
a single External Identity based on a regular RSA public key, and it would not necessarily be clear
how the identity was composed.

Specific evidence could prove that this threshold cryptosystem identity is `equivalent` to some
 `ThresholdCompose` identity. This kind of proof requires `readsFor` and `signsFor` relations
tailored to the cryptosystem used. Once equivalence is proven, however, one could use the threshold
 cryptosystem identity for efficiency, but reason using the
 `ThresholdCompose` identity.

## Special identities

The following special identities illustrate the generality of our
identity abstractions:

### "true / All"

Anyone can sign and decrypt (`verify` returns true and `encrypt` returns the `Plaintext`). No secret
knowledge is required, so all agents can take on this identity.

The _true_ identity preserves structure under conjunction (_x_ `&&` _true_ `equivalent` _x_) and
forgets structure under disjunction (_x_ `||` _true_ `equivalent` _true_).

### "false / None"

No one can sign or decrypt (`verify` returns false and `encrypt`
 returns empty string). No secret knowledge exists that fulfills these
 requirements, so no agent can take on this identity.

The _false_ identity forgets structure under disjunction
 (_x_ `&&` _false_ `equivalent` _false_) and preserves structure under
 disjunction (_x_ `||` _false_ `equivalent` _x_).

## Identity Names

Sometimes it is useful to have a name for an external identity before the relevant cryptographic
values are available. For example, we might refer to _"a quorum of validators from chain `X` at
epoch `Y`"_. Before epoch `Y` has begun, chain `X` may not have yet decided who constitutes a
quorum.

It would be possible to build a `Verifier`, where the evidence that the signers are in fact a quorum
of validators from chain `X` at epoch `Y` is part of the signature. One might later build a simpler
`Verifier`, which elides this evidence, and then prove that the two `signsSameAs` using the
evidence. However, barring some really exciting cryptography, we'd need to know the quorums from
chain `X` at epoch `Y` before we could make an `Encryptor`.

We therefore introduce a new type, _Identity Name_, which represents a placeholder to be filled in
when an appropriate external identity can be found. Specifically, each type of identity name comes
with a predicate, which can be satisfied by an external identity, and accompanying evidence.
Identity names can also be hashed, like external identities.

Identity names can be described in two structures: one for checking that
 a `VerifierType` corresponds with an `IdentityName`, and one for checking
 that an `EncryptorType` corresponds with an `IdentityName`.
The same name can refer to both a `VerifierType` and an `EncryptorType`.

#### Verifier Name Juvix Type

An `IdentityName` can be mapped to an appropriate `VerifierType`
 when suitable `Evidence` is found.
Here, `checkVerifierName` defines what evidence is acceptable for a
 `VerifierType`.

Note that `IdentityName`s are also hashable: we require a structure
 `verifierNameHash` that details how to hash them.

```juvix
type VerifierName
  (OrdKey VerifierType Signable Commitment Evidence IdentityName VerifierNameHashOrdKeyType) :=
  mkVerifierName {
    verifier : Verifier OrdKey VerifierType Signable Commitment;
    checkVerifierName : IdentityName -> VerifierType -> Evidence -> Bool;
    verifierNameHash : HASH VerifierNameHashOrdKeyType IdentityName
  };
```

#### Encryptor Name Juvix Type

An `IdentityName` can be mapped to an appropriate Encryptor `EncryptorType`
 when suitable `Evidence` is found.
Here, `checkEncryptorName` defines what evidence is acceptable for an
 `Encryptor` `EncryptorType`.
Note that `IdentityName`s are also hashable: we require a structure
 `encryptorNameHash` that details how to hash them.

```juvix
type EncryptorName
  (OrdKey EncryptorType Plaintext Ciphertext Evidence IdentityName EncryptorNameHashOrdKeyType) :=
  mkEncryptorName {
    verifier : Encryptor OrdKey EncryptorType Plaintext Ciphertext;
    checkEncryptorName : IdentityName -> EncryptorType -> Evidence -> Bool;
    encryptorNameHash : HASH EncryptorNameHashOrdKeyType IdentityName
  };
```

For example, for the identity name _"a quorum of validators from chain `X` at epoch `Y`"_, a
satisfying external identity would be composed from the validators selected for epoch `Y`, and the
accompanying evidence would be a light-client proof from chain `X` that these are the correct
validators for epoch `Y`.

Note that multiple identity names can refer to the same external identity, and in principle,
multiple external identities could have the same identity name. Usually, multiple external
identities only have the same identity name when there is Byzantine behaviour, but that is not
explicitly part of the identity abstractions at this layer.

### Sub-Identities

One particularly common case for identity names is when one party (the super-identity) wants to
designate a specific name they use to refer to another identity. Here, the super-identity is acting
like a [certificate authority](https://en.wikipedia.org/wiki/Certificate_authority): they designate
which external identity corresponds with this identity name. This sub-identity is often something
the super-identity controls: a specific machine they own, or a process they run on that machine.
Such a sub-identity might be associated with a string, such as `"acceptor"`, which might designate
the process participating in consensus within a validator. In this case, the predicate should check
that the super-identity has signed a statement declaring that the external identity matches the
sub-identity.

### "." Notation

Because sub-identities using string names are so common, we have a short-cut notation for expressing
identity names. Given some identity _Alice_, for any string `"foo"`, _Alice.foo_ is an identity
name. For example, even before they learn anything about _Alice_, validators might refer to
_Alice.acceptor_ to mean the specific process Alice is running to participate in consensus. The
identity _Alice_ can sign statements to let people know what external identity they should
(immutably) use for _Alice.foo_ or _Alice.acceptor_. These are left associative, so _Alice.foo_ can
designate _Alice.foo.bar_ (shorthand for (_Alice.foo_)_.bar_) and _Alice.foo.bar_ can designate
_Alice.foo.bar.baz_ (shorthand for ((_Alice.foo_)_.bar_)_.baz_), and so on. These are a special case
of sub-identities: _X.Y_ is a sub-identity of _X_.

Formally, we use `mkPair (hash Alice) "foo"` as the Juvix representation of _Alice.foo_:

A specific kind of identity name, wher ethe evidence is a signed
 statement from a specified parent saying that it associates this
 VerifierType with a specific `name`.

Here,

- `Name` is the type the parent identifies with a child.
  For example, for `name = string`, and some identity Alice, we can specify
  `(hash(Alice),"bob")`, or _Alice.bob_, as the identity that
  Alice refers to as `"bob"`.

- `child` : `Verifier` type that can be identified with a name.

- `parent` : `Verifier` type that signs evidence statements.

  Crucially, it must be able to sign tuples of the form
  (string, name, child's hash type)
  In our example, where Alice refers to Bob as Alice.`"bob"`, `child` describes
  Bob, `parent` describes Alice, and `name` describes `"bob"`.

- `hash` Describes what will become the `verifierNameHash`.
  Crucially, it must be able to hash pairs of the form
  (parent's hash type, name)

```juvix
SubVerifierFunctor
  (OrdKey VerifierType Signable Commitment Name ParentOrdKeyType : Type)
  (child : Verifier OrdKey VerifierType Signable Commitment)
  (parent : Verifier ParentOrdKeyType VerifierType (Pair String (Pair Name OrdKey)) Commitment)
  (hash : HASH ParentOrdKeyType (Pair ParentOrdKeyType Name)) :
  VerifierName OrdKey VerifierType Signable Commitment (Pair VerifierType Commitment) (Pair ParentOrdKeyType Name) ParentOrdKeyType :=
  mkVerifierName@{
    verifier := child;
    checkVerifierName := \{
      (mkPair ph n) c (mkPair pv pc) :=
        (Verifier.verify parent pv (mkPair "I identify this verifier with this name : " (mkPair n (HASH.hash (Verifier.verifierHash child) c))) pc) &&
        ((OrdKey.compare (HASH.ordKey (Verifier.verifierHash parent)) ph (HASH.hash (Verifier.verifierHash parent) pv)) == EQ)
    };
    verifierNameHash := hash;
  }
```

In other words, we have a specific, standardized thing an external identity can sign to designate
that another external identity corresponds to a "." name.

Note that we can use "." sub-identities for purposes other than identifying identities that the
super-identity controls. _Alice_ might have a friend _Bob_, and designate his external identity as
_Alice.bob_. This is an example of a place where "sub-identity-ness" is not transitive:
_Alice.bob.carol_ is (_Alice.bob_)_.carol_, a sub-identity of _Alice.bob_, so it is up to _Bob_ to
designate which external identity he associates with `"carol"`, and _Alice_ has no say:
_Alice.bob.carol_ is not a sub-identity of _Alice_.

### Identity Engine

In practice, using Identity Names requires each physical machine to maintain a mapping from identity
names to known external identities. The machine does not have to store the accompanying evidence for
each, although it might be useful to do so sometimes (for example, in order to present to a third
party). When any process on that machine wants to do any operation using an identity name instead of
an external identity, it can query this mapping to see if there is a known external identity to use
for that operation.

An Identity Engine can also store evidence for known `signsFor` and `readsFor` relationships, and
help choose which external identity is most efficient for a task. For example, if an agent wants to
encrypt a message to _"a quorum of validators from chain `X` at epoch `Y`"_, they would first
resolving the identity name to an identity (possibly a Threshold Composed Identity), and might then
ask if there is some known equivalent identity (such as a threshold encryption identity) with
cheaper encryption.

### Identity Name Resolution

There is no general mechanism for finding external identities (and accompanying evidence) for
_arbitrary_ identity names, with arbitrary forms of evidence. However, for some common types of
identity names, such as "." sub-identities, we can establish a standard server and query language,
which participating Identity Engines can query to resolve those identity names.
