---
icon: material/order-alphabetical-ascending
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - ordering-subsystem
  - index
---

???+ code "Juvix imports"

  ```juvix
  module arch.node.subsystems.ordering;
  import arch.node.engines.executor open;
  import arch.node.engines.mempool_worker open;
  ```

# Ordering Subsystem

## Purpose

The *Ordering Subsystem* is responsible for ordering and executing `TransactionCandidate`s, and maintaining this node's replica of the [replicated state machine](https://en.wikipedia.org/wiki/State_machine_replication).
Although here were are primarily concerned with running the *anoma state machine*, The Ordering Subsystem is designed to be somewhat agnostic over exactly what replicated state machine it's running: this provides a useful abstraction barrier, as well as some reusability. 

## Background
The Ordering Subsystem maintains a [replicated state machine](https://en.wikipedia.org/wiki/State_machine_replication), which is a core concept of [distributed systems](https://en.wikipedia.org/wiki/Distributed_computing).
The architecture of the execution ([[Executor]]s) and data storage ([[Shard]]) components is based on of [_Calvin: Fast Distributed Transactions for Partitioned Database Systems_](http://cs.yale.edu/homes/thomson/publications/calvin-sigmod12.pdf), while the raw `TransactionCandidate` storage and ordering components ([[Worker]]s and [[Consensus]]) are based on [_Autobahn: Seamless high speed BFT_](https://arxiv.org/abs/2401.10369) and [Narwhal's]( https://arxiv.org/abs/2105.11827) scale-out architecture.
We aim to run transactions as concurrently as possible, while maintining [serializability]( https://en.wikipedia.org/wiki/Serializability), a key concept of [Transaction processing systems](https://en.wikipedia.org/wiki/Transaction_processing) and databases.
Chain [[Consensus]] ultimately determines a total order of transactions for each replicated state machine, so our replica can then run [deterministic execution scheduling](
https://www.cs.umd.edu/~abadi/papers/determinism-vldb10.pdf).

## The State Machine
A state machine can be characterized as having some datatype of `State`, some type of `TransactionCandidate`, and some function `update : State -> TransactionCandidate -> State` that produces a new state, given an old state and a transaction. 

The Ordering Subsystem makes a few additional assumptions, to improve parallelism:

1. The `State` of the replicated state machine is divided into `KVSKey`, `KVSDatum` pairs (with unique `KVSKeys`). The `KVSDatum` stored at each can be mutable.
   In principle, one could encode any state machine this way, putting its whole state under one `KVSKey`, but this would not enable much parralelism. 
2. Each `TransactionCandidate` includes a `Label`: a list of `KVSKey`s from which it may read and `KVSKey`s to which it may write. The new state differs from the old state only in the write `KVSKey`s, and the values at these write `KVSKey`s are determined _only_ from the values of the read `KVSKey`s and the `TransactionCandidate`. This allows us to compute updates in parallel whenever the `TransactionCandidate`s involved use different `KVSKeys` in their labels. 
3. `update` is deterministic and total: all replicas can run `update` on all `TransactionCandidates`, in order, and arrive at the same state. `update` may itself encode a notion of _gas_, or a notion of _transaction failure_ that doesn't change the state, but there is no special return value, and there are no `Exception`s.  

Note that `update` is allowed to have some _side effects_. 
It can, for instance, send messages over the network, so long as the success or failure of these messages does not affect the new state.
This is how we should encode consistent reads to state: they are `TransactionCandidate`s that read from state, send messages over the network, and update nothing. 

### Anoma

We detail in the [Anoma State Architecture ART Report](https://art.anoma.net/list.html#paper-14265827) how the anoma state machine's state may be divided into keys. 
The anoma `update` function must run as follows:

1. Perform _post-ordering execution_ in order to assemble and anoma `Transaction`, a set of blobs to be stored, and a set of messages to be sent over the network, (and posibly other side effects, but we haven't thought of any yet).
   This can involve reading from state (including data blobs).
   During _post-ordering execution_, any _aborts_ or failures or attempts to read outside the `TransactionCandidate`'s label should result in `update` returning the unchanged, input state. 
2. Verify all the proofs for all the resource logics of all the resources in the anoma `Transaction`. If any fail (or run out of gas or whatever), return the unchanged, input state. 
3. Send all the messages, and then return a new state with all the blobs, nullifiers, and commitments written. 

Periodically, the anoma state machine should run special transactions, to do things like assemble commitment roots, and establish checkpoints. 

