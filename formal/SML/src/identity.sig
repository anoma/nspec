(* --8<-- [start:identity_description] *)(*
An Identity structure, formally, specifies all the types for
 corresponding internal and external identities.
So, for a given Identity structure `I`, `I.verifier` should be the
 type of objects that can verify `commitment`s produced by a
 corresponding object of type `I.signer`.
Likewise, `I.decryptor` should be the type of objects that can decrypt
 `cyphertext`s produced by a corresponding object of type
 `I.encryptor`.
Implementations should ultimately include, for example,
 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
 public / private keys sytems.

An Identity includes:


- a type `signer` that can cryptographically `sign` (or credibly commit) to something (a `signable`), forming a `commitment`.

- a type `decryptor` that can cryptographically `decrypt` something (a `cyphertext`), resulting in a `plaintext` (or `NONE`, if decryption fails).

- a type `verifier` that can cryptographically `verify` that a `commitment` (or cryptographic signature) corresponds to a given message (a `signable`), and was signed by the `signer` corresponding to this `verifier`.

- a type `encryptor` that can cryptographically `encrypt` a `plaintext` (message) to create a `cyphertext` readable only by the corresponding `decryptor`.

Properties are inherited from `VERIFIER`, `ENCRYPTOR`, `SIGNER`, and `DECRYPTOR`.
*)(* --8<-- [end:identity_description] *)

(* --8<-- [start:identity] *)
signature IDENTITY = sig
  include  INTERNAL_IDENTITY
  include  EXTERNAL_IDENTITY
end
(* --8<-- [end:identity] *)
