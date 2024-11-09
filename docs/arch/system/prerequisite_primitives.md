---
# icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Prerequisite primitives

## Canonical compute representation

The protocol requires a canonical serialisation of Turing-equivalent functions and data.

A serialisation can be any function which maps data to a series of bytes. The inverse function which maps a series of bytes to data is referred to as a deserialisation.

Being *canonical* for a serialisation $s$ means that there exists a function $d$
such that, for any function or data $x$, all the agents using the protocol agree
that the following equation holds.

$$s(\mathsf{eval}(d(x))) = x.$$

In what follows, we assume any serialisation is canonical, unless otherwise specified. Internal representations of compute may vary as long as this external equivalence holds. Certain additional correspondences of internal representations may be required for particular verifiable computation schemes (see below).

For the remainder of this specification, this canonical representation is taken as implicit, and may be assumed where appropriate (e.g. `serialise` is called before sending a function over the network).

## Cryptographic components

### Canonical collision-resistant one-way hash function

The protocol requires a so-called "hash" function which computes a fixed-length output from a variable-length preimage.

```haskell
hash :: ByteString -> ByteString
```

`hash` must be both one-way, in that it is not computationally feasible for any agent to compute the preimage from the hash output, and collision-resistant, in that it is not computationally feasible for any agent to find two different preimages which hash to the same value.

Throughout the remainder of this document, serialisation can be assumed to take place first where appropriate, e.g. `hash` can be treated as synonymous with `hash . serialise`.

This hash function does not necessarily need to be canonical - it could be negotiated between groups of agents - but for the sake of simplicity we will assume henceforth that it is.

### Verifiable computation scheme

We assume an abstract verifiable computation scheme operating over arbitrary types and relations such that all agents have access to the following interface:

```haskell
class Proof p where
    prove :: a -> b -> (a -> b -> Bool) -> p
    verify :: a -> b -> (a -> b -> Bool) -> p -> Bool
```

Subject to scheme-specific assumptions, this scheme should provide _correctness_:

```haskell
correctness : Type
correctness =
    predicate a b = 1 -> verify a b predicate (prove a b predicate) = 1
```

and also _soundness_:

```haskell
soundness : Type
soundness =
    predicate a b = 0 -> forall proof . verify a b predicate proof = 0
```

This scheme may be instantiated in various ways with different properties and different assumptions, and the correctness, soundness, and scaling properties of compositions thereof will hold modulo the specific assumptions made.

For example, let's take three common instantiations:

- The _trivial_ scheme is one where computation is simply replicated. The
  trivial scheme is defined as `verify(a, b, predicate, _) = predicate a b`
  (with proof type `()`). It has no extra security assumptions but is not
  succinct.

- The _trusted delegation_ scheme is one where computation is delegated to a
  known, trusted party whose work is not checked. The trusted delegation scheme
  is defined as `verify(a, b, predicate, proof) = checkSignature (a, b,
  predicate) proof`, where the trusted party is assumed to produce such a
  signature only if `predicate a b = 1`. This scheme is succinct but requires a
  trusted party assumption (which could be generalised to a threshold quorum in
  the obvious way). Note that since the computation is still verifiable, a
  signer of `(a, b, predicate)` where `predicate a b = 0` could be held
  accountable by anyone else who later checked the predicate.

- The _succinct proof-of-knowledge_ scheme is one where the result of computation is attested to with a cryptographic proof (of the sort commonly instantiated by modern-day SNARKs & STARKs). Succint proof-of-knowledge schemes provide succinctness as well as veriability subject to the scheme-specific cryptographic assumptions. They may also possibly be _zero-knowledge_, in which the verifier learns nothing other than `predicate a b = 1` (in this case, and in others, `a` and `b` will often be "hidden" with hash functions, such that the verifier knows only `hash a` and `hash b` but the substance of the relation obtains over the preimages).

Global consensus on the verifiable computation scheme is not required, and there is no canonical one, but agents must agree on a particular scheme to use for a particular case of verifiable computation, and agents must know the `Proof` type and `prove` / `verify` functions for any scheme which they use.
