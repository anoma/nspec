---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

!!! todo

    This whole page needs to be reworked.

    Questions:

    - What should this type be now?
    - Is everything just a provable VM?
    - VM gives the semantics to interpret the function, which seems necessary.
    - We have some type of assumptions $Assumption$
    - $prove_n$ generates the proof of type $Proof_n$
    - $assumptions_n$ returns the assumptions required for a proof
    - $verify_n$ verifies a proof of type $Proof_n$

---

# Proof

We define a set of structures required to define a proving system $PS$ as follows:

- Proof $\pi: PS.Proof$
- Instance $x: PS.Instance$ is the input used to produce and verify a proof.
- Witness $w: PS.Witness$ is the input used to produce (but not verify) a proof.
- Proving key $pk: PS.ProvingKey$ contains the data required to produce a proof for a pair $(x, w)$.
- Verifying key $vk: PS.VerifyingKey$ contains the data required, along with the instance $x$, to verify a proof $\pi$.

A proving system $PS$ consists of a pair of algorithms, $(Prove, Verify)$:

- $Prove(pk, x, w): PS.ProvingKey \times PS.Instance \times PS.Witness \rightarrow PS.Proof$
- $Verify(vk, x, \pi): PS.VerifyingKey \times PS.Instance \times PS.Proof \rightarrow \mathbb{F}_b$

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