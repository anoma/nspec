---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.primitive_interfaces.index;
```

# Primitive interfaces

This section defines the hierarchy of primitives used in resource machine design and describes interfaces for each primitive.

The diagram below illustrates the primitive types required for resource machine. Red nodes correspond to primitive interfaces, green nodes correspond to instantiations of the interfaces. Each primitive instantiation has an associated type, e.g. delta hash instantiation of `Hash` interface has an associated type `DeltaHash`. Primitive instantiations' names are derived from the type name but written in lower camel case, e.g., for `DeltaHash` the corresponding function would be `deltaHash(..)`.

<figure markdown>

```mermaid
flowchart LR
    ProvingSystem
    Map --> MapInstance
    CommitmentAccumulator --> CommitmentAccumulatorInstance
    NullifierSet --> NullifierSetInstance

    List --> ListInstance
    Set --> SetInstance

    style SetInstance fill:transparent
    style ListInstance fill:transparent
    style MapInstance fill:transparent
    style CommitmentAccumulatorInstance fill:transparent
    style NullifierSetInstance fill:transparent


    ProvingSystem --> ComplianceProvingSystem
    ProvingSystem --> ResourceLogicProvingSystem
    ProvingSystem --> IDeltaProvingSystem
    IDeltaProvingSystem --> DeltaProvingSystem
    style ComplianceProvingSystem fill:transparent
    style ResourceLogicProvingSystem fill:transparent
    style DeltaProvingSystem fill:transparent
```
<figcaption>Primitive interfaces</figcaption>

</figure>


<figure markdown>

```mermaid
flowchart LR

    FixedSize --> Arithmetic
    FixedSize --> Hash


    FixedSize --> Nonce
    FixedSize --> RandSeed
    FixedSize --> NullifierKeyCommitment
    FixedSize --> NullifierKey

    style Nonce fill:transparent
    style RandSeed fill:transparent
    style NullifierKey fill:transparent
    style NullifierKeyCommitment fill:transparent


    Arithmetic --> Quantity
    Arithmetic --> Balance

    Arithmetic --> DeltaHash

    style Quantity fill:transparent
    style Balance fill:transparent
    style DeltaHash fill:transparent


    Hash --> PS\.VerifyingKey
    Hash --> LabelHash
    Hash --> ValueHash
    Hash --> DeltaHash

    Hash --> Commitment
    Hash --> Nullifier
    Hash --> Kind
    Hash --> LogicVKOuterHash
    Hash --> MerkleTreeNodeHash

    style LogicVKCompact fill:transparent
    style LabelHash fill:transparent
    style ValueHash fill:transparent
    style DeltaHash fill:transparent
    style Commitment fill:transparent
    style Nullifier fill:transparent
    style Kind fill:transparent
    style LogicVKOuterHash fill:transparent
    style MerkleTreeNodeHash fill:transparent


    Hash --> AppDataValueHash
    style AppDataValueHash fill:transparent
```
<figcaption>Primitive types</figcaption>

</figure>
