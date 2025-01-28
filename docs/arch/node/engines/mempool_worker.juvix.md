---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- mempool-worker-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.mempool_worker;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.mempool_worker_config open public;
    import arch.node.engines.mempool_worker_messages open public;
    import arch.node.engines.mempool_worker_environment open public;
    import arch.node.engines.mempool_worker_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open mempool_worker_config_example;
    open mempool_worker_environment_example;
    ```

# Mempool Worker Engine

The Mempool Worker Engine serves as a transaction coordinator in Anoma, managing
the critical process of ordering transactions and orchestrating their execution.
Think of it as a traffic controller that not only assigns each transaction a unique
position in line (via a timestamp called a *TxFingerprint*), but also ensures all the
necessary resources (state access) are locked and ready before execution begins. In
the current version of Anoma (V2), there is only a single Mempool Worker Engine
instance, making it the central coordinator for all transaction processing.

When users or solvers submit transactions (via `MempoolWorkerMsgTransactionRequest`),
the Worker examines the transaction's label to understand what state it may need to
access - which keys it may read from and/or write to. It assigns each transaction a
unique fingerprint (called a `timestamp`) that establishes its position in the
execution order, and returns an acknowledgment (`MempoolWorkerMsgTransactionAck`)
to the submitter. This acknowledgment includes a signature over the transaction
hash and metadata, providing proof of acceptance into the processing pipeline.

The Worker's core responsibility is managing a sophisticated locking protocol that
ensures transactions can execute safely and efficiently. For each transaction, it
sends `KVSAcquireLock` messages to all Shards that manage keys the transaction
needs to access. These locks specify which keys will definitely be read
(`eager_read_keys`), which might be read (`lazy_read_keys`), which will definitely
be written (`will_write_keys`), and which might be written (`may_write_keys`).
The Shards respond with `KVSLockAcquired` messages once they've recorded these
access intentions.

A crucial part of the Worker's job is tracking the "seen-all" points - timestamps
before which all Shards have processed all relevant lock requests. It maintains two
such points: `seen_all_writes` for write locks and `seen_all_reads` for read locks.
When Shards confirm lock acquisition, the Worker updates these points and
broadcasts them to all Shards via `UpdateSeenAll` messages. This information is
vital for the Shards to know when they can safely process read requests and perform
state updates, as it guarantees no earlier lock requests are still pending.

For each transaction, the Worker spawns an Executor Engine (configured with the
transaction's program and access rights) and maintains a mapping between Executors
and their transactions. As Executors complete their work, they notify the Worker
via `ExecutorMsgExecutorFinished` messages containing summaries of what was read
and written. The Worker collects these execution summaries, maintaining a record
of transaction processing outcomes.

The Mempool Worker's state tracks pending transactions and their corresponding
Executors, maintains the mapping of transactions to their fingerprints,
collects lock acquisition confirmations, tracks the seen-all barriers, and stores
execution summaries. This state allows it to provide the ordering and
coordination services needed for Anoma's parallel execution model, where multiple
transactions can process simultaneously so long as their state access patterns
don't conflict, ensuring (serializability)[https://en.wikipedia.org/wiki/Database_transaction_schedule#Serializable]..

## Purpose

Workers are one of the [[Mempool Engines#mempool-engines|mempool engines]]
and, in V2, they are _the_ only one and there is only a single worker.

The worker receives transaction requests from users and
[[Solver#solver|solvers]] and batches these transaction requests, assigning a
unique [[TxFingerprint#txfingerprint|TxFingerprint]] to every new transaction.
Each transaction candidate will be sent to an [[Executor#executor|Executor]]
inside an [[ExecuteTransaction#executetransaction|ExecuteTransaction]] message.
Once the worker has received a [[KVSLockAcquired]] for every part of the
transaction request's label (from the shards of the same Anoma validator in
response to [[KVSAcquireLock]]-messages), it knows that this transaction
candidate has been _"seen"_ by all [[Shard#shard|Shards]], which implies that
all shards are prepared to process lock requests from execution processes (see
[[KVSReadRequest]] and [[KVSWrite]] for details). This information about locks
being recorded is distributed to all [[Shard#shard|shards]] via
[[UpdateSeenAll#updateseenall|UpdateSeenAll]] messages, which contain the most
recent [[TxFingerprint#txfingerprint|TxFingerprint]] for which it is certain
that _all_ [[Shard#shard|Shards]] have _"seen"_ this transaction candidate and
all previous ones from the same worker (and they are thus prepared to grant
locks). Note that if [[Shard#shard|shards]] receive transaction candidates in a
different order than the final total order of transactions,
[[UpdateSeenAll#updateseenall|UpdateSeenAll]] messages are necessary to avoid
that [[Shard#shard|shards]] grant locks before all locks of previous transaction
executions have been served.

Workers also are in charge of collecting and curating logs of transaction
execution. Success is equivalent to all reads and writes being successful and an
[[ExecutorFinished]]-message from the [[Executor#executor|executor]] that was
spawned to execute the message.

## Engine components

- [[Mempool Worker Messages]]
- [[Mempool Worker Configuration]]
- [[Mempool Worker Environment]]
- [[Mempool Worker Behaviour]]

## The type for a mempool worker engine

<!-- --8<-- [start:MempoolWorkerEngine] -->
```juvix
MempoolWorkerEngine (KVSKey KVSDatum Executable ProgramState : Type) : Type :=
  Engine
    MempoolWorkerCfg
    (MempoolWorkerLocalState KVSKey KVSDatum Executable)
    MempoolWorkerMailboxState
    MempoolWorkerTimerHandle
    MempoolWorkerActionArguments
    (Anoma.PreMsg KVSKey KVSDatum Executable)
    (Anoma.PreCfg KVSKey KVSDatum Executable)
    (Anoma.PreEnv KVSKey KVSDatum Executable ProgramState);
```
<!-- --8<-- [end:MempoolWorkerEngine] -->

### Example of a mempool worker engine

<!-- --8<-- [start:exampleMempoolWorkerEngine] -->
```juvix
exampleMempoolWorkerEngine : MempoolWorkerEngine String String ByteString String :=
  mkEngine@{
    cfg := mempoolWorkerCfg;
    env := mempoolWorkerEnv;
    behaviour := mempoolWorkerBehaviour;
  };
```
<!-- --8<-- [start:exampleMempoolWorkerEngine] -->

where [[Mempool Worker Configuration#mempoolWorkerCfg|`mempoolWorkerCfg`]] is defined as follows:

--8<-- "./docs/arch/node/engines/mempool_worker_config.juvix.md:mempoolWorkerCfg"

where [[Mempool Worker Environment#mempoolWorkerEnv|`mempoolWorkerEnv`]] is defined as follows:

--8<-- "./docs/arch/node/engines/mempool_worker_environment.juvix.md:mempoolWorkerEnv"

and [[Mempool Worker Behaviour#mempoolWorkerBehaviour|`mempoolWorkerBehaviour`]] is defined as follows:

--8<-- "./docs/arch/node/engines/mempool_worker_behaviour.juvix.md:mempoolWorkerBehaviour"

