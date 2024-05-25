(* --8<-- [start:hash_description] *)(*
A general purpose signature describing structures that implement a hash
 function.
The output should be an orderable type suitable for a lookup key (hence,
 OrdKey.ord_key).
For example, `Bytes32.bytes32` for 32-byte hashes.
Example implementations could implement
 [SHA3-256](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf),
 [Rescue128](https://eprint.iacr.org/2019/426), etc.

Properties:

- `(compare(hash a , hash b) = EQUAL) = (a = b)`

- In general, `hash a` should convey no other information about `a`

- `OrdKey.ord_key` is the type of our hash.
  It should be constant size, and totally ordered.

- `hash` takes linear time to compute over the size of the input.

*)(* --8<-- [end:hash_description] *)

(* --8<-- [start:hash] *)
signature HASH = sig
  structure OrdKey : ORD_KEY
  type hashable
  val hash : hashable -> OrdKey.ord_key
end
(* --8<-- [end:hash] *)
