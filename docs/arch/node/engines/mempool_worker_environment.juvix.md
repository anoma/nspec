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
    import arch.node.engines.mempool_worker_messages open;
    import arch.node.types.engine_environment open;
    ```

# Mempool Worker Environment

## Overview
The local state each worker (in v0.2.0 and below there is only 1) tracks the ``in progress'' transaction candidates as they are executed.

- the current batch number (consecutively numbered)

- the list of [[TransactionCandidate|transaction candidate|]]s in each batch

- a unique [[TxFingerprint]] for each transaction candidate,
  at least in previous batches

- the set of relevant received [[KVSLockAcquired]]-acquired messages

- the set of relevant sent [[UpdateSeenAll]]-messages

- [[ExecutionSummary|execution summaries]] for each transaction

## Mailbox states
!!! todo
    Figure out what a mailbox state is, what makes it special, and if we're just using Unit.

The Mempool Worker Engine does not require complex mailbox states.
We define the mailbox state as `Unit`.

### `MempoolWorkerMailboxState`

```juvix
syntax alias MempoolWorkerMailboxState := Unit;
```

## Local state
Each worker (in v0.2.0 and below there is only 1) keeps track of
- the current batch number (consecutively numbered)

- the list of [[TransactionCandidate|transaction candidate|]]s in each batch

- a unique [[TxFingerprint]] for each transaction candidate,
  at least in previous batches

- the set of relevant received [[KVSLockAcquired]]-acquired messages

- the set of relevant sent [[UpdateSeenAll]]-messages

- [[ExecutionSummary|execution summaries]] for each transaction

### `MempoolWorkerLocalState`
!!! todo
    using the below template from commitment, write the local state for a mempool worker (including the stuff in the list above)

```juvix
type MempoolWorkerLocalState := mkMempoolWorkerLocalState@{
  signer : Unit;
  backend : Unit;
};
```

???+ quote "Arguments"

    `signer`:
    : The signer for the identity.

    `backend`:
    : The backend to use for signing.

## Timer Handle
!!! todo
    figure out what a Timer Handle is, and if a mempool worker needs one.

The Mempool Worker Engine does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

### `MempoolWorkerTimerHandle`

```juvix
syntax alias MempoolWorkerTimerHandle := Unit;
```

## The Mempool Worker Environment

### `MempoolWorkerEnvironment`

```juvix
MempoolWorkerEnvironment : Type :=
  EngineEnvironment
    MempoolWorkerLocalState
    MempoolWorkerMailboxState
    MempoolWorkerTimerHandle;
```

### Instantiation
!!! todo
    using the commitment engine template, create a (small) example worker

<!-- --8<-- [start:mempoolWorkerEnvironment] -->
```juvix extract-module-statements
module mempool_worker_environment_example;


mempoolWorkerEnvironment : MempoolWorkerEnvironment :=
    mkEngineEnvironment@{
      name := "mempool-worker";
      localState := mkMempoolWorkerLocalState@{
        signer := unit;
        backend := unit;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:mempoolWorkerEnvironment] -->
