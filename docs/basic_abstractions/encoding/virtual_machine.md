---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---


# Virtual machine

A _virtual machine_ is a specific way to represent functions, uniquely defined by three functions _encode_, _decode_, and _evaluate_. The protocol uses virtual machines in several places:

- wherever we need canonical commitments to and evaluatable representations of functions, such as external identities
- in the resource machine, for resource logics
- in the resource machine, for transaction functions
- in application definitions, for projection functions

In general, the protocol does not require the same virtual machine to be used in all of these places, or even a specific virtual machine to be used in a specific place. However, agents who wish to interoperate must agree on the definitions of the virtual machines which they are using, and different virtual machines may have different performance characteristics in different contexts. In order to facilitate interoperability, the protocol standardizes a multiformat of virtual machines, where each virtual machine is associated with a unique natural number. We will refer to the virtual machine associated with $n$ as $VM_n$, and associated functions as $encode_n$, $decode_n$, and $evaluate_n$. Each virtual machine, in the implementation language, also comes with an opaque internal representation type $VM_n.t$.

## Decoding

The decoding function $decode_n$ attempts to decode a `DataValue` into an internal representation $VM_n.t$. Decoding which encounters a `FunctionV` associated with a different virtual machine will simply represent that as data (instead of code) in the internal representation type.

```juvix
type Decode = DataValue -> Maybe VM_n.t
```

## Encoding

The encoding function $encode_n$ encodes an internal representation of a function and/or data into a `DataValue`. Functions in the internal representation will be serialized in some fashion and paired with the natural number associated with the virtual machine in a `FunctionV`.

```juvix
type Encode = VM_n.t -> DataValue
```

### Properties

The encoding and decoding functions must be inverses of each other, in that:

- decoding an encoded value will result in `Just <that value>`
- encoding a decoded value will result in the original internal representation

## Evaluation

The evaluation function $evaluate_n$ calls a function (in the internal representation) on the provided list of arguments (in the original representation). Evaluation must be deterministic. Evaluation must also meter _gas_, a measure of compute and memory resource expenditure. Different virtual machines will have different gas scales. Evaluation takes a _gas limit_. During VM internal execution, gas must be tracked, and evaluation must terminate if the gas limit is exceeded. Should execution complete successfully within the gas limit, the VM must return the gas actually used.

```juvix
type Evaluate =
  VM_n.t ->
  [VM_n.t] ->
  Natural ->
  (Maybe VM_n.t, Natural)
```

!!! note

    In the future, gas will likely change from a scalar to a vector to allow for metering compute and memory resources differently.

# Provable virtual machines

A _provable_ virtual machine is a virtual machine with a proof type $P_n$ and two additional functions parameterized over $P_n$, $prove_n$ and $verify_n$.

## Proving

The proving function $prove_n$ generates a proof for a given program (logical relation), public input, and private input.

!!! note

    Parentheses here are used to indicate the expected type of the arguments. Calling `prove` with arguments of the wrong type will fail.

```juvix
type Prove =
  VM_n.t (T0 -> T1 -> boolean) ->
  VM_n.t (T0) ->
  VM_n.t (T1) ->
  P_n
```

## Verification

The verification function $verify_n$ verifies a proof for a given program and public input.

!!! note

    Parentheses here are used to indicate the expected type of the arguments. Calling `verify` with arguments of the wrong type will fail.

```juvix
type Verify =
  VM_n.t (T0 -> T1 -> boolean) ->
  VM_n.t (T1) ->
  P_n ->
  boolean
```

## Properties

These functions must be _sound_ and _complete_, in that:

- valid proofs can only be created for valid inputs (_soundness_), and a valid proof can be created for any valid input (_completeness_)
-  i.e. `verify f public proof = true` if and only if `proof = prove f public' private'` where `public = public'` and `evaluate f [public', private'] g = (true, _)` for some sufficient gas limit `g` (we could probably split evaluation into gassy and gassless versions)

Should `P_n` not reveal any information about `VM_n.t (T0)`, the provable virtual machine can be said to be _zero-knowledge_.