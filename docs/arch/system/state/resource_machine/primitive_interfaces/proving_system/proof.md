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

!!! warning

    The content will likely change soon.

# Proof

We define a set of structures required to define a proving system $PS$ as follows:

- Proof $\pi: PS.Proof$ - proves that a specific statement `f` with the inputs `x` and `w` evaluates to `True`.
<!--ᚦ«do we have a type for `f` `x` and `w`?»-->
<!--ᚦ«Moving this line after Instance and Witness avoids the confusion.»-->
<!--‼type f := (PS.Instance × PS.Witness) → Bool-->
- Instance $x: PS.Instance$ is the ordered input data structure used to produce and verify a proof.
<!--ᚦ«ordered in which sense? post-ordering ? (partially) ordered?»-->
<!--ᚦ«do we have an (internal/external) link to examples of such instances?»-->
- Witness $w: PS.Witness$ is the ordered input data structure used to produce (but not verify) a proof.
<!--ᚦ«ordered in which sense?»-->
<!--ᚦ«do we have an (internal/external) link to examples of such witnesses?»-->
- Proving key $pk: PS.ProvingKey$ contains the data required to produce a proof for a pair $(x, w)$. Specific to a particular statement (different statements `f` and `f'` imply different proving keys) being proven, but doesn't depend on the inputs.
<!--ᚦ«So, the proving key determines the statement; 
can there be several proving keys for the same statement? 
A (foot)note may be useful.
»-->
- Verifying key $vk: PS.VerifyingKey$ contains the data required, along with the instance $x$, to verify a proof $\pi$. Specific to a particular statement being proven (different statements `f` and `f'` imply different verifying keys), but doesn't depend on the inputs.
<!--ᚦ«what about the converse the implication?»-->

A proving system $PS$ consists of a pair of algorithms, $(Prove, Verify)$:
<!--ᚦ«Can these algorithms be functions for the purposes of the specs?»-->

- $Prove(pk, x, w): PS.ProvingKey \times PS.Instance \times PS.Witness \rightarrow PS.Proof$
<!--ᚦ«can explain what happens here? sth. like "this function generates a proof for the existence of a witness $w$ for $f(\mathit{pk}, x, w)$ where $f$ is $f_{pk}$, the statement of the proving key."»-->
- $Verify(vk, x, \pi): PS.VerifyingKey \times PS.Instance \times PS.Proof \rightarrow Bool$.
<!--ᚦ«can explain what happens here? sth. like "this function verifies that the proof for the existence of a witness for $f(x,w)$ [...] is valid/correct/...»-->

!!! note

    To verify a proof created for instance `x`, the same instance `x` must be used. For instances that contain elements of the same type, the order of the elements must be preserved.
<!--ᚦ«So, at the first sentence, verifying a proof $\pi=\mathit{Prove}(\mathit{pk}, x, w)$
by invoking $\mathit{Verify}(\mathit{vk}, y, \pi)$ and obtaining true is only possible if $x=y$?
»-->
<!--ᚦ«So, PS.Instance is not a base type but has additional structure?»-->
<!--ᚦ«the `x` should probably be $x$ for consistency»-->

A proving system must have the following properties:

- **Completeness**: it must be possible to make a proof for a statement which is true.
<!--ᚦ«
i.e., whenever $f(x,w)$ is true, there is some pk for f and a  prove for it
→
"every statement" of a certain type, I guess
»-->
- **Soundness**: it must not be possible to make a proof for a statement which is false.

For a statement `f`, `Verify(vk, x, proof) = True` implies that `f x w = True` and `Verify(vk, x, proof) = False` implies that `f x w = False`.
<!--ᚦ«
How is the relation of $f$ and vk pk?
»-->

Certain proving systems may also be **zero-knowledge**, meaning that the produced proofs reveal no information other than their own validity.

A proof $\pi$ for which $Verify(pr) = True$ is considered valid.
<!--ᚦ«
    Is this a definition? "A proof is ᴠᴀʟɪᴅ when ..."
»-->
<!--ᚦ«
$\pi$ = `pr` ? Or what else is the relation between $\pi$ and `pr`?
»-->

For example, let's take three common instantiations:
<!--ᚦ«... of proving systems.»-->

- The _trivial_ scheme is one where computation is simply replicated. The
  trivial scheme is defined as `verify(predicate, x, _) = predicate x`. It has no extra security assumptions but is not succinct. In this case, all of the data is used for both proving and verifying and witness and proof has unit type `()`.
<!--ᚦ«
    The juvix type is `Unit`.
type Unit :=
  --- The only constructor of ;Unit;.
  unit;
»-->

- The _trusted delegation_ scheme is one where computation is delegated to a
  known, trusted party whose work is not checked. The trusted delegation scheme
  is defined as `verify((predicate, pk), x, sig) = checkSignature pk (predicate, x) sig`, where the trusted party is assumed to produce such a
  signature only if `predicate x = True`. This scheme is succinct but requires a
  trusted party assumption (which could be generalised to a threshold quorum in
  the obvious way). Note that since the computation is still verifiable, a
  signer of `(predicate, x)` where `predicate x = False` could be held
  accountable by anyone else who later evaluated the predicate. In this case witness also has unit type and the proof has the type `Signature`.
<!--ᚦ«adapt to signatures of the specs»-->
<!--ᚦ«spelling is british-ize , e.g. generalize »-->

- The _succinct proof-of-knowledge_ scheme is one where the result of computation is attested to with a cryptographic proof (of the sort commonly instantiated by modern-day SNARKs & STARKs). Succinct proof-of-knowledge schemes provide succinctness as well as verifiability subject to the scheme-specific cryptographic assumptions. They may also possibly be _zero-knowledge_, in which the verifier learns nothing other than `predicate x w = True` (in this case, and in others, `w` will be "hidden" with hash functions and `x` will remain public (and include the hiding representations of `w`), such that the verifier knows only `hash w` and `x` but the substance of the relation obtains over the preimages).
<!--ᚦ«adding links may be useful»-->

Assuming the proving system is used to verify that a predicate evaluated on its inputs returns `True`, the table below describes what each parameter will be for each of the three common proving system instantiations:

||Proving key|Verifying key|Instance (`x`)|Witness (`w`)|Proof|Properties|
|-|-|-|-|-|-|-|
|Trivial scheme|predicate|predicate|predicate's arguments|()|()|transparent, not succinct|
|Trusted delegation|predicate + signing key|predicate + signature verifying key|predicate's arguments|()|signature|succinct, trusted, verifiable|
|Succinct PoK|defined by the scheme (incl. predicate representation)|defined by the scheme|public input|private input|defined by the scheme|succinct, verifiable, possibly zero knowledge|
<!--ᚦ«PoK → proof of knowledge / link»-->

!!! note

    In practice, the predicate and its arguments can be represented as a hash or commitment to the actual value. In the trivial scheme, they would have to be opened in order to verify them. In the trusted delegation case, they *don't have to* be opened if the signature is produced over the hashed values.

<!--ᚦ«What does it mean to open? cf. opening of a Hash?»-->

<!--ᚦ
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global remarks
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
«mandy concepts deserve links, externally and internally»-->

<!--ᚦtags:reviewed,consistent-->
