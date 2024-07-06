---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Virtual machine

A virtual machine is a specific way to represent functions.

The protocol uses virtual machines in several places:
- wherever we need canonical commitments to and evaluatable representations of functions, such as external identities
- in the resource machine, for resource logics
- in the resource machine, for transaction functions
- in application definitions, for projection functions

In general, the protocol does not require the same virtual machine to be used in all of these places, or even a specific virtual machine to be used in a specific place. However, agents who wish to interoperate must agree on the definitions of the virtual machines which they are using, and different virtual machines may have different performance characteristics in different contexts.

A _virtual machine_ is an encoding of arbitrary classically-computable functions defined by a representation type `Repr` and two (type-parameterised) functions, `deserialise` and `serialise`:

The representation type `Repr` includes the type of an encoded function and some opaque internal representation:

```juvix
type Repr := mkRepr {
  type :: Datatype;
  internal :: t;
}
```

The `deserialise` function attempts to deserialise a bytestring into an internal representation of a function of the specified type.

```juvix
type Deserialise = Datatype -> Bytestring -> Maybe Repr
```

The `serialise` function serialises an internal representation of a function into a bytestring.

```
type Serialise = Repr -> Bytes
```

These functions must be inverse, i.e.:

- `deserialise t . serialise 

First, however, what exactly is a virtual machine? Let’s try to capture a definition in math:

A virtual machine is an encoding of arbitrary classically-computable functions defined by two (type-parameterized) functions:
deserialise : bytes -> Maybe (Repr T) which attempts to deserialise a bytestring into an internal representation of a function of type T.
serialise : Repr T -> bytes which serialises an internal representation of a function of a type T into a bytestring.
These functions must be inverses, i.e. deserialise . serialise = Just . id. and fmap serialise . deserialise = id.
An evaluatable virtual machine is a virtual machine with an additional function evaluate : (Repr (T0 -> T1)) -> Repr T0 -> Repr T1, which simply calls a function on the provided argument (in an internal representation). evaluate is required to be deterministic.
A provable virtual machine is a virtual machine with two additional functions parameterized over a proof type P:
prove : Repr (T0 -> T1 -> T2 -> boolean) -> Repr T0 -> Repr T1 -> P generates a proof, where Repr T0 is understood as the private input, and Repr T1 as the public input.
verify : Repr (T0 -> T1 -> T2) -> Repr T1 -> P -> boolean verifies a proof for a given program and public input.
Should P not reveal any information about Repr T0, the provable virtual machine can be said to be zero-knowledge.
