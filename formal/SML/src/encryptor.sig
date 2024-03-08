(* ANCHOR: encryptor_description *)(*
A signature describing a type `encryptor` that can cryptographically
 `encrypt` a `plaintext` (message) to create a `ciphertext` readable
 only by the corresponding `decryptor`.
An `encryptor` can be hashed (producing a unique identifier), so a
 structure with signature `ENCRYPTOR` must specify an `EncryptorHash`
 structure defining a suitable hash function.
Implementations should ultimately include, for example,
 [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
 keys,  which should be able to decrypt bitstrings into anything that
 can be  unmarshaled from a bitstring.

Properties:
- `encrypt` should take polynomial time (in the size of its inputs)
- Each `E:ENCRYPTOR` should have a corresponding `D:DECRYPTOR`, and
  each `d: D.decryptor` has a corresponding `e: E.encryptor` such
  that:
  - for all `c : D.cyphertext`, `p : D.plaintext`:
    `D.decrypt d c = Some p` iff `c = E.encrypt e p`
  - if `d = e`, we call this "symmetric encryption," and otherwise
    it's "asymmetric encryption."
    In an asymmetric cryptosystem, a computationally bounded adversary
    should not be able to approximate `d` knowing only `e`.
*)(* ANCHOR_END: encryptor_description *)

(* ANCHOR: encryptor *)
signature ENCRYPTOR = sig
  type encryptor
  type plaintext
  type ciphertext
  val encrypt : encryptor -> plaintext -> ciphertext
  structure EncryptorHash : HASH sharing type EncryptorHash.hashable = encryptor
end
(* ANCHOR_END: encryptor *)
