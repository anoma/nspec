---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Identity Architecture

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
Decryptor. We specify both using [SML
signatures](https://www.cs.cornell.edu/riccardo/prog-smlnj/notes-011001.pdf#page=64).

#### Signer SML Signature

--8<-- "./formal/SML/src/signer.sig:signer_description"

```sml
--8<-- "./formal/SML/src/signer.sig:signer"
```

#### Decryptor SML Signature

--8<-- "./formal/SML/src/decryptor.sig:decryptor_description"

```sml
--8<-- "./formal/SML/src/decryptor.sig:decryptor"

```

#### Internal Identity SML Signature

An Internal Identity structure, then, simply specifies everything specified by
both Signer and Decryptor.

--8<-- "./formal/SML/src/internal_identity.sig:internal_identity_description"

```sml
--8<-- "./formal/SML/src/internal_identity.sig:internal_identity"
```

### External Identity

An external identity includes only public information. An external identity can
verify signatures produced by an internal identity, and encrypt messages the
internal identity can then decrypt. Formally, an external identity has 2 parts:
a Verifier and an Encryptor. Each is _hashable_: any
[structure](https://www.cs.cornell.edu/riccardo/prog-smlnj/notes-011001.pdf#page=59)
specifying Verifier and Encryptor types must also specify a hash function, so
that external identities can be specified by hash.

#### Verifier SML Signature

--8<-- "./formal/SML/src/verifier.sig:verifier_description"

```sml
--8<-- "./formal/SML/src/verifier.sig:verifier"

```

#### Encryptor SML Signature

--8<-- "./formal/SML/src/encryptor.sig:encryptor_description"

```sml
--8<-- "./formal/SML/src/encryptor.sig:encryptor"
```

#### External Identity SML Signature

 An external identity, then, simply specifies everything specified by
 both Verifier and Encryptor.

--8<-- "./formal/SML/src/external_identity.sig:external_identity_description"

```sml
--8<-- "./formal/SML/src/external_identity.sig:external_identity"

```

### Identity SML Signature

--8<-- "./formal/SML/src/identity.sig:identity_description"

```sml
--8<-- "./formal/SML/src/identity.sig:identity"
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

We do not specify all the ways one might know if one identity `signsFor`
another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As one simple form of
evidence, we can specify a format for signed statements from _B_ that proves
some specified _A_ `signsFor` _B_.

Note that `signsFor` evidence cannot be revoked, and so a `signsFor` relation is
not _stateful_: it cannot depend on the current state of, for example, a
blockchain.

#### SignsFor SML Signature

--8<-- "./formal/SML/src/signs_for.sig:signs_for_description"

```sml
--8<-- "./formal/SML/src/signs_for.sig:signs_for"

```

### SignsFor Equivalence

We can also define a kind of identity _equivalence_: _A_ `signsSameAs` _B_
 precisely when _A_ `signsFor` _B_ and _B_ `signsFor` _A_. This means that (in
 general), if you want to sign a message as _A_, but for whatever reason it's
cheaper to sign a message as _B_, it's safe to just use _B_ instead, and vice
 versa.

## ReadsFor Relation

Similar to `signsFor`, it is useful to sometimes note that one identity can read
 information encrypted to another identity. For example, suppose _Alice_ gives
her private `decryptor` to _Bob_, and wants to let everyone know that _Bob_ can
 now read anything encrypted to _Alice_. Nodes who want to take this into
 account might accept some sort of `evidence`, perhaps a signed statement from
_Alice_, so that they can recognize that _Bob_ `readsFor` _Alice_.

Like `signsFor`, `readsFor` is a partial order over identitites. This means
`readsFor` is transitive: if _A_ `readsFor` _B_ and _B_ `readsFor` _C_, then _A_
 `readsFor` _C_. The `readsFor` relation becomes especially useful with regard
to [composed identities, discussed below](#composition).

### ReadsFor Evidence

We do not specify all the ways one might know if one identity `readsFor`
 another. In general, an [Identity Engine](#identity-engine) might accept (and
perhaps store) a variety of forms of evidence as proof. As one simple form of
 evidence, we can specify a format for signed statements from _B_ that proves
_A_ `readsFor` _B_.

#### ReadsFor SML Signature

--8<-- "./formal/SML/src/reads_for.sig:reads_for_description"

```sml
--8<-- "./formal/SML/src/reads_for.sig:reads_for"
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

#### Threshold Composition SML Signature (Signer and Verifier)

--8<-- "./formal/SML/src/threshold_compose.fun:threshold_compose_description"

```sml
--8<-- "./formal/SML/src/threshold_compose.fun:threshold_compose"

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

```sml
--8<-- "./formal/SML/src/threshold_compose_signs_for.fun:threshold_compose_signs_for"
```

#### `readsFor` Threshold Composition

Like any identity, ThresholdCompositionIdentities can have arbitrary
 `readsFor` relationships.
However, some cases should always hold: _A_ `readsFor` _B_ if every
 identity in _A_ has no more weight (divided by threshold) than
 identities it `readsFor` in _B_.
This implies that any collection of identities that can read messages
 encrypted with _A_ can also read messages encrypted as _B_.

```sml
--8<-- "./formal/SML/src/threshold_compose_reads_for.fun:threshold_compose_reads_for"
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

A group of agents can also compose an opaque identity, s.t. composition information is not available
to the outside. One example would be a using distributed key generation and a threshold
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

### "True / All"

Anyone can sign and decrypt (`verify` returns true and `encrypt` returns the plaintext). No secret
knowledge is required, so all agents can take on this identity.

The _true_ identity preserves structure under conjunction (_x_ `&&` _true_ `equivalent` _x_) and
forgets structure under disjunction (_x_ `||` _true_ `equivalent` _true_).

### "False / None"

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

Identity names can be described in 2 structures: one for checking that
 a `verifier` corresponds with an `identityName`, and one for checking
 that an `encryptor` corresponds with an `identityName`.
The same name can refer to both a `verifier` and an `encryptor`.

#### Verifier Name SML Signature

--8<-- "./formal/SML/src/verifier_name.sig:verifier_name_description"

```sml
--8<-- "./formal/SML/src/verifier_name.sig:verifier_name"
```

#### Encryptor Name SML Signature

--8<-- "./formal/SML/src/encryptor_name.sig:encryptor_name_description"

```sml
--8<-- "./formal/SML/src/encryptor_name.sig:encryptor_name"

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

Formally, we use `(hash(Alice), "foo")` as the SML representation of _Alice.foo_:

--8<-- "./formal/SML/src/sub_verifier.fun:subverifier_description"

```sml
--8<-- "./formal/SML/src/sub_verifier.fun:subverifier"
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
