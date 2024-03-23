(* --8<-- [start:signs_for_description] *)(*
Formally, a `signsFor` relation requires a type of evidence, and a
 `VERIFIER` structure.
This codifies a belief about what `verifier`'s `commitments` are
 "at least as good as" another `verifier`'s.
Evidence can be signed statements, proofs, or even local state about beliefs.

For example, suppose `Alice` wants to grant authority to `Bob` to
 `sign` on her behalf.
Nodes who want to take this into account might accept some sort of
 `e:evidence`, perhaps a signed statement from `Alice`, so that they
 can recognize that `signsFor e (Bob, Alice)`.

Note that `signsFor` is not symmetric: `signsFor e (x,y)` does not
 imply that any `z` exists such that `signsFor z (y,x)`.
*)(* --8<-- [end:signs_for_description] *)

(* --8<-- [start:signs_for] *)
signature SIGNS_FOR = sig
  structure Verifier : VERIFIER
  type evidence
  val signsFor : evidence -> (Verifier.verifier * Verifier.verifier) -> bool
end
(* --8<-- [end:signs_for] *)
