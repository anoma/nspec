# Hash

binding, collision resistant

for shielded: cryptographic hash, hiding

TODO: do we want a separate interface for the logic hash, given it is a verifier key?

## Hash interface diagram
---
title: Hash hierarchy
---

classDiagram
    class IHash~T, U~ {
         <<Interface>>
         +hash(T) U
    }

    IHash <|-- LogicHash
    IHash <|-- LabelHash
    IHash <|-- ValueHash

    IHash <|-- CommitmentHash
    IHash <|-- NullifierHash
    IHash <|-- KindHash
    IHash <|-- IDeltaHash

    class IDeltaHash~T, U~ {
        <<Interface>>
        +add(U, U) U
        +sub(U, U) U
    }

    IDeltaHash <|-- DeltaHash
