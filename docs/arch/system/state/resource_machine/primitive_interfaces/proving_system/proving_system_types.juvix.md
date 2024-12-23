---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.primitive_interfaces.proving_system.proving_system_types;
import prelude open;
```

# Proving system definition


We define a set of structures required to define a proving system $PS$ as follows:

- Proof $\pi: PS.Proof$ - proves that a specific statement `f` with the inputs `x` and `w` evaluates to `True`.
- Instance $x: PS.Instance$ is the ordered input data structure used to produce and verify a proof.
- Witness $w: PS.Witness$ is the ordered input data structure used to produce (but not verify) a proof.
- Proving key $pk: PS.ProvingKey$ contains the data required to produce a proof for a pair $(x, w)$. Specific to a particular statement (different statements `f` and `f'` imply different proving keys) being proven, but doesn't depend on the inputs.
- Verifying key $vk: PS.VerifyingKey$ contains the data required, along with the instance $x$, to verify a proof $\pi$. Specific to a particular statement being proven (different statements `f` and `f'` imply different verifying keys), but doesn't depend on the inputs.

Besides a paramter `Statement`
(that is left underspecified for the time being),
we have the type parameters as listed above.

```juvix
type ProvingSystemStructure
     (Statement Proof Instance Witness ProvingKey VerifyingKey : Type) :=
            mkProvingSystemStructure@{
                 f : Statement;
                 pi : Proof;
                 x : Instance;
                 w : Witness;
                 pk : ProvingKey;
                 vk : VerifyingKey;
            }
;
```

!!! todo "instances : ordered input data structure ???"

    What does it mean for (the type of) instances to be ordered?

!!! todo "witnesses : ordered input data structure ???"

    What does it mean for (the type of) witnesses to be ordered?
    
A _proving system $PS$_ consists of a pair of algorithms, $(Prove, Verify)$:

- $Prove(pk, x, w): PS.ProvingKey \times PS.Instance \times PS.Witness \rightarrow PS.Proof$
- $Verify(vk, x, \pi): PS.VerifyingKey \times PS.Instance \times PS.Proof \rightarrow Bool$.

Thus, the trait of a proving system has two methods.

```juvix
trait
type record ProvingSystem
     (Statement Proof Instance Witness ProvingKey VerifyingKey : Type) :=
     mkProvingSystem@{
         prove : ProvingKey -> Instance -> Witness -> Proof;
         verify : VerifyingKey -> Instance -> Proof -> Bool;
     }
;
```

!!! note
    To verify a proof created for instance `x`, the same instance `x` must be used. For instances that contain elements of the same type, the order of the elements must be preserved.

!!! todo "add «axioms» to the signature"

    Ideally, we want to add the "axiom"
    $verify(vk, y, prove(pk, x, w)) = true \Rightarrow x = y$.

### Properties

A proving system must have the following properties:

- **Completeness**: it must be possible to make a proof for a statement which is true.
- **Soundness**: it must not be possible to make a proof for a statement which is false.

For a statement `f`, `Verify(vk, x, proof) = True` implies that `f x w = True` and `Verify(vk, x, proof) = False` implies that `f x w = False`.

!!! todo "completeness"

    How to express that for all terms $f$ of type Statement such that $f x w = True$,
    there exists a witness $w$, an instance $x$ (...)
    such that $Verify(vk, x, prove(pk, x, w))$⁈
    So,
    the type `Statement` is
    a (very special) subtype of $Instance \to Witness \to Bool$.

!!! todo "soundness"

    _mutatis mutandis_

Certain proving systems may also be **zero-knowledge**, meaning that the produced proofs reveal no information other than their own validity.

A proof $\pi$ for which $Verify(pr) = True$ is considered _valid_.

### Common proving scheme types

- The _trivial_ scheme is one where computation is simply replicated. The
  trivial scheme is defined as `verify(predicate, x, _) = predicate x`. It has no extra security assumptions but is not succinct. In this case, all of the data is used for both proving and verifying and witness and proof has unit type `()`.

- The _trusted delegation_ scheme is one where computation is delegated to a
  known, trusted party whose work is not checked. The trusted delegation scheme
  is defined as `verify((predicate, pk), x, sig) = checkSignature pk (predicate, x) sig`, where the trusted party is assumed to produce such a
  signature only if `predicate x = True`. This scheme is succinct but requires a
  trusted party assumption (which could be generalised to a threshold quorum in
  the obvious way). Note that since the computation is still verifiable, a
  signer of `(predicate, x)` where `predicate x = False` could be held
  accountable by anyone else who later evaluated the predicate. In this case witness also has unit type and the proof has the type `Signature`.

- The _succinct proof-of-knowledge_ scheme is one where the result of computation is attested to with a cryptographic proof (of the sort commonly instantiated by modern-day SNARKs & STARKs). Succinct proof-of-knowledge schemes provide succinctness as well as verifiability subject to the scheme-specific cryptographic assumptions. They may also possibly be _zero-knowledge_, in which the verifier learns nothing other than `predicate x w = True` (in this case, and in others, `w` will be "hidden" with hash functions and `x` will remain public (and include the hiding representations of `w`), such that the verifier knows only `hash w` and `x` but the substance of the relation obtains over the preimages).

Assuming the proving system is used to verify that a predicate evaluated on its inputs returns `True`, the table below describes what each parameter will be for each of the three common proving system instantiations:

||Proving key|Verifying key|Instance (x)|Witness (w)|Proof|Properties|
|-|-|-|-|-|-|-|
|Trivial scheme|predicate|predicate|predicate's arguments|()|()|transparent, not succinct|
|Trusted delegation|predicate + signing key|predicate + signature verifying key|predicate's arguments|()|signature|succinct, trusted, verifiable|
|Succinct PoK|defined by the scheme (incl. predicate representation)|defined by the scheme|public input|private input|defined by the scheme|succinct, verifiable, possibly zero knowledge|

!!! note

In practice, the predicate and its arguments can be represented as a hash or commitment to the actual value. In the trivial scheme, they would have to be opened in order to verify them. In the trusted delegation case, they *don't have to* be opened if the signature is produced over the hashed values.

!!! note
  For application developers: writing applications that can work with all types of systems can be challenging since different proof types require different argument split between instance and witness (e.g., trivial scheme, unlike succinct PoK, expects no witness). The current solution is to write applications with succinct PoK types of proving systems in mind, which then can be translated to other proving systems by moving witness arguments to instance.
