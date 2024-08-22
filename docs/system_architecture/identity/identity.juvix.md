---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? note "Juvix imports"

    ```juvix
    module system_architecture.identity;
    import prelude open hiding {Pair};
    import Stdlib.Data.Pair as Pair open using {Pair; ,} public;
    import Stdlib.Data.Nat as Nat open using {Nat; +; *; <=} public;
    import Stdlib.Trait.Eq as Eq open using {==} public;
    import Stdlib.Trait.Ord as Ord open using {Ordering; EQ} public;
    -- import Stdlib.Trait.Foldable.Polymorphic as Foldable.Polymorphic open using {foldl} public;
    ```

# Identity Architecture

```juvix
type Ordkey (ord_key : Type) :=
  mkOrdkey {
      compare : ord_key -> ord_key -> Ordering
  };
```


```juvix
type HASH (ord_key hashable : Type) :=
  mkHASH {
    OrdKey : Ordkey ord_key;
    hash : hashable -> ord_key
  };
```

??? note "ORD MAP"

    ```juvix
    -- Note: instance of this with Data.Map should be made
    type ORD_MAP (map_ord_key : Type) (map_con {- originally "map" -}: Type -> Type) :=
      mkORD_MAP {
        ord_key : Ordkey map_ord_key;
        empty : {a : Type} -> map_con a;
        map  : {a b : Type} -> (a -> b) -> map_con a -> map_con b;
        insert  : {a : Type} -> Pair (map_con a) (Pair map_ord_key a) -> map_con a;
        foldl  : {a b : Type} -> (Pair a b -> b) -> b -> map_con a -> b;
        intersectWith  : {a b c : Type} -> (Pair a b -> c) -> Pair (map_con a) (map_con b) -> map_con c;
        all : {a : Type} -> (a -> Bool) -> map_con a -> Bool
        -- Bunch of stuff, see https://www.smlnj.org/doc/smlnj-lib/Util/sig-ORD_MAP.html
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
 decryption. Formally, an internal identity has 2 parts: a Signer and a
Decryptor.

#### Signer Juvix Type

A signature describing a type `signer` that can cryptographically
 `sign` (or credibly commit) to something (a `signable`), forming a
 `commitment`.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature) keys,
  which should be able to sign anything that can be marshaled into a
  bitstring.

Properties:

- In general, every `S:SIGNER` needs a corresponding `V:VERIFIER`, and
  every `s:S.signer` needs a corresponding `v:V.verifier`, such that:

  - For any message `m`: `verify v m x = (x = (sign s m))`

  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.

```juvix
type SIGNER (signer signable commitment : Type) :=
  mkSIGNER {
    sign : signer -> signable -> commitment
  };
```

#### Decryptor Juvix Type

A signature describing a type `decryptor` that can cryptographically
 `decrypt` something (a `ciphertext`), resulting in a `plaintext`
 (or `N1`, if decryption fails).
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be  unmarshaled from a bitstring.

Properties:

- a computationally bounded adversary should not be able to
  approximate `decrypt d` without knowledge of `d`.

- `decrypt` should take polynomial time (in the size of its inputs)

- Each `D:DECRYPTOR` should have a corresponding `E:ENCRYPTOR`, and
  each `d: D.decryptor` has a corresponding `e: E.encryptor` such
  that:

  - for all `c : D.ciphertext`, `p : D.plaintext`:
    `D.decrypt d c = Some p` iff `c = E.encrypt e p`

  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption"

```juvix
type DECRYPTOR (decryptor plaintext ciphertext : Type) :=
  mkDECRYPTOR {
    decrypt : decryptor -> ciphertext -> Maybe plaintext
  }
```

#### Internal Identity Juvix Type

An Internal Identity structure, then, simply specifies everything specified by
both Signer and Decryptor.

An Internal Identity structure specifies the necessary types and
 functions for both a Signer and a Decryptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) private keys,
 which should be able to decrypt integers into anything that can be
 unmarshaled from a bitstring, and sign anything which can be
 marshaled into a bytestring to form an integer.

An internal_identity includes:

- a type `signer` that can cryptographically
  `sign` (or credibly commit) to something (a `signable`), forming a
  `commitment`.

- a type `decryptor` that can cryptographically `decrypt` something
  (a `ciphertext`), resulting in a `plaintext`
  (or `N1`, if decryption fails).

Properties are inherited from `SIGNER` and `DECRYPTOR`.

```juvix
type INTERNAL_IDENTITY (Signer Signable commitment Decryptor plaintext ciphertext : Type) :=
  mkINTERNAL_IDENTITY {
    signer : SIGNER Signer Signable commitment;
    decryptor : DECRYPTOR Decryptor plaintext ciphertext
  }
```

### External Identity

An external identity includes only public information. An external identity can
verify signatures produced by an internal identity, and encrypt messages the
internal identity can then decrypt. Formally, an external identity has 2 parts:
a Verifier and an Encryptor. Each is _hashable_: any
[structure](https://www.cs.cornell.edu/riccardo/prog-smlnj/notes-011001.pdf#page=59)
specifying Verifier and Encryptor types must also specify a hash function, so
that external identities can be specified by hash.

#### Verifier Juvix Type

A signature describing a type `verifier` that can cryptographically
 `verify` that a `commitment` (or cryptographic signature) corresponds
 to a given message (a `signable`), and was signed by the `signer`
 corresponding to this `verifier`.
A `verifier` can be hashed (producing a unique identifier), so a
 structure with signature `VERIFIER` must specify a `VerifierHash`
 structure defining a suitable `hash` function.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature)
 identities.

Properties:

- In general, every `V:VERIFIER` needs a corresponding `S:SIGNER`, and
  every `s:S.signer` needs a corresponding `v:V.verifier`, such that:

  - For any message `m`: `verify v m x = (x = (sign s m))`

  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.

```juvix
type VERIFIER (ord_key verifier signable commitment : Type) :=
  mkVERIFIER {
    verify : verifier -> signable -> commitment -> Bool;
    VerifierHash : HASH ord_key verifier
  }
```

#### Encryptor SML Signature

A signature describing a type `encryptor` that can cryptographically
 `encrypt` a `plaintext` (message) to create a `ciphertext` readable
 only by the corresponding `decryptor`.
An `encryptor` can be hashed (producing a unique identifier), so a
 structure with signature `ENCRYPTOR` must specify an `EncryptorHash`
 structure defining a suitable hash function.
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be  unmarshaled from a bitstring.

Properties:


- `encrypt` should take polynomial time (in the size of its inputs)

- Each `E:ENCRYPTOR` should have a corresponding `D:DECRYPTOR`, and
  each `d: D.decryptor` has a corresponding `e: E.encryptor` such
  that:

  - for all `c : D.ciphertext`, `p : D.plaintext`:
    `D.decrypt d c = Some p` iff `c = E.encrypt e p`

  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption."
    In an asymmetric cryptosystem, a computationally bounded adversary
    should not be able to approximate `d` knowing only `e`.

```juvix
type ENCRYPTOR (ord_key encryptor plaintext ciphertext : Type) :=
  mkENCRYPTOR {
    encrypt : encryptor -> plaintext -> ciphertext;
    EncryptorHash : HASH ord_key encryptor
  }
```

#### External Identity Juvix Type

An External Identity structure specifies the necessary types and
 functions for both a Verifier and an Encyrptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) public keys.

An external_identity includes:

- a type `verifier` that can cryptographically `verify` that a
  `commitment` (or cryptographic signature) corresponds to a given
  message (a `signable`), and was signed by the `signer`
  corresponding to this `verifier`.

- a type `encryptor` that can cryptographically `encrypt` a
  `plaintext` (message) to create a `ciphertext` readable only by the
  corresponding `decryptor`.

Properties are inherited from `VERIFIER` and `ENCRYPTOR`.

```juvix
type EXTERNAL_IDENTITY (
    verifier_ord_key verifier signable commitment
    encryptor_ord_key encryptor plaintext ciphertext : Type) :=
  mkEXTERNAL_IDENTITY {
    Verifier : VERIFIER verifier_ord_key verifier signable commitment;
    Encryptor : ENCRYPTOR encryptor_ord_key encryptor plaintext ciphertext
  };
```

### Identity Juvix Type

An Identity structure, formally, specifies all the types for
 corresponding internal and external identities.
So, for a given Identity structure `I`, `I.verifier` should be the
 type of objects that can verify `commitment`s produced by a
 corresponding object of type `I.signer`.
Likewise, `I.decryptor` should be the type of objects that can decrypt
 `ciphertext`s produced by a corresponding object of type
 `I.encryptor`.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
 public / private keys sytems.

An Identity includes:


- a type `signer` that can cryptographically `sign` (or credibly commit) to something (a `signable`), forming a `commitment`.

- a type `decryptor` that can cryptographically `decrypt` something (a `ciphertext`), resulting in a `plaintext` (or `N1`, if decryption fails).

- a type `verifier` that can cryptographically `verify` that a `commitment` (or cryptographic signature) corresponds to a given message (a `signable`), and was signed by the `signer` corresponding to this `verifier`.

- a type `encryptor` that can cryptographically `encrypt` a `plaintext` (message) to create a `ciphertext` readable only by the corresponding `decryptor`.

Properties are inherited from `VERIFIER`, `ENCRYPTOR`, `SIGNER`, and `DECRYPTOR`.

```juvix
type IDENTITY (
  signer
  internal_signable
  internal_commitment
  decryptor
  internal_plaintext
  internal_ciphertext
  verifier_ord_key
  verifier
  external_signable
  external_commitment
  encryptor_ord_key
  encryptor
  external_plaintext
  external_ciphertext
  : Type) :=
  mkIDENTITY {
    internalIdentity : INTERNAL_IDENTITY signer internal_signable internal_commitment decryptor internal_plaintext internal_ciphertext;
    externalIdentity : EXTERNAL_IDENTITY verifier_ord_key verifier external_signable external_commitment encryptor_ord_key encryptor external_plaintext external_ciphertext
  };
```

## SignsFor Relation

Some identities may have the authority to sign statements on behalf of other
 identities. For example, _Alice_ might grant _Bob_ the authority to sign
arbitrary messages on her behalf. We write this relationship as _Bob_ `signsFor`
 _Alice_.

In general, `signsFor` is a partial order over identitites. This means
`signsFor` is transitive: if _A_ `signsFor` _B_ and _B_ `signsFor` _C_, then _A_
 `signsFor` _C_. The `signsFor` relation becomes especially useful with regard
to [composed identities, discussed below](#composition).

### SignsFor Evidence

We do not specify all the ways 1 might know if 1 identity `signsFor`
another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As 1 simple form of
evidence, we can specify a format for signed statements from _B_ that proves
some specified _A_ `signsFor` _B_.

Note that `signsFor` evidence cannot be revoked, and so a `signsFor` relation is
not _stateful_: it cannot depend on the current state of, for example, a
blockchain.

#### SignsFor Juvix Type

Formally, a `signsFor` relation requires a type of evidence, and a
 `VERIFIER` structure.
This codifies a belief about what `verifier`'s `commitments` are
 "at least as good as" another `verifier`'s.
Evidence can be signed statements, proofs, or even local state about beliefs.

For example, suppose `Alice` wants to grant authority to `Bob` to
 `sign` on her behalf.
Nodes who want to take this into account might accept some sort of
 `e:evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `signsFor e (Bob, Alice)`.

Note that `signsFor` is not symmetric: `signsFor e (x,y)` does not
 imply that any `z` exists such that `signsFor z (y,x)`.

```juvix
type SIGNS_FOR (ord_key verifier signable commitment evidence : Type) :=
  mkSIGNS_FOR {
    Verifier : VERIFIER ord_key verifier signable commitment;
    signsFor : evidence -> (Pair verifier verifier) -> Bool
  };
```

### SignsFor Equivalence

We can also define a kind of identity _equivalence_: _A_ `signsSameAs` _B_
 precisely when _A_ `signsFor` _B_ and _B_ `signsFor` _A_. This means that (in
 general), if you want to sign a message as _A_, but for whatever reason it's
cheaper to sign a message as _B_, it's safe to just use _B_ instead, and vice
 versa.

## ReadsFor Relation

Similar to `signsFor`, it is useful to sometimes note that 1 identity can read
 information encrypted to another identity. For example, suppose _Alice_ gives
her private `decryptor` to _Bob_, and wants to let every1 know that _Bob_ can
 now read anything encrypted to _Alice_. Nodes who want to take this into
 account might accept some sort of `evidence`, perhaps a signed statement from
_Alice_, so that they can recognize that _Bob_ `readsFor` _Alice_.

Like `signsFor`, `readsFor` is a partial order over identitites. This means
`readsFor` is transitive: if _A_ `readsFor` _B_ and _B_ `readsFor` _C_, then _A_
 `readsFor` _C_. The `readsFor` relation becomes especially useful with regard
to [composed identities, discussed below](#composition).

### ReadsFor Evidence

We do not specify all the ways 1 might know if 1 identity `readsFor`
 another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As 1 simple form of
 evidence, we can specify a format for signed statements from _B_ that proves
_A_ `readsFor` _B_.

#### ReadsFor Juvix Type

Formally, a `readsFor` relation requires a type of evidence, and an
 `ENCRYPTOR` structure.
This codifies a belief about what `DECRYPTOR`s can read other
 `ENCRYPTOR`s ciphertext.
Evidence can be signed statements, proofs, or even local state about beliefs.

Specifically, if a node expresses a `readsFor` relation, and
 `readsFor e (x,y)`, then the node believes that any node knowing the
 decryptor corresponding to `x` can decrypt `encrypt y p`.
If there is some plaintext `p` such that some node knowing a decryptor
 corresponding to `x` cannot read `encrypt y p`, then the node's
 beliefs, as encoded in the `readsFor` relation, are incorrect.

For example, suppose `Alice` gives her private `decryptor` to `Bob`,
 and wants to let every1 know that `Bob` can now read anything
 encrypted to `Alice`.
Nodes who want to take this into account might accept some sort of
 `e:evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `readsFor e (Bob, Alice)`.

Note that `readsFor` is not symmetric: `readsFor e (x,y)` does not
 imply that any `z` exists such that `readsFor z (y,x)`.

```juvix
type READS_FOR (ord_key encryptor plaintext ciphertext evidence : Type) :=
  mkREADS_FOR {
    Encryptor : ENCRYPTOR ord_key encryptor plaintext ciphertext;
    readsFor : evidence -> (Pair encryptor encryptor) -> Bool
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

#### Threshold Composition Juvix Type (Signer and Verifier)

A `ThresholdCompose` `verifier` consists of a
 threshold (`int`), and a set of `verifier`s, each paired with a
 weight (`int`).
 (this set is encoded as a `Map.map` from hashes of `verifiers` to
  `int * verifier` pairs).
`commitments` are simply `Map`s from hashes of the underlying
 identities to `commitments` signed by that identitity.
A `commitment` verifies iff the set of valid commitments included
 correspond to a set of `verifiers` whose weights sum to at least
 the threshold.
Note that this satisfies both signatures `VERIFIER` and `SIGNER`.

In general, `ThresholdCompose` `signer`s and `verifier`s may not be
 used much directly.
Instead, nodes can make more efficient identities (using cryptographic
 siganture aggregation techniques), and express their relationship to
 `ThresholdCompose` `verifier`s as a `SIGNS_FOR` relationship.
This will let nodes reason about identities using simple
 `ThresholdCompose` `verifier`s, while actually using more efficient
 implementations.

Formally, to specify a `ThresholdCompose`, we need:

- `Verifier`, the structure of the underlying `verifiers`.

- `Signer`, the corresponding structure of the underlying `signers`.

- `Map : ORD_MAP`, to be used to encode weights and `commitment`s.
  (Note that this needs `Map.Key` to be the hash type of the
   underlying `Verifier`)

- `ThresholdComposeHash`, which specifies a `hash` function that can
   hash our composed `verifier`s (type
   `{threshold:int, weights : ((int * Verifier.verifier) Map.map)}`).

A `ThresholdCompose` structure provides:

- `structure Map : ORD_MAP` the underlying `ORD_MAP` used in
   `verifier` and `commitment`

- `structure UnderlyingVerifier : VERIFIER` the structure describing
   the types of the underlying `verifier`s which can be composed.

- `structure UnderlyingSigner : SIGNER` the structure describing
   the types of the underlying `signer`s which can be composed.

- `structure VerifierHash : HASH` describes the hash function for
   hashing these composed `verifiers`

- `type signer` is the type of composed signers.
   These are just `UnderlyingSigner.signer Map.map`, meaning each is
   stored under the hash of the corresponding
   `UnderlyingVerifier.verifier`.
   `signer` does not need to encode weights or threshold.

- `type verifier` the type of composed verifiers. These are
   `{threshold:int, weights : ((int * UnderlyingVerifier.verifier) Map.map)}`

- `type signable` the type of message that can be signed. This is
   exactly the same as what the underlying verifiers can sign
   (`UnderlyingVerifier.signable`).

- `type commitment` describes composed signatures, these are a
   `Map.map` from hashes of underlying verifiers
   (`UnderlyingVerifier.VerifierHash.OrdKey.ord_key`) to signatures
   (`UnderlyingVerifier.commitment`)

- `fun sign` creates a `commitment` using all
   `UnderlyingSigner.signer`s in the composed `signer`.

- `fun verify` returns true iff the set of valid commitments included
   correspond to a set of `UnderlyingVerifier.verifier`s whose weights
   sum to at least the threshold.

- `fun signerCompose` is constructs a composed `signer` from a list of
   `UnderlyingVerifier.verifier * UnderlyingSigner.signer` pairs.
   Note that each `signer` must be paired with its correct `verifier`,
    or the composed `signer` will not produce verifiable
    `commitment`s.

- `fun verifierCompose` is useful for constructing the composition of
   a list of verifiers.
  Returns a composed `verifier`.
  Its arguments are:

  - the threshold (`int`)

  - a `list` of weight (`int`), `UnderlyingVerifier.verifier` pairs.

- `fun verifierAnd` creates a composed `verifier` that is the "&&" of
   2 input verifiers: a `signer` must encode the information of the
   signers for *both* `x` and `y` to sign statements `verifierAnd x y`
   will verify.

- `fun verifierOr` creates a composed `verifier` that is the "||" of
   2 input verifiers: a `signer` must encode the information of the
   signers for *either* `x` or `y` to sign statements `verifierOr x y`
   will verify.

```juvix
type Compose_hashable (verifier : Type) (map_con : Type -> Type) :=
  mkCompose_hashable {
    threshold : Nat;
    weights : map_con (Pair Nat verifier)
  };

type ThresholdCompose
  ( ord_key : Type ) ( map_con : Type -> Type )
  ( verifier signable commitment signer VerifierHash_ord_key : Type)
   :=
  mkThresholdCompose {
    Map : ORD_MAP ord_key map_con;
    UnderlyingVerifier : VERIFIER ord_key verifier signable commitment;
    UnderlyingSigner : SIGNER signer signable commitment;
    VerifierHash : HASH VerifierHash_ord_key (Compose_hashable verifier map_con);

    sign : map_con signer -> signable -> map_con commitment;
    verify : (Compose_hashable verifier map_con) -> signable -> map_con commitment -> Bool;
    signerCompose : List (Pair verifier signer) -> map_con signer;
    verifierCompose : Nat -> List (Pair Nat verifier) -> (Compose_hashable verifier map_con);
    verifierAnd : verifier -> verifier -> (Compose_hashable verifier map_con);
    verifierOr : verifier -> verifier -> (Compose_hashable verifier map_con);
  };

projectVERIFIER
  { map_con : Type -> Type }
  { ord_key verifier signable commitment signer VerifierHash_ord_key : Type }
  ( tc : ThresholdCompose ord_key map_con verifier signable commitment signer VerifierHash_ord_key ) :
  VERIFIER VerifierHash_ord_key (Compose_hashable verifier map_con) signable (map_con commitment) :=
  mkVERIFIER@{
    verify := ThresholdCompose.verify tc;
    VerifierHash := ThresholdCompose.VerifierHash tc;
  };

ThresholdComposeFunctor
  { map_con : Type -> Type }
  { ord_key verifier signable commitment signer VerifierHash_ord_key : Type }
  (Verifier : VERIFIER ord_key verifier signable commitment)
  (Signer : SIGNER signer signable commitment)
  (Map_In : ORD_MAP ord_key map_con)
  (ThresholdComposeHash : HASH VerifierHash_ord_key (Compose_hashable verifier map_con)) :
  ThresholdCompose
    ord_key map_con
    verifier signable commitment
    signer
    VerifierHash_ord_key
   :=
  mkThresholdCompose@{
    Map := Map_In;
    UnderlyingVerifier := Verifier;
    UnderlyingSigner := Signer;
    VerifierHash := ThresholdComposeHash;
    sign := \ {s m := ORD_MAP.map Map \ { i := SIGNER.sign UnderlyingSigner i m } s};
    verify := \ {
      | (mkCompose_hashable t ws) s c := (
          t <= (
            ORD_MAP.foldl Map \{(x, y) := x + y} 0 (
              ORD_MAP.intersectWith Map (
                \{ | ((w, v), x) :=
                      ite (VERIFIER.verify UnderlyingVerifier v s x) w 0
                }
            ) (ws, c)))
      )
    };

    signerCompose := \{ l :=
        foldl
        \{ m (v, s) :=
          ORD_MAP.insert Map (m, ((
            HASH.hash (VERIFIER.VerifierHash UnderlyingVerifier) v
          ), s))
        }
        (ORD_MAP.empty Map) l
    };

    verifierCompose := \{
      threshold weights :=
        (mkCompose_hashable threshold
          (foldl
            \ { m (w, v) :=
              ORD_MAP.insert Map (m, ((
                HASH.hash (VERIFIER.VerifierHash UnderlyingVerifier) v
              ), (w, v)))
            }
            (ORD_MAP.empty Map) weights
        ))
    };

    verifierAnd := \{ x y := verifierCompose 2 [(1, x); (1, y)]};
    verifierOr := \{ x y := verifierCompose 1 [(1, x); (1, y)] };
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
  `ThresholdCompose` `verifier`s
 _x_ `signsFor` _y_ if every underlying verifier in _x_ has no more
  weight (divided by threshold) as verifiers it `signsFor` in y.
This implies that anything which can sign as _x_ can also sign
 as _y_.

This requires an underlying `S:SIGNS_FOR` for comparing the weighted
 signers in _x_ and _y_, which in turn may require evidence.
No additional evidence is required.

Other parameters necessary to define the `ThresholdCompose`
 `verifiers` include:

- `Signer`, the corresponding structure of the underlying `signers`.

- `Map : ORD_MAP`, to be used to encode weights and `commitment`s.
  (Note that this needs `Map.Key` to be the hash type of the
   underlying `S.Verifier`)

- `ThresholdComposeHash`, which specifies a `hash` function that can
   hash our composed `verifier`s (type
   `{threshold:int, weights : ((int * S.Verifier.verifier) Map.map)}`).

```juvix
type ThresholdComposeSignsFor
  ( ord_key verifier signable commitment evidence : Type )
  ( map_con : Type -> Type )
  ( VerifierHash_ord_key )
   :=
  mkThresholdComposeSignsFor {
    UnderlyingSignsFor : SIGNS_FOR ord_key verifier signable commitment evidence;
    Verifier : ThresholdCompose ord_key map_con verifier signable commitment verifier VerifierHash_ord_key;
    signsFor : evidence -> Pair (Compose_hashable verifier map_con) (Compose_hashable verifier map_con) -> Bool;
  };

projectSIGNS_FOR
  { ord_key verifier signable commitment evidence : Type }
  { map_con : Type -> Type }
  { VerifierHash_ord_key : Type }
  ( tc : ThresholdComposeSignsFor ord_key verifier signable commitment evidence map_con VerifierHash_ord_key ) :
  SIGNS_FOR VerifierHash_ord_key (Compose_hashable verifier map_con) signable (map_con commitment) evidence :=
  mkSIGNS_FOR@{
    Verifier := projectVERIFIER (ThresholdComposeSignsFor.Verifier tc);
    signsFor := ThresholdComposeSignsFor.signsFor tc;
  };

ThresholdComposeSignsForFunctor
  { ord_key verifier signable commitment evidence : Type }
  { map_con : Type -> Type }
  { VerifierHash_ord_key : Type }
  ( S : SIGNS_FOR ord_key verifier signable commitment evidence )
  ( Signer : SIGNER verifier signable commitment)
  ( Map : ORD_MAP ord_key map_con )
  ( ThresholdComposeHash : HASH VerifierHash_ord_key (Compose_hashable verifier map_con) ) :
  ThresholdComposeSignsFor ord_key verifier signable commitment evidence map_con VerifierHash_ord_key
  :=
  mkThresholdComposeSignsFor@{
    UnderlyingSignsFor := S;
    Verifier := ThresholdComposeFunctor (SIGNS_FOR.Verifier UnderlyingSignsFor) Signer Map ThresholdComposeHash;
    signsFor := \{
      e ((mkCompose_hashable t0 w0), (mkCompose_hashable t1 w1)) :=
        ORD_MAP.all Map
          \{ (w, v) :=
              (w * t1) <=
              ((ORD_MAP.foldl Map
                \{ ((x, v1), s) :=
                    ite (SIGNS_FOR.signsFor UnderlyingSignsFor e (v, v1)) (x + s) s
                }
                0 w1
                ) * t0)
          }
          w0
    };
  };
```

#### `readsFor` Threshold Composition

Like any identity, ThresholdCompositionIdentities can have arbitrary
 `readsFor` relationships.
However, some cases should always hold: _A_ `readsFor` _B_ if every
 identity in _A_ has no more weight (divided by threshold) than
 identities it `readsFor` in _B_.
This implies that any collection of identities that can read messages
 encrypted with _A_ can also read messages encrypted as _B_.

 A `readsFor` relation for easy comparison of
  `ThresholdComposeEncryptor.encryptor`s
 _x_ `readsFor` _y_ if every underlying encryptor in _x_ has no more
  weight (divided by threshold) as encryptors it `readsFor` in y.
This implies that anything which can decrypt as _x_ can also decrypt
 as _y_.

This requires an underlying `R:READS_FOR` for comparing the weighted
 encryptors in  _x_ and _y_, which in turn may require evidence.
No additional evidence is required.

!!! ThresholdComposeEncryptor isn't implemented

```juvix
axiom encrypt_DUMMY :
  {encryptor plaintext ciphertext : Type} -> {map_con : Type -> Type} ->
  (Compose_hashable encryptor map_con) -> plaintext -> ciphertext;
```

```juvix
type ThresholdComposeEncryptor
  (ord_key encryptor plaintext ciphertext : Type)
  (map_con : Type -> Type)
  (EncryptorHash_ord_key : Type)
  :=
  mkThresholdComposeEncryptor {
    Map : ORD_MAP ord_key map_con;
    UnderlyingEncryptor : ENCRYPTOR ord_key encryptor plaintext ciphertext;
    EncryptorHash : HASH EncryptorHash_ord_key (Compose_hashable encryptor map_con);
    compose : Nat -> List (Pair Nat encryptor) -> Compose_hashable encryptor map_con;
    encrypt : (Compose_hashable encryptor map_con) -> plaintext -> ciphertext;
  };
```

```juvix
projectENCRYPTOR
  {ord_key encryptor plaintext ciphertext : Type}
  {map_con : Type -> Type}
  {EncryptorHash_ord_key : Type}
  (tc : ThresholdComposeEncryptor ord_key encryptor plaintext ciphertext map_con EncryptorHash_ord_key) :
  ENCRYPTOR EncryptorHash_ord_key (Compose_hashable encryptor map_con) plaintext ciphertext
  :=
  mkENCRYPTOR@{
    encrypt := ThresholdComposeEncryptor.encrypt tc;
    EncryptorHash := ThresholdComposeEncryptor.EncryptorHash tc;
  };
```

```juvix
ThresholdComposeEncryptorFunctor
  {ord_key encryptor plaintext ciphertext : Type}
  {map_con : Type -> Type}
  {EncryptorHash_ord_key : Type}
  (Encryptor : ENCRYPTOR ord_key encryptor plaintext ciphertext)
  (Map_In : ORD_MAP ord_key map_con)
  (ThresholdComposeHash : HASH EncryptorHash_ord_key (Compose_hashable encryptor map_con)) :
  ThresholdComposeEncryptor ord_key encryptor plaintext ciphertext map_con EncryptorHash_ord_key
  := mkThresholdComposeEncryptor@{
    Map := Map_In;
    UnderlyingEncryptor := Encryptor;
    EncryptorHash := ThresholdComposeHash;
    compose := \{
      t w :=
        mkCompose_hashable@{
          threshold := t;
          weights :=
            foldl
              \{m (w, e) :=
                ORD_MAP.insert Map (m, ((HASH.hash (ENCRYPTOR.EncryptorHash UnderlyingEncryptor) e), (w, e)))
              }
              (ORD_MAP.empty Map) w
        }
    };
    encrypt := encrypt_DUMMY;
  };
```

```juvix
type ThresholdComposeReadsFor
  ( ord_key encryptor plaintext ciphertext evidence : Type )
  ( map_con : Type -> Type )
  ( EncryptorHash_ord_key : Type )
   :=
  mkThresholdComposeReadsFor {
    UnderlyingReadsFor : READS_FOR ord_key encryptor plaintext ciphertext evidence;
    Encryptor : ThresholdComposeEncryptor ord_key encryptor plaintext ciphertext map_con EncryptorHash_ord_key;
    readsFor : evidence -> Pair (Compose_hashable encryptor map_con) (Compose_hashable encryptor map_con) -> Bool;
  };
```

```juvix
projectREADS_FOR
  { ord_key verifier signable commitment evidence : Type }
  { map_con : Type -> Type }
  { EncryptorHash_ord_key : Type }
  ( tc : ThresholdComposeReadsFor ord_key verifier signable commitment evidence map_con EncryptorHash_ord_key ) :
  READS_FOR EncryptorHash_ord_key (Compose_hashable verifier map_con) signable commitment evidence :=
  mkREADS_FOR@{
    Encryptor := projectENCRYPTOR (ThresholdComposeReadsFor.Encryptor tc);
    readsFor := ThresholdComposeReadsFor.readsFor tc;
  };
```

```juvix
ThresholdComposeReadsForFunctor
  { ord_key encryptor plaintext ciphertext evidence : Type }
  { map_con : Type -> Type }
  { EncryptorHash_ord_key : Type }
  ( R : READS_FOR ord_key encryptor plaintext ciphertext evidence )
  ( Map : ORD_MAP ord_key map_con )
  ( ThresholdComposeHash : HASH EncryptorHash_ord_key (Compose_hashable encryptor map_con) ) :
  ThresholdComposeReadsFor ord_key encryptor plaintext ciphertext evidence map_con EncryptorHash_ord_key
  :=
  mkThresholdComposeReadsFor@{
    UnderlyingReadsFor := R;
    Encryptor := ThresholdComposeEncryptorFunctor (READS_FOR.Encryptor UnderlyingReadsFor) Map ThresholdComposeHash;
    readsFor := \{
      e ((mkCompose_hashable t0 w0), (mkCompose_hashable t1 w1)) :=
        ORD_MAP.all Map
          \{ (w, v) :=
              (w * t1) <=
              ((ORD_MAP.foldl Map
                \{ ((x, v1), s) :=
                    ite (READS_FOR.readsFor UnderlyingReadsFor e (v, v1)) (x + s) s
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
threshold.

However, this takes much more space to express, so we use the
equally general and more numerically efficient threshold composition abstraction.

### Opaque Composition

A group of agents can also compose an opaque identity, s.t. composition information is not available
to the outside. 1 example would be a using distributed key generation and a threshold
cryptosystem [e.g. Threshold RSA](https://iacr.org/archive/eurocrypt2001/20450151.pdf). Here the
agents compute _1_ RSA keypair together, with only shares of the private key being generated by
each agent. Decryption of messages encrypted to the single public key then requires cooperation of
a subset of agents holding key shares, fulfilling the threshold requirements. This group would have
a single External Identity based on a regular RSA public key, and it would not necessarily be clear
how the identity was composed.

Specific evidence could prove that this threshold cryptosystem identity is `equivalent` to some
 `ThresholdCompose` identity. This kind of proof requires `readsFor` and `signsFor` relations
tailored to the cryptosystem used. Once equivalence is proven, however, 1 could use the threshold
 cryptosystem identity for efficiency, but reason using the
 `ThresholdCompose` identity.

## Special identities

The following special identities illustrate the generality of our
identity abstractions:

### "True / All"

Any1 can sign and decrypt (`verify` returns true and `encrypt` returns the plaintext). No secret
knowledge is required, so all agents can take on this identity.

The _true_ identity preserves structure under conjunction (_x_ `&&` _true_ `equivalent` _x_) and
forgets structure under disjunction (_x_ `||` _true_ `equivalent` _true_).

### "False / N1"

No 1 can sign or decrypt (`verify` returns false and `encrypt`
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
of validators from chain `X` at epoch `Y` is part of the signature. 1 might later build a simpler
`Verifier`, which elides this evidence, and then prove that the 2 `signsSameAs` using the
evidence. However, barring some really exciting cryptography, we'd need to know the quorums from
chain `X` at epoch `Y` before we could make an `Encryptor`.

We therefore introduce a new type, _Identity Name_, which represents a placeholder to be filled in
when an appropriate external identity can be found. Specifically, each type of identity name comes
with a predicate, which can be satisfied by an external identity, and accompanying evidence.
Identity names can also be hashed, like external identities.

Identity names can be described in 2 structures: 1 for checking that
 a `verifier` corresponds with an `identityName`, and 1 for checking
 that an `encryptor` corresponds with an `identityName`.
The same name can refer to both a `verifier` and an `encryptor`.

#### Verifier Name Juvix Type

An `identityName` can be mapped to an appropriate `Verifier.verifier`
 when suitable `evidence` is found.
Here, `checkVerifierName` defines what evidence is acceptable for a
 `Verifier.verifier`.

Note that `identityName`s are also hashable: we require a structure
 `VerifierNameHash` that details how to hash them.

```juvix
type VERIFIER_NAME
  (ord_key verifier signable commitment evidence identityName VerifierNameHash_ord_key) :=
  mkVERIFIER_NAME {
    Verifier : VERIFIER ord_key verifier signable commitment;
    checkVerifierName : identityName -> verifier -> evidence -> Bool;
    VerifierNameHash : HASH VerifierNameHash_ord_key identityName
  };
```

#### Encryptor Name Juvix Type

An `identityName` can be mapped to an appropriate `Encryptor.encryptor`
 when suitable `evidence` is found.
Here, `checkEncryptorName` defines what evidence is acceptable for a
 `Encryptor.encryptor`.
Note that `identityName`s are also hashable: we require a structure
 `EncryptorNameHash` that details how to hash them.

```juvix
type ENCRYPTOR_NAME
  (ord_key encryptor plaintext ciphertext evidence identityName EncryptorNameHash_ord_key) :=
  mkENCRYPTOR_NAME {
    Verifier : ENCRYPTOR ord_key encryptor plaintext ciphertext;
    checkEncryptorName : identityName -> encryptor -> evidence -> Bool;
    EncryptorNameHash : HASH EncryptorNameHash_ord_key identityName
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

1 particularly common case for identity names is when 1 party (the super-identity) wants to
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

Formally, we use `(hash(Alice), "foo")` as the SML representation of _Alice.foo_:

A specific kind of identity name, wher ethe evidence is a signed
 statement from a specified parent saying that it associates this
 verifier with a specific `name`.

Here,

- `name` is the type the parent identifies with a child.
  For example, for `name = string`, and some identity Alice, we can specify
  `(hash(Alice),"bob")`, or _Alice.bob_, as the identity that
  Alice refers to as `"bob"`.

- `Child` : `VERIFIER` type that can be identified with a name.

- `Parent` : `VERIFIER` type that signs evidence statements.

  Crucially, it must be able to sign tuples of the form
  (string, name, Child's hash type)
  In our example, where Alice refers to Bob as Alice.`"bob"`, `Child` describes
  Bob, `Parent` describes Alice, and `name` describes `"bob"`.

- `Hash` Describes what will become the `VerifierNameHash`.
  Crucially, it must be able to hash pairs of the form
  (Parent's hash type, name)

```juvix
SubVerifierFunctor
  (ord_key verifier signable commitment evidence name parent_ord_key : Type)
  (Child : VERIFIER ord_key verifier signable commitment)
  (Parent : VERIFIER parent_ord_key verifier (Pair String (Pair name ord_key)) commitment)
  (Hash : HASH parent_ord_key (Pair parent_ord_key name)):
  VERIFIER_NAME ord_key verifier signable commitment (Pair verifier commitment) (Pair parent_ord_key name) parent_ord_key :=
  mkVERIFIER_NAME@{
    Verifier := Child;
    checkVerifierName := \{
      (ph, n) c (pv, pc) :=
        (VERIFIER.verify Parent pv ("I identify this Verifier with this name: ", (n, (HASH.hash (VERIFIER.VerifierHash Child) c))) pc) &&
        ((Ordkey.compare (HASH.OrdKey (VERIFIER.VerifierHash Parent)) ph (HASH.hash (VERIFIER.VerifierHash Parent) pv)) == EQ)
    };
    VerifierNameHash := Hash;
  }
```

In other words, we have a specific, standardized thing an external identity can sign to designate
that another external identity corresponds to a "." name.

Note that we can use "." sub-identities for purposes other than identifying identities that the
super-identity controls. _Alice_ might have a friend _Bob_, and designate his external identity as
_Alice.bob_. This is an example a place where "sub-identity-ness" is not transitive:
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