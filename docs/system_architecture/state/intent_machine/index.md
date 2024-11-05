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

**The Intent Machine** is an abstraction describing the process of counterparty discovery and settlement in the Anoma protocol. Intent machines take sets of intents, search for possible valid and balanced transactions, and select [transactions](../resource_machine/transaction.md) to actually execute. An abstract description can be found in the following report:

- [Zenodo](https://zenodo.org/records/10654543)
- [ART Index](https://art.anoma.net/list.html#paper-10654543)

## Intents
In the abstract, an intent is an expression of preference by an agent over future states of the system. Concretely, intents define which of the [resources](../resource_machine/index.md) owned by an agent they offer for consumption, and which they desire to be created, in a transaction.

## Solving
The way that balanced transactions are derived from sets of intents is called solving. The act of solving involves aggregation of intents, as well as matching sets of intents, s.t. the resources to be consumed and created encoded in the intents of this set are balanced.

## Data Format
### Intent
An intent is represented in Anoma as a (potentially unbalanced) [transaction](../resource_machine/transaction.md). Some intents contain ephemeral resources, the [[resource:Definition|resource logic]] of which encodes the constraints for the intent. Other intents can express their unfulfilled constraints solely by means of unbalanced parts of the delta term.

## Solver Interface
Solvers receive sets of unbalanced transactions from agents, run matching algorithms of their choice over them, and return balanced transactions, which are sent to the [execution engine](../../arch/node/ordering/execution/index.md).
