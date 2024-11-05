# Hash

Hash type is defined as a fixed size type that is *binding*, meaning that if the input value of type `Arg` changed, the output value would change as well.

!!! warning
    TODO:

    - for shielded: cryptographic hash, hiding
    - do we want a separate interface for the logic hash, given it is a verifier key? UPD in Taiga we had the verifier key hashed. Is it fixed size? If not, what was the reason for tripple hashing? vk + hash + function privacy commitment

### LogicHash

In the case of resource logic, the hash used to compute it should output the logic's verifying key and therefore is determined by the proving system used to compute resource logic proofs.

## Hash interface diagram

```mermaid

classDiagram

    class Hash~T, Arg~ {
         <<Interface>>
    }

    Hash <|-- LogicHash
    Hash <|-- LabelHash
    Hash <|-- ValueHash

    Hash <|-- Commitment
    Hash <|-- Nullifier
    Hash <|-- Kind
    Hash <|-- DeltaHash
    Hash <|-- LogicRefHash

    Hash <|-- AppDataValueHash

```

#Used in
- Resource components (logic, label, value)
- Resource computable components (cm, nf, kind, delta)