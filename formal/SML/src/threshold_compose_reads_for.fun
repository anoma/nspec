(* --8<-- [start:threshold_compose_reads_for_description] *)(*
 A `readsFor` relation for easy comparison of
  `ThresholdComposeEncryptor.encryptor`s
 _x_ `readsFor` _y_ if every underlying encryptor in _x_ has no more
  weight (divided by threshold) as encryptors it `readsFor` in y.
This implies that anything which can decrypt as _x_ can also decrypt
 as _y_.

This requires an underlying `R:READS_FOR` for comparing the weighted
 encryptors in  _x_ and _y_, which in turn may require evidence.
No additional evidence is required.
*)(* --8<-- [end:threshold_compose_reads_for_description] *)

(* --8<-- [start:threshold_compose_reads_for] *)
functor ThresholdComposeReadsFor(structure R:READS_FOR
    structure Map : ORD_MAP sharing Map.Key = R.Encryptor.EncryptorHash.OrdKey
    structure ThresholdComposeHash : HASH
      where type hashable = {threshold:int, weights : ((int * R.Encryptor.encryptor) Map.map)}
  ) : READS_FOR = struct
  structure UnderlyingReadsFor = R
  structure Encryptor = ThresholdComposeEncryptor(
    structure Map = Map
    structure Encryptor = UnderlyingReadsFor.Encryptor
    structure ThresholdComposeHash = ThresholdComposeHash)
  type evidence = UnderlyingReadsFor.evidence
  fun readsFor e ({threshold = t0, weights = w0}, {threshold = t1, weights = w1}) =
    Map.all (fn (w,v) => w*t1 <= (Map.foldl (fn ((x,v1), s) =>
      if UnderlyingReadsFor.readsFor e (v, v1) then x+s else s) 0 w1)*t0) w0
end
(* --8<-- [end:threshold_compose_reads_for] *)
