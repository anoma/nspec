---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- executor-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.executor_2_environment;
    import prelude open;
    import arch.node.engines.executor_2_messages open;
    import arch.node.engines.shard_2_messages as Shard;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Executor Environment

## Overview

The executor environment maintains state needed to execute transactions, including the current transaction being processed and values read from shards.

## Mailbox states

```juvix
syntax alias ExecutorMailboxState := Unit;
```

The executor engine does not require complex mailbox states. Therefore, we define the mailbox state type as `Unit`.

## Local state

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:ExecutionData] -->
    ```juvix
    type PendingReads := mkPendingReads {
      reads : Map Shard.KVSKey KVSDatum
    };

    type TransactionState := mkTransactionState {
      executable : TransactionExecutable;
      label : TransactionLabel;
      timestamp : TxFingerprint;
      curator : EngineID;
      issuer : EngineID;
      pending : PendingReads
    };
    ```
    <!-- --8<-- [end:ExecutionData] -->

### `ExecutorLocalState`

<!-- --8<-- [start:ExecutorLocalState] -->
```juvix
type ExecutorLocalState := mkExecutorLocalState {
  currentTransaction : Option TransactionState
};
```
<!-- --8<-- [end:ExecutorLocalState] -->

???+ quote "Arguments"

    `currentTransaction`
    : The currently executing transaction and its state, if any

## Timer handles

```juvix
syntax alias ExecutorTimerHandle := Unit;
```

The executor engine does not require timers. Therefore, we define the timer handle type as `Unit`.

## The Executor Environment

### `ExecutorEnv`

<!-- --8<-- [start:ExecutorEnv] -->
```juvix
ExecutorEnv : Type :=
  EngineEnv
    ExecutorLocalState
    ExecutorMailboxState
    ExecutorTimerHandle
    ExecutorMsg;
```
<!-- --8<-- [end:ExecutorEnv] -->

#### Instantiation

<!-- --8<-- [start:executorEnv] -->
```juvix extract-module-statements
module executor_environment_example;

  executorEnv : ExecutorEnv :=
    mkEngineEnv@{
      localState := mkExecutorLocalState@{
        currentTransaction := none
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:executorEnv] -->