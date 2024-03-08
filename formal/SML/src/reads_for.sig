(* ANCHOR: reads_for_description *)(*
Formally, a `readsFor` relation requires a type of evidence, and an
 `ENCRYPTOR` structure.
This codifies a belief about what `DECRYPTOR`s can read other
 `ENCRYPTOR`s ciphertext.
Evidence can be signed statements, proofs, or even local state about beliefs.

Specifically, if a node expresses a `readsFor` relation, and
 `readsFor e (x,y)`, then the node believes that any node knowing the
 decryptor corresponding to `x` can decrypt `encrypt y p`.
If there is some plaintext `p` such that some node knowing a decryptor
 corresponding to `x` cannot read `encrypt y p`, then the node's
 beliefs, as encoded in the `readsFor` relation, are incorrect.

For example, suppose `Alice` gives her private `decryptor` to `Bob`,
 and wants to let everyone know that `Bob` can now read anything
 encrypted to `Alice`.
Nodes who want to take this into account might accept some sort of
 `e:evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `readsFor e (Bob, Alice)`.

Note that `readsFor` is not symmetric: `readsFor e (x,y)` does not
 imply that any `z` exists such that `readsFor z (y,x)`.
*)(* ANCHOR_END: reads_for_description *)

(* ANCHOR: reads_for *)
signature READS_FOR = sig
  structure Encryptor : ENCRYPTOR
  type evidence
  val readsFor : evidence -> (Encryptor.encryptor * Encryptor.encryptor) -> bool
end
(* ANCHOR_END: reads_for *)
