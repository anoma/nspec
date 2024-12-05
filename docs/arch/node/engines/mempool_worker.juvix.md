---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- mempool
- mempool-worker
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.mempool_worker;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.mempool_worker_messages open public;
    import arch.node.engines.mempool_worker_environment open public;
    import arch.node.engines.mempool_worker_behaviour open public;
    ```

# Mempool Worker

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
## Components

- [[Worker Messages]]
- [[Worker Environment]]
- [[Worker Behaviour]]

## Type

<!-- --8<-- [start:MempoolWorkerEngine] -->
```juvix
MempoolWorkerEngine : Type := Engine
  MempoolWorkerLocalState
  MempoolWorkerMailboxState
  MempoolWorkerTimerHandle
  MempoolWorkerMatchableArgument
  MempoolWorkerActionLabel
  MempoolWorkerPrecomputation;
```
<!-- --8<-- [end:MempoolWorkerEngine] -->

### Example of a mempool worker engine

<!-- --8<-- [start:exampleMempoolWorkerEngine] -->
```juvix
exampleMempoolWorkerEngine : MempoolWorkerEngine := mkEngine@{
    name := "mempool_worker";
    initEnv := commitmentEnvironment;
    behaviour := mempoolWorkerBehaviour;
  };
```
<!-- --8<-- [end:exampleMempoolWorkerEngine] -->

where `mempoolWorkerEnvironment` is defined as follows:

--8<-- "./docs/arch/node/engines/mempool_worker_environment.juvix.md:mempoolWorkerEnvironment"

and `mempoolWorkerBehaviour` is defined as follows:

!!! todo
    Figure out what it means to define behaviour and put it here