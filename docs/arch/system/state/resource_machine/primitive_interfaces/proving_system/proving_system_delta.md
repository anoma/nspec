# Delta Proving System

Delta proving system is used to prove that the transaction delta is equal to a certain value. To support transaction composition that results in a new transaction being produced, the delta proving system must, in addition to the standard proving system interface, provide a *proof aggregation function*:
<!--ᚦ«wikilink to transaction delta desirable»-->
<!--ᚦ«
", in addition to the standard proving system interface, provide a *proof aggregation function*"
→
"extends the [[Proving system|proving system interface]] with method *aggregate* that aggregates delta proofs of two transactions."
»-->

`DeltaProvingSystem`:

1. `prove(PS.ProvingKey, PS.Instance, PS.Witness) -> PS.Proof`
2. `verify(PS.VerifyingKey, PS.Instance, PS.Proof) -> Bool`
3. `aggregate(PS.Proof, PS.Proof) -> PS.Proof`<!--ᚦ«to double check: proof aggregation does not need any of the ProvingKey, Instance or Witnesses?»-->

The aggregation function allows to aggregate proofs in a way that if $\pi_1$ proves that the first transaction's balance is $b_1$ and the second proof $\pi_2$ proves the second transaction's balance is $b_2$, then the proof $Aggregate(\pi_1, \pi_2)$ proves that the composed transaction's balance is $b_1 + b_2$.
<!--ᚦ«This should be including kind distinctness.»-->

The diagram below describes the relationship between the [[Proof|basic_abstractions/proving/proof.md]] interface and the delta proving system interface.
<!--ᚦ«This sentence seems not to fit the picture»-->

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
<!--ᚦtags:reviewed,consistent,nits-->
