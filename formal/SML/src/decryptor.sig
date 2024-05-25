(* --8<-- [start:decryptor_description] *)(*
A signature describing a type `decryptor` that can cryptographically
 `decrypt` something (a `cyphertext`), resulting in a `plaintext`
 (or `NONE`, if decryption fails).
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be  unmarshaled from a bitstring.

Properties:

- a computationally bounded adversary should not be able to
  approximate `decrypt d` without knowledge of `d`.

- `decrypt` should take polynomial time (in the size of its inputs)

- Each `D:DECRYPTOR` should have a corresponding `E:ENCRYPTOR`, and
  each `d: D.decryptor` has a corresponding `e: E.encryptor` such
  that:

  - for all `c : D.cyphertext`, `p : D.plaintext`:
    `D.decrypt d c = Some p` iff `c = E.encrypt e p`

  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption"
*)(* --8<-- [end:decryptor_description] *)

(* --8<-- [start:decryptor] *)
signature DECRYPTOR = sig
  type decryptor
  type plaintext
  type cyphertext
  val decrypt : decryptor -> cyphertext -> plaintext option
end
(* --8<-- [end:decryptor] *)
