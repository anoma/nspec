# Delta Proving System

Delta proving system is used to prove that the transaction delta is equal to a certain value. To support transaction composition that results in a new transaction being produced, the delta proving system must, in addition to the standard proving system interface, provide a *proof aggregation function*: 

`DeltaProvingSystem`:

- `prove(PS.ProvingKey, PS.Instance, PS.Witness) -> PS.Proof`
- `verify(PS.VerifyingKey, PS.Instance, PS.Proof) -> Bool`
- `aggregate(PS.Proof, PS.Proof) -> PS.Proof`

The aggregation function allows to aggregate proofs in a way that if $\pi_1$ proves that the first transaction's balance is $b_1$ and the second proof $\pi_2$ proves the second transaction's balance is $b_2$, then the proof $Aggregate(\pi_1, \pi_2)$ proves that the composed transaction's balance is $b_1 + b_2$.

>For $bv_1$ being the balancing value of the first delta proof, $bv_2$ being the balancing value of the second delta proof, and $bv_{tx}$ being the balancing value of the composed delta proof, it satisfies $bv_{tx} = bv_1 + bv_2$. The aggregation function takes two delta proofs as input and outputs a delta proof. The aggregation function is defined by the proving system and might require creation of a new proof.

The diagram below describes the relationship between the [standard proving system](./../../../../../basic_abstractions/proving/proof.md) interface and the delta proving system interface.

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

    IProvingSystem <|-- IDeltaProvingSystem

    class IDeltaProvingSystem~VerifyingKey, ProvingKey, Instance, Witness, Proof~ {
         <<Interface>>
        +aggregate(Proof, Proof) Proof
    }
    IDeltaProvingSystem <|-- DeltaProvingSystem

    class DeltaProvingSystem

```