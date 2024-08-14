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

## Basic definition

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

These functions must be inverses of each other.

## Evaluation

An _evaluatable_ virtual machine is a virtual machine with an additional function _evaluate_, which simply calls a function (in the internal representation) on the provided list of arguments.

Evaluation must be deterministic.

Evaluation must also meter _gas_, a measure of compute and memory resource expenditure. Different virtual machines will have different gas scales. Evaluation takes a _gas limit_. During VM internal execution, gas must be tracked, and execution must terminate if the gas limit is exceeded. Should execution complete successfully within the gas limit, the VM must return the gas actually used.

```juvix
type Evaluate =
  Repr ->
  Repr ->
  Natural ->
  (Maybe Repr, Natural)
```

!!! note

    In the future, gas will likely change from a scalar to a vector to allow for metering compute and memory resources differently.

## Proving

A _provable_ virtual machine is a virtual machine with a proof type `P` and two additional functions parameterized over `P`:

The _prove_ function generates a proof for a given program, public input, and private input.

```juvix
type Prove =
  Repr (T0 -> T1 -> T2 -> boolean) ->
  Repr T0 ->
  Repr T1 ->
  P
```

The _verify_ function verifies a proof for a given program and public input.

```juvix
type Verify =
  Repr (T0 -> T1 -> T2) ->
  Repr T1 ->
  P ->
  boolean
```

These functions must be _correct_ and _complete_, in that:

- valid proofs can only be created for valid inputs (_correctness_)
- a valid proof can be created for any valid input (_completeness_)

Should `P` not reveal any information about `Repr T0`, the provable virtual machine can be said to be _zero-knowledge_.