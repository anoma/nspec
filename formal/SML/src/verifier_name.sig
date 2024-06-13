(* Sometimes it is useful to have a name for an external identity
    before the relevant cryptographic values are available. *)

(* --8<-- [start:verifier_name_description] *)(*
An `identityName` can be mapped to an appropriate `Verifier.verifier`
 when suitable `evidence` is found.
Here, `checkVerifierName` defines what evidence is acceptable for a
 `Verifier.verifier`.

Note that `identityName`s are also hashable: we require a structure
 `VerifierNameHash` that details how to hash them.
*)(* --8<-- [end:verifier_name_description] *)

(* --8<-- [start:verifier_name] *)
signature VERIFIER_NAME = sig
  structure Verifier : VERIFIER
  type evidence
  type identityName
  val checkVerifierName : identityName -> Verifier.verifier -> evidence -> bool
  structure VerifierNameHash : HASH sharing type VerifierNameHash.hashable = identityName
end
(* --8<-- [end:verifier_name] *)
