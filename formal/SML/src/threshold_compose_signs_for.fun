(* --8<-- [start:threshold_compose_signs_for_description] *)(*
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
*)(* --8<-- [end:threshold_compose_signs_for_description] *)

(* --8<-- [start:threshold_compose_signs_for] *)
functor ThresholdComposeSignsFor(structure S:SIGNS_FOR
  structure Signer:SIGNER sharing Signer = S.Verifier
  structure Map : ORD_MAP sharing Map.Key = S.Verifier.VerifierHash.OrdKey
  structure ThresholdComposeHash : HASH
    where type hashable = {threshold:int, weights : ((int * S.Verifier.verifier) Map.map)}
  ) : SIGNS_FOR = struct
  structure UnderlyingSignsFor = S
  structure Verifier : VERIFIER = ThresholdCompose(
    structure Map = Map
    structure Signer = Signer
    structure Verifier = UnderlyingSignsFor.Verifier
    structure ThresholdComposeHash = ThresholdComposeHash)
  type evidence = S.evidence
  fun signsFor e ({threshold = t0, weights = w0}, {threshold = t1, weights = w1}) =
    Map.all (fn (w,v) => w*t1 <= (Map.foldl (fn ((x,v1), s) =>
      if UnderlyingSignsFor.signsFor e (v, v1) then x+s else s) 0 w1)*t0) w0
end
(* --8<-- [end:threshold_compose_signs_for] *)
