---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- mempool
- mempool-worker
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.mempool_worker_environment;
    import prelude open;
    import arch.node.engines.shard_messages open;
    import arch.node.engines.executor_messages open;
    import arch.node.engines.mempool_worker_messages open;
    import arch.node.types.engine_environment open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Mempool Worker Environment

## Overview

The Mempool Worker engine's environment maintains the state necessary for managing transaction requests, including information about batches, transaction candidates, and the state of lock acquisition and execution.

## Local State

### `MempoolWorkerLocalState`

The local state of the Mempool Worker engine includes the following:

<!-- --8<-- [start:MempoolWorkerLocalState] -->
```juvix
type MempoolWorkerLocalState := mkMempoolWorkerLocalState {
  batch_number : BatchNumber;
  transactions : Map TxFingerprint TransactionCandidate;
  transactionEngines : Map EngineID TxFingerprint;
  locks_acquired : List (Pair EngineID KVSLockAcquiredMsg);
  seen_all_writes : TxFingerprint;
  seen_all_reads : TxFingerprint;
  execution_summaries : Map TxFingerprint ExecutorFinishedMsg;
  gensym : TxFingerprint
}
```
<!-- --8<-- [end:MempoolWorkerLocalState] -->

???+ quote "Arguments"

    `batch_number`:
    : The current batch number.

    `transactions`:
    : A map of transaction fingerprints to their corresponding transaction candidates.

    `locks_acquired`:
    : A list of relavant `KVSLockAcquiredMsg`s.

    `seen_all_writes`:
    : The highest transaction fingerprint for which all writes have been seen by the shards.

    `seen_all_reads`:
    : The highest transaction fingerprint for which all reads have been seen by the shards.

    `execution_summaries`:
    : A map of transaction fingerprints to their corresponding execution summaries.

    `gensym`:
    : A monotonically increasing number used to generate unique transaction numbers.

## Mailbox State

The Mempool Worker engine does not require a complex mailbox state, so we define it as a unit type:

### `MempoolWorkerMailboxState`

```juvix
syntax alias MempoolWorkerMailboxState := Unit;
```

## Timer Handle

The Mempool Worker engine does not require a timer handle, so we define it as a unit type:

### `MempoolWorkerTimerHandle`

```juvix
syntax alias MempoolWorkerTimerHandle := Unit;
```

## The Mempool Worker Environment

### `MempoolWorkerEnv`

```juvix
MempoolWorkerEnv : Type :=
  EngineEnv
    MempoolWorkerLocalState
    MempoolWorkerMailboxState
    MempoolWorkerTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:mempoolWorkerEnv] -->
```juvix extract-module-statements
module mempool_worker_environment_example;

  mempoolWorkerEnv : MempoolWorkerEnv :=
    mkEngineEnv@{
      localState := mkMempoolWorkerLocalState@{
        batch_number := 0;
        transactions := Map.empty;
        transactionEngines := Map.empty;
        locks_acquired := [];
        seen_all_writes := 0;
        seen_all_reads := 0;
        execution_summaries := Map.empty;
        gensym := 0
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:mempoolWorkerEnv] -->
