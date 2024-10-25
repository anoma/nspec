# Proving system

The resource machine differentiates between three kinds of proofs, each of which can have a distinct proving system used to produce that sort of proofs

||Execution context|Constraints defined by|Are the constraints public by default?|Description
|-|-|-|-|-|
|Resource logic proof|Action|Application|No|Action is compliant with the application constraints|
|Compliance proof|Compliance unit|Resource machine instance|Yes|Action (partitioned in compliance units) is compliant with the RM rules|
|Delta proof|Transaction|Resource machine interface|Yes|Transaction is balanced|

TODO: add some thoughts about compliance and RL proving systems

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