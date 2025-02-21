---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - proving-system
  - resource-machine
  - type
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.proving_system;
    import prelude open;
    import arch.system.state.resource_machine.prelude open;
    ```

# Proving System

A **proving system** is defined by five type parameters: `Proof`, `VerifyingKey`,
`ProvingKey`, `Instance`, and `Witness`. It provides two core functions:

1. `prove(pk, instance, witness) -> Proof`  
2. `verify(vk, instance, proof) -> Bool`

These functions are used to produce and verify proofs that some statement
involving the instance and witness is correct, under the assumptions of
completeness and soundness.

## Trait Definition

Below is the Juvix trait `ProvingSystem`, parameterized by these five types:

```juvix
trait
type ProvingSystem
  (Proof : Type)
  (VerifyingKey : Type)
  (ProvingKey : Type)
  (Instance : Type)
  (Witness : Type)
:= mkProvingSystem@{
    prove  : ProvingKey -> Instance -> Witness -> Proof;
    verify : VerifyingKey -> Instance -> Proof -> Bool;
};
```

!!! note
    - **Completeness** means that if the statement is true, a proof can be
      generated that passes verification.
    - **Soundness** means that if the statement is false, no valid proof can be
      created (or equivalently, any purported proof will fail verification).

## Usage

The trait can be instantiated to model different proving schemes:

- **Trivial scheme**: replicate the computation in `verify`.
- **Trusted delegation**: rely on a trusted party’s signature.
- **Succinct Proof of Knowledge**: e.g., SNARKs, STARKs, possibly zero-knowledge.

The particular instantiation is determined by how `ProvingKey`, `VerifyingKey`,
`Instance`, `Witness`, and `Proof` are defined, and by the implementations of
`prove` and `verify`.