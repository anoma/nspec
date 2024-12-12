---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Primitive interfaces

This section defines the hierarchy of primitives used in resource machine design and describes interfaces for each primitive.

The diagram below illustrates the primitive types required for resource machine. Red nodes correspond to primitive interfaces, green nodes correspond to instantiations of the interfaces. Each primitive instantiation has an associated type, e.g. delta hash instantiation of `Hash` interface has an associated type `DeltaHash`. Primitive instantiations' names are derived from the type name but written in lower camel case, e.g., for `DeltaHash` the corresponding function would be `deltaHash(..)`.


``` mermaid

flowchart TB
    ProvingSystem
    Set --> OrderedSet
    Map --> MapInstance
    CommitmentAccumulator --> CommitmentAccumulatorInstance
    NullifierSet --> NullifierSetInstance

    OrderedSet --> OrderedSetInstance
    Set --> SetInstance

    style SetInstance fill:#ddf2d1
    style OrderedSetInstance fill:#ddf2d1
    style MapInstance fill:#ddf2d1
    style CommitmentAccumulatorInstance fill:#ddf2d1
    style NullifierSetInstance fill:#ddf2d1


    ProvingSystem --> ComplianceProvingSystem
    ProvingSystem --> ResourceLogicProvingSystem
    ProvingSystem --> IDeltaProvingSystem
    IDeltaProvingSystem --> DeltaProvingSystem
    style ComplianceProvingSystem fill:#ddf2d1
    style ResourceLogicProvingSystem fill:#ddf2d1
    style DeltaProvingSystem fill:#ddf2d1
```

``` mermaid

flowchart TB

    FixedSize --> Arithmetic
    FixedSize --> Hash


    FixedSize --> Nonce
    FixedSize --> RandSeed
    FixedSize --> NullifierKeyCommitment
    FixedSize --> NullifierKey

    style Nonce fill:#ddf2d1
    style RandSeed fill:#ddf2d1
    style NullifierKey fill:#ddf2d1
    style NullifierKeyCommitment fill:#ddf2d1


    Arithmetic --> Quantity
    Arithmetic --> Balance

    Arithmetic --> DeltaHash

    style Quantity fill:#ddf2d1
    style Balance fill:#ddf2d1
    style DeltaHash fill:#ddf2d1


    Hash --> LogicHash
    Hash --> LabelHash
    Hash --> ValueHash
    Hash --> DeltaHash

    Hash --> Commitment
    Hash --> Nullifier
    Hash --> Kind
    Hash --> LogicRefHash
    Hash --> MerkleTreeNodeHash

    style LogicHash fill:#ddf2d1
    style LabelHash fill:#ddf2d1
    style ValueHash fill:#ddf2d1
    style DeltaHash fill:#ddf2d1
    style Commitment fill:#ddf2d1
    style Nullifier fill:#ddf2d1
    style Kind fill:#ddf2d1
    style LogicRefHash fill:#ddf2d1
    style MerkleTreeNodeHash fill:#ddf2d1


    Hash --> AppDataValueHash
    style AppDataValueHash fill:#ddf2d1

```