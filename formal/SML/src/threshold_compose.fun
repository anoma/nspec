(* --8<-- [start:threshold_compose_description] *)(*
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
   two input verifiers: a `signer` must encode the information of the
   signers for *both* `x` and `y` to sign statements `verifierAnd x y`
   will verify.
- `fun verifierOr` creates a composed `verifier` that is the "||" of
   two input verifiers: a `signer` must encode the information of the
   signers for *either* `x` or `y` to sign statements `verifierOr x y`
   will verify.
*)(* --8<-- [end:threshold_compose_description] *)

(* --8<-- [start:threshold_compose] *)
functor ThresholdCompose (
  structure Verifier:VERIFIER
  structure Signer:SIGNER sharing Signer = Verifier
  structure Map : ORD_MAP sharing Map.Key = Verifier.VerifierHash.OrdKey
  structure ThresholdComposeHash : HASH
    where type hashable = {threshold:int, weights : ((int * Verifier.verifier) Map.map)}
  ) = struct
  structure Map = Map
  structure UnderlyingVerifier = Verifier
  structure UnderlyingSigner = Signer
  structure VerifierHash = ThresholdComposeHash
  type signer = UnderlyingSigner.signer Map.map
  type verifier = VerifierHash.hashable
  type signable = UnderlyingVerifier.signable
  type commitment = UnderlyingVerifier.commitment Map.map
  fun sign s m = Map.map (fn i => UnderlyingSigner.sign i m) s
  fun verify {threshold = t, weights = ws} s c = t <= (Map.foldl op+ 0 (
    Map.intersectWith (fn ((w,v), x) => if UnderlyingVerifier.verify v s x then w else 0) (ws, c)))
  fun signerCompose (l : (UnderlyingVerifier.verifier * UnderlyingSigner.signer) list) : signer =
    foldl (fn ((v,s), m) => Map.insert(m, UnderlyingVerifier.VerifierHash.hash v, s)) Map.empty l
  fun verifierCompose (threshold : int)
                      (weights : (int * UnderlyingVerifier.verifier) list)
                      : verifier =
    {threshold = threshold,
     weights = foldl (fn ((w,v), m) =>
       Map.insert(m, UnderlyingVerifier.VerifierHash.hash v, (w, v))) Map.empty weights}
  fun verifierAnd (x: UnderlyingVerifier.verifier)
                  (y: UnderlyingVerifier.verifier)
                  : verifier = verifierCompose 2 [(1,x), (1,y)]
  fun verifierOr (x: UnderlyingVerifier.verifier)
                 (y: UnderlyingVerifier.verifier)
                 : verifier = verifierCompose 1 [(1,x), (1,y)]
end
(* --8<-- [end:threshold_compose] *)
