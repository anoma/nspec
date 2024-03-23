(* --8<-- [start:signer_description] *)(*
A signature describing a type `signer` that can cryptographically
 `sign` (or credibly commit) to something (a `signable`), forming a
 `commitment`.
Implementations should ultimately include, for example
 [BLS](https://en.wikipedia.org/wiki/BLS_digital_signature) keys,
  which should be able to sign anything that can be marshaled into a
  bitstring.

Properties:
- In general, every `S:SIGNER` needs a corresponding `V:VERIFIER`, and
  every `s:S.signer` needs a corresponding `v:V.verifier`, such that:
  - For any message `m`: `verify v m x = (x = (sign s m))`
  - for most cryptosystems, a computationally bounded adversary should not be
    able to approximate `s` knowing only `v`.
*)(* --8<-- [end:signer_description] *)

(* --8<-- [start:signer] *)
signature SIGNER = sig
  type signer
  type signable
  type commitment
  val sign : signer -> signable -> commitment
end
(* --8<-- [end:signer] *)
