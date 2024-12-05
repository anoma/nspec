---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- shard-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.shard_environment;
    import prelude open;
    import arch.node.engines.shard_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Shard Environment

## Overview

The shard environment maintains state about key-value pairs, tracking read and write accesses for each key across different transaction timestamps. It provides multi-version concurrent storage capabilities.

## Mailbox states

```juvix
syntax alias ShardMailboxState := Unit;
```

The shard engine does not require complex mailbox states. Therefore, we define the mailbox state type as `Unit`.

## Local state

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:DAGStructure] -->
    ```juvix
    type ReadStatus := mkReadStatus {
      hasBeenRead : Bool;
      isEager : Bool;
      executor : EngineID
    };

    type WriteStatus : Type := mkWriteStatus {
      data : Option KVSDatum;
      mayWrite : Bool
    };

    type KeyAccess := mkKeyAccess {
      readStatus : Option ReadStatus;
      writeStatus : Option WriteStatus
    };

    type DAGStructure := mkDAGStructure {
      keyAccesses : Map KVSKey (Map TxFingerprint KeyAccess);
      heardAllReads : TxFingerprint;
      heardAllWrites : TxFingerprint
    };
    ```
    <!-- --8<-- [end:DAGStructure] -->

### `ShardLocalState`

<!-- --8<-- [start:ShardLocalState] -->
```juvix
type ShardLocalState := mkShardLocalState {
  dagStructure : DAGStructure;
  anchors : List NarwhalBlock
};
```
<!-- --8<-- [end:ShardLocalState] -->

???+ quote "Arguments"

    `dagStructure`
    : Structure tracking all key accesses across transactions, including read/write status and heardAllWrites point

    `anchors`
    : Sequence of consensus decisions

## Timer handles

```juvix
syntax alias ShardTimerHandle := Unit;
```

The shard engine does not require timers. Therefore, we define the timer handle type as `Unit`.

## The Shard Environment

### `ShardEnv`

<!-- --8<-- [start:ShardEnv] -->
```juvix
ShardEnv : Type :=
  EngineEnv
    ShardLocalState
    ShardMailboxState
    ShardTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:ShardEnv] -->

#### Instantiation

<!-- --8<-- [start:shardEnv] -->
```juvix extract-module-statements
module shard_environment_example;

  shardEnv : ShardEnv :=
    mkEngineEnv@{
      localState := mkShardLocalState@{
        dagStructure := mkDAGStructure@{
          keyAccesses := Map.empty;
          heardAllReads := 0;
          heardAllWrites := 0
        };
        anchors := []
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:shardEnv] -->
