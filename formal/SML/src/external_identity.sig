(* ANCHOR: external_identity_description *)(*
An External Identity structure specifies the necessary types and
 functions for both a Verifier and an Encyrptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) public keys.

An external_identity includes:
- a type `verifier` that can cryptographically `verify` that a
  `commitment` (or cryptographic signature) corresponds to a given
  message (a `signable`), and was signed by the `signer`
  corresponding to this `verifier`.
- a type `encryptor` that can cryptographically `encrypt` a
  `plaintext` (message) to create a `cyphertext` readable only by the
  corresponding `decryptor`.

Properties are inherited from `VERIFIER` and `ENCRYPTOR`.
*)(* ANCHOR_END: external_identity_description *)

(* ANCHOR: external_identity *)
signature EXTERNAL_IDENTITY = sig
  include VERIFIER
  include ENCRYPTOR
end
(* ANCHOR_END: external_identity *)
