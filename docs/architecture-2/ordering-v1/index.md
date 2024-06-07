---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Ordering Machine

## Introduction

### Purpose

The ordering machine is a set of communicating engines that collaborate in

- receiving [[TransactionCandidate|transaction candidates]] from
  users or solvers

- [[Mempool Engines|ordering]] these requests for
  [[Execution Engines|execution]],

- [[Execution Engines|executing]] the
  [[TransactionCandidate|transaction candidates]],

- updated the [[Shard|state]] accordingly,

- making the state available.

### Background

<!-- we might just "require" no internal links in the background section -->
In full generality,
Anoma nodes form a [distributed system](
https://en.wikipedia.org/wiki/Distributed_computing)<!--
—consisting of a communicating set of ordering engines—
--> that implements a [transaction processing system](
    https://en.wikipedia.org/wiki/Transaction_processing_system) (TPS) and
a [replicated state machine](
    https://en.wikipedia.org/wiki/State_machine_replication) (RSM).
This state machine must represent all anoma state, including commitments and nullifiers.
The Ordering Machine, however, does not need to understand the full complexity of the anoma state: only that it can be represented as a Key Value Store, where [[TransactionCandidate|transaction candidates]] each read some (arbitrary) data from keys, and can write some (arbitrary) data to keys.
We outline the full requirements of the abstraction boundary with the State Machine in the [[Execution Engines]] page.

In V1,
the implementation is running on a single physical machine.
As a consequence the [consensus problem](
    https://en.wikipedia.org/wiki/Consensus_(computer_science)) is trivial.
Roughly,
in V1, we only have the machine that is going to be replicated from V2 onward.

**Scope**

We start by describing the overall structure of
the ordering machine while
the details of the protocol and the functionality of
the engines is described in the respective pages.
The collection of all engines of the [[Ordering Machine|ordering machine]] is
organized into three groups:

- [[Mempool Engines]];

- [[Consensus Engine]];

- [[Execution Engines]].

We mention the consensus engine,
because it is one of the most important components from V2 onward,
although it is not present in V1.

## Overview

[[TransactionRequest|Transaction requests]] trigger transaction processing.
[[User]]s or [[Solver]]s send [[TransactionRequest|transaction requests]]
to the ordering machine: more specifically,
to a [[Worker Engine|worker engine]].
The ordering machine will eventually order and execute
the [[TransactionCandidate|transaction candidates]] included in these requests.
Successfully processing a [[TransactionRequest|transaction request]] amounts to
invoking the [transition function](
https://en.wikipedia.org/wiki/State_machine_replication#State_machine)
of the RSM,
according to an agreed upon order
(determined by the [[Mempool Engines|mempool]]
in collaboration with [[Consensus Engine|consensus]]).
Typical transactions contain read and write operations to
a “global” key-value store representing the state of the RSM.
In general, transactions may have side effects besides state updates,
but these are not considered in V1.

!!! todo

    Are they ignored?
    Are ExecutionSummary and pub sub information of execution data side effects?

- The [[Mempool Engines|mempool engines]] are responsible for
  managing [[TxData|transaction data]],
  (pre-)processing them for consensus and execution.

- The trivial consensus problem is already implicitly solved
  by _the_ [[Worker Engine|worker]] in V1.

  - In V1, there is only one [[Worker Engine|worker]].
    There will be multiple (on each Node) in future versions.

- The [[Execution Engines|execution engines]] execute
  the transactions:

  - [[Shard]]s maintain the local copy of the global state (of the RSM),
    i.e., serve read and write requests of [[Executor]]s
    to the key-value store (of the RSM).

  - [[Executor]]s process [[TransactionCandidate|transaction candidates]], effectively
     invoking the [transition function
      ](https://en.wikipedia.org/wiki/State_machine_replication#State_machine)
      of the RSM.

![](ordering-v1.svg)

--8<-- "./ordering/a-complete-lifecycle.md:all"

[^1 time stamp]: In fact it is the latter time stamp that is most relevant;
    the former is merely an indicator about performance of the worker.

[^1]: This response may be delayed until the TxFingerprint is assigned.
    In V2,
    the "shuffling" of transactions may be pseudo-random
    so that we can quickly pass on transaction data to mirror workers.
