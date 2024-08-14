---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Proving system

We define a set of structures required to define a proving system $PS$ as follows:

- Proof $\pi: PS.Proof$
- Instance $x: PS.Instance$ is the public input used to produce a proof.
- Witness $w: PS.Witness$ is the private input used to produce a proof.
- Proving key $pk: PS.ProvingKey$ contains the secret data required to produce a proof for a pair $(x, w)$.
- Verifying key $vk: PS.VerifyingKey$ contains the data required, along with the witness $x$, to verify a proof $\pi$.

A **proof record** carries the components required to verify a proof. It is defined as a composite structure $PR = (\pi, x, vk): ProofRecord$, where:

- $ProofRecord = PS.VerifyingKey \times PS.Instance \times PS.Proof$
- $vk: PS.VerifyingKey$
- $x: PS.Instance$
- $\pi: PS.Proof$ is the proof of the desired statement

A proving system $PS$ consists of a pair of algorithms, $(Prove, Verify)$:

- $Prove(pk, x, w): PS.ProvingKey \times PS.Instance \times PS.Witness \rightarrow PS.Proof$
- $Verify(pr): PS.ProofRecord \rightarrow \mathbb{F}_b$

A proving system must have the following properties:

- **Completeness**: it must be possible to make a proof for a statement which is true.
- **Soundness**: it must not be possible to make a proof for a statement which is false.

Certain proving systems may also be **Zero-Knowledge**, meaning that the produced proofs reveal no information other than their own validity.

A proof $\pi$ for which $Verify(pr) = 1$ is considered valid.

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