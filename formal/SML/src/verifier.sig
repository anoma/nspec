(* --8<-- [start:verifier_description] *)(*
A signature describing a type `verifier` that can cryptographically
 `verify` that a `commitment` (or cryptographic signature) corresponds
 to a given message (a `signable`), and was signed by the `signer`
 corresponding to this `verifier`.
A `verifier` can be hashed (producing a unique identifier), so a
 structure with signature `VERIFIER` must specify a `VerifierHash`
 structure defining a suitable `hash` function.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature)
 identities.

Properties:
- In general, every `V:VERIFIER` needs a corresponding `S:SIGNER`, and
  every `s:S.signer` needs a corresponding `v:V.verifier`, such that:
  - For any message `m`: `verify v m x = (x = (sign s m))`
  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.
*)(* --8<-- [end:verifier_description] *)

(* --8<-- [start:verifier] *)
signature VERIFIER = sig
  type verifier
  type signable
  type commitment
  val verify : verifier -> signable -> commitment -> bool
  structure VerifierHash : HASH sharing type VerifierHash.hashable = verifier
end
(* --8<-- [end:verifier] *)
