---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - resource-machine
  - protocol
  - commitment
  - nullifier
  - accumulator
  - resource logic
---

```juvix
module arch.system.state.resource_machine_03.index;
```

# Introduction

![Alt text](./dag.svg)
<img src="./arch/system/state/resource_machine_03/dag.svg">

```kroki-plantuml
@from_file:./arch/system/state/resource_machine_03/dag.puml
```

```kroki-plantuml
@startuml
Bob -> Alice : [[https://research.anoma.net Forums]]
@enduml
```


<!--
**The Anoma Resource Machine (ARM)** is the part of the Anoma protocol that defines and enforces the rules for valid state updates that satisfy users' preferences. The new proposed state is then agreed on by the consensus participants. In that sense the role of the Anoma Resource Machine in the Anoma protocol is similar to the role of the Ethereum Virtual Machine in the Ethereum protocol.

## Data structures

The atomic unit of the ARM state is called a [[Resource | **resource**]]. Resources are immutable, they can be created once and consumed once. The system state is represented by the set of active resources: the resources that were created but not nullified.

[[Transaction | **Transactions**]] produced by the ARM represent the proposed state update. They consist of [[Action|**actions**]], which group resources with the same execution context.

Ensuring the correctness of the transaction is achieved with the help of non-interactive proofs attached to it:

1. to prove the transaction is balanced correctly, there are [[Delta proof | delta proofs]]. Balance is the criterion of a transaction's completeness.
2. to prove the transaction complies with the ARM rules, there are [[Compliance proof | compliance proofs]]. Actions are partitioned into [[Compliance unit | compliance units]] that define the compliance proof scope.
3. to prove the transaction satisfies the user constraints, there are [[Resource logic proof | resource logic proofs]].


![Proof contexts associated with data structures](proof_contexts.svg)


## The role of the ARM

The ARM is used to create, compose, and verify transactions. It is stateless and run by every node that processes transactions. Anoma users submit their intents to the intent gossip network in the form of unbalanced ARM transactions with metadata, which are received and processed by solvers that output balanced ARM transactions. These transactions are then ordered and finally sent to the executor node, that verifies and executes the transactions in the determined order, updating the global state.

## The specification

This specification describes a common interface shared by all ARM instantiations. Depending on the primitive instantiation choices, the resulting ARM instantiation will have different properties. For example, using zk-SNARKs to create and verify the ARM proofs might result in a succinct or even shielded ARM instantiation. The ARM interface is designed to provide interoperability between different ARM instantiations.

The design of the Anoma Resource Machine was significantly inspired by the [Zcash protocol](https://zips.z.cash/protocol/protocol.pdf).

- Keywords: anoma, blockchain technology, protocol design, resource machine
-->
