---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - ordering-subsystem
  - engine
  - shard
  - environment
---

??? code "Juvix imports"

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

The shard environment maintains state about key-value pairs, tracking read and write accesses
for each key across different transaction timestamps. It provides multi-version concurrent storage
capabilities.

## Mailbox states

```juvix
syntax alias ShardMailboxState := Unit;
```

The shard engine does not require complex mailbox states. Therefore, we define the mailbox state type as `Unit`.

## Local state

??? code "Auxiliary Juvix code"

    <!-- --8<-- [start:DAGStructure] -->
    ```juvix
    type ReadStatus := mkReadStatus {
      hasBeenRead : Bool;
      isEager : Bool;
      executor : EngineID
    };

    type WriteStatus KVSDatum := mkWriteStatus @{
      data : Option KVSDatum;
      mayWrite : Bool
    };

    type KeyAccess KVSDatum := mkKeyAccess @{
      readStatus : Option ReadStatus;
      writeStatus : Option (WriteStatus KVSDatum)
    };

    type DAGStructure KVSKey KVSDatum := mkDAGStructure @{
      keyAccesses : Map KVSKey (Map TxFingerprint (KeyAccess KVSDatum));
      heardAllReads : TxFingerprint;
      heardAllWrites : TxFingerprint
    };
    ```
    <!-- --8<-- [end:DAGStructure] -->

### `ShardLocalState`

<!-- --8<-- [start:ShardLocalState] -->
```juvix
type ShardLocalState KVSKey KVSDatum := mkShardLocalState @{
  dagStructure : DAGStructure KVSKey KVSDatum;
  anchors : List NarwhalBlock
};
```
<!-- --8<-- [end:ShardLocalState] -->

???+ code "Arguments"

    `dagStructure`
    : Structure tracking all key accesses across transactions, including read/write status and `heardAll` points

    `anchors`
    : Sequence of consensus decisions (Currently unused)

## Timer handles

```juvix
syntax alias ShardTimerHandle := Unit;
```

The shard engine does not require timers. Therefore, we define the timer handle type as `Unit`.

## The Shard Environment

### `ShardEnv`

<!-- --8<-- [start:ShardEnv] -->
```juvix
ShardEnv (KVSKey KVSDatum : Type) : Type :=
  EngineEnv
    (ShardLocalState KVSKey KVSDatum)
    ShardMailboxState
    ShardTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:ShardEnv] -->

#### Instantiation

<!-- --8<-- [start:shardEnv] -->
```juvix extract-module-statements
module shard_environment_example;

  shardEnv : ShardEnv String String :=
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
