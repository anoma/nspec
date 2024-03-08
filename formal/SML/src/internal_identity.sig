(* ANCHOR: internal_identity_description *)(*
An Internal Identity structure specifies the necessary types and
 functions for both a Signer and a Decryptor.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) private keys,
 which should be able to decrypt integers into anything that can be
 unmarshaled from a bitstring, and sign anything which can be
 marshaled into a bytestring to form an integer.

An internal_identity includes:
- a type `signer` that can cryptographically
  `sign` (or credibly commit) to something (a `signable`), forming a
  `commitment`.
- a type `decryptor` that can cryptographically `decrypt` something
  (a `cyphertext`), resulting in a `plaintext`
  (or `NONE`, if decryption fails).

Properties are inherited from `SIGNER` and `DECRYPTOR`.
*)(* ANCHOR_END: internal_identity_description *)

(* ANCHOR: internal_identity *)
signature INTERNAL_IDENTITY = sig
  include SIGNER
  include DECRYPTOR
end
(* ANCHOR_END: internal_identity *)
