---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - intent-machine
  - intent
  - solver
  - protocol
  hide:
- toc
---

# Intent Machine
## Introduction

**The Intent Machine** is responsible for counterparty discovery in the anoma protocol. It creates executable [transactions](../resource_machine/transaction.md) from sets of intents. An abstract description can be found in the following report:

- [Zenodo](https://zenodo.org/records/10654543)
- [ART Index](https://art.anoma.net/list.html#paper-10654543)

## Intents
In the abstract, an intent is an expression of preferences over future states of the system by an agent. Concretely, intents define which of the [resources](../resource_machine/index.md) owned by an agent they offer for consumption, and which they desire to be created, in a transaction.

## Solving
The way that balanced transactions are derived from sets of intents is called solving. The act of solving involves aggregation of intents, as well as matching sets of intents, s.t. the resources to be consumed and created encoded in the intents of this set are balanced.

## Data Format
### Intent
An intent is represented in anoma as a, potentially unbalanced, [transaction](../resource_machine/transaction.md). It contains an ephemeral resource, the [resource logic](../resource_machine/resource/definition.md) of which encodes the constraints for the intent.

## Solver Interface
Solvers receive sets of unbalanced transactions from agents, run matching algorithms of their choice over them, and return balanced transactions, which are sent to the [execution engine](../../node_architecture/ordering/execution/index.md).