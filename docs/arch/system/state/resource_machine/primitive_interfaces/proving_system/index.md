---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Proving system

!!! todo

    add efficiency expectations (what to prioritise)

The resource machine differentiates between three kinds of proofs, each of which can have a distinct [[Proof|proving system]] used to produce that sort of proofs:

1. resource logic proofs
2. compliance proofs
3. delta proofs

||Execution context|Constraints defined by|Are the constraints public by default?|Meaning
|-|-|-|-|-|
|Resource logic proof|[[Action]]|Application|No|Action is compliant with the application constraints|
|Compliance proof|[[Compliance unit]]|RM instance|Yes|Action (partitioned into compliance units) is compliant with the RM rules|
|Delta proof|[[Transaction]]|RM interface|Yes|Transaction is balanced|

Every proof has three types of inputs and constraints:

1. *Architecture-level* inputs and constraints. This type of inputs and constraints allow to enforce certain resource machine properties and have to be present in each resource logic, no matter in the context of which instantiation and application the resource logic was produced. These contraints ensure basic resource machine properties.
2. *Instantiation-level* inputs and constraints. These inputs and constraints must be present in every resource logic compatible with a concrete resource machine instantiation but might not be required by other instantiations. These constraints ensure additional resource machine properties desired by the instantiation.
3. *Application-level* (custom) inputs and constraints that are present in every resource logic specified by a concrete application. These constraints define how the application works.

This specification explicitly defines only the architecture-level inputs and constraints. Only application-level constraints are referred to as custom.

## Proving system requirements

The first two kinds of proofs, resource logic proofs and compliance proofs,
follow the standard proving system interface defined [[Proof|here]]. The delta
proof has an additional functionality required and is further described
[[Delta proving system|here]].

### Resource logic proving system choice

Resource logic proof is the most common proof type. Each [[Action | action]] that modifies the state of `n` resources (creates or consumes) has at least `n` resource logic proofs attached to it. In principle, the predicate checked with each proof can be different for all `n` proofs. For that reason, the proving system of choice should support easy proof instantiation process for new predicates (e.g., a SNARK that requires a trusted setup ceremony initiated for every predicate is probably not the most efficient choice for this proving system).

### Compliance proving system choice

Compliance constraints are fixed per RM instantiation, meaning that the predicate being checked is the same for each compliance unit, with only the instance and witness being different each time. For that reason, a proving system that prioritises efficiency for a single predicate over the ease of creating proofs for new predicates might be more suitable.

## Proving system hierarchy

The diagram below describes the relationships between the proving system and delta proof interfaces and their instantiations that correspond to the proving system for each proof type.

``` mermaid
---
title: Proving System hierarchy
---
classDiagram
    class IProvingSystem~VerifyingKey, ProvingKey, Instance, Witness, Proof~ {
         <<Interface>>
         +prove(ProvingKey, Instance, Witness) Proof
         +verify(VerifyingKey, Instance, Proof) Bool
    }

    IProvingSystem <|-- ResourceLogicProvingSystem
    IProvingSystem <|-- ComplianceProvingSystem
    IProvingSystem <|-- IDeltaProvingSystem

    class ResourceLogicProvingSystem
    class ComplianceProvingSystem

    class IDeltaProvingSystem~VerifyingKey, ProvingKey, Instance, Witness, Proof~ {
         <<Interface>>
        +aggregate(Proof, Proof) Proof
    }
    IDeltaProvingSystem <|-- DeltaProvingSystem

    class DeltaProvingSystem

```