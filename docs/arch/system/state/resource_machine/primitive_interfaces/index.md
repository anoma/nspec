# Primitive interfaces

This section defines the hierarchy of primitives used in resource machine design and describes interfaces for each primitive. Each primitive has an associated type, e.g. hash primitive has type `Hash`. 

The diagram below illustrates the primitive types required for resource machine. Green nodes correspond to the primitives for which only one instantiation is required, e.g., we only need to instantiate `DeltaHash` type once for a given RM implementation and use it everywhere where `DeltaHash` is expected. It is assumed for such types that there is a unique function used to derive elements of the type. The name of this function is derived from the type name, written in lower camel case, e.g., for `DeltaHash` the corresponding derivation function would be `deltaHash(..)`.


``` mermaid

flowchart TB
    ProvingSystem
    Set
    List
    Map
    CommitmentAccumulator
    NullifierSet
    FixedSize

    style Set fill:#ddf2d1
    style List fill:#ddf2d1
    style Map fill:#ddf2d1
    style CommitmentAccumulator fill:#ddf2d1
    style NullifierSet fill:#ddf2d1


    ProvingSystem --> ComplianceProvingSystem
    ProvingSystem --> ResourceLogicProvingSystem
    ProvingSystem --> IDeltaProvingSystem
    IDeltaProvingSystem --> DeltaProvingSystem
    style ComplianceProvingSystem fill:#ddf2d1
    style ResourceLogicProvingSystem fill:#ddf2d1
    style DeltaProvingSystem fill:#ddf2d1


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