(* --8<-- [start:subverifier_description] *)(*
A specific kind of identity name, wher ethe evidence is a signed
 statement from a specified parent saying that it associates this
 verifier with a specific `name`.

Here,
- `name` is the type the parent identifies with a child.
  For example, for `name = string`, and some identity Alice, we can specify
  `(hash(Alice),"bob")`, or _Alice.bob_, as the identity that
  Alice refers to as `"bob"`.
- `Child` : `VERIFIER` type that can be identified with a name.
- `Parent` : `VERIFIER` type that signs evidence statements.
  Crucially, it must be able to sign tuples of the form
  (string, name, Child's hash type)
  In our example, where Alice refers to Bob as Alice.`"bob"`, `Child` describes
  Bob, `Parent` describes Alice, and `name` describes `"bob"`.
- `Hash` Describes what will become the `VerifierNameHash`.
  Crucially, it must be able to hash pairs of the form
  (Parent's hash type, name)
*)(* --8<-- [end:subverifier_description] *)

(* --8<-- [start:subverifier] *)
functor SubVerifier (
  type name
  structure Child : VERIFIER
  structure Parent : VERIFIER where type signable = string * name * Child.VerifierHash.OrdKey.ord_key
  structure Hash : HASH where type hashable = Parent.VerifierHash.OrdKey.ord_key * name
  ) : VERIFIER_NAME = struct
  structure Verifier = Child
  structure VerifierNameHash = Hash
  type evidence = Parent.verifier * Parent.commitment
  type identityName = Parent.VerifierHash.OrdKey.ord_key * name
  fun checkVerifierName (ph, n) c (pv, pc)  = 
    (Parent.verify pv ("I identify this Verifier with this name: ", n, Child.VerifierHash.hash(c)) pc)
    andalso (Parent.VerifierHash.OrdKey.compare(ph,(Parent.VerifierHash.hash pv)) = EQUAL)
end
(* --8<-- [end:subverifier] *)
