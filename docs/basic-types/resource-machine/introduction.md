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
hide:
- toc
---

# Introduction

**The Anoma Resource Machine (ARM)** is the part of the Anoma protocol that defines and enforces the rules for valid state updates that satisfy users' preferences. The new proposed state is then agreed on by the consensus participants. In that sense the role of the Anoma Resource Machine in the Anoma protocol is similar to the role of the Ethereum Virtual Machine in the Ethereum protocol.

The atomic unit of the ARM state is called a **resource**. Resources are immutable, they can be created once and consumed once, which indicates that the system state has been updated.

## Resource model

The ARM transaction model is neither the account nor UTXO model. Unlike the Bitcoin UTXO model, which sees UTXOs as currency units and is limited in expressivity, the resource model is generalised and provides flexibility — resource logics — programmable predicates associated with each resource — can be defined in a way to construct applications that operate in any desired transaction model, including the account and UTXO models. 

For example, a token operating in the account model would be represented by a single resource containing a map $user: balance$ (unlike the UTXO model, where the token would be represented by a collection of resources of the token type, each of which would correspond to a portion of the token total supply and belong to some user owning this portion). Only one resource of that kind can exist at a time. When users want to perform a transfer, they consume the old balance table resource and produce a new balance table resource.

## Properties

The Anoma Resource Machine has the following properties:

- _Atomic state transitions of unspecified complexity_ — the number of resources created and consumed in every atomic state transition is not bounded by the system.
- _Information flow control_ — the users of the system can decide how much of the information about their state to reveal and to whom. From the resource machine perspective, states with different visibility settings are treated equally (e.g., there is no difference between transparent — visible to anyone — and shielded — visible only to the parties holding the viewing keys — resources), but the amount of information revealed about the states differs. It is realised with the help of _shielded execution_, in which the state transition is only visible to the parties involved.
- _Account abstraction_ — each resource is controlled by a **resource logic** — a custom predicate that encodes constraints on valid state transitions for that kind of resource and determines when a resource can be created or consumed. A valid state transition requires a resource logic validity proof for every resource created or consumed in the proposed state transition.
- _Intent-centric architecture_ — the ARM provides means to express intents and ensures their correct and complete fulfilment and settlement.



The design of the Anoma Resource Machine was significantly inspired by the [Zcash protocol](https://zips.z.cash/protocol/protocol.pdf).

The rest of the document contains the definitions of the ARM building blocks and the necessary and sufficient requirements to build the Anoma Resource Machine.

- [10.5281/zenodo.10498991](https://doi.org/10.5281/zenodo.10498991)
- [ART Index](https://art.anoma.net/list#paper-10498991)

## Notation

For a function $h$, we denote the output finite field of $h$ as $\mathbb{F}_h$. If a function $h$ is used to derive a component $x$, we refer to the function as $h_x$, and the corresponding to $h$ finite field is denoted as $\mathbb{F}_{h_x}$, or, for simplicity, $\mathbb{F}_x$.

- Keywords: anoma, blockchain technology, protocol design, resource machine