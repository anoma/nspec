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
    module arch.node.engines.shard_2_environment;
    import prelude open;
    import arch.node.engines.shard_2_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Shard Environment

??? quote "Auxiliary Juvix code"

    ```juvix
    syntax alias ChainId := String;
    syntax alias Height := Nat;
    syntax alias Learner := String;
    syntax alias KVSTimestamp := TxFingerprint;
    ```

## Overview

The shard environment maintains state about key-value pairs, timestamps, timelines, and transaction histories. It provides multi-version concurrent storage capabilities.

## Mailbox states

```juvix
syntax alias ShardMailboxState := Unit;
```

The shard engine does not require complex mailbox states. Therefore, we define the mailbox state type as `Unit`.

## Local state

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:KeyData] -->
    ```juvix
    type WriteMarker := mkWriteMarker {
      mayWrite : Bool
    };

    type ReadMarker := mkReadMarker {
      executor : EngineID;
      isEager : Bool
    };

    type KeyState := mkKeyState {
      value : KVSDatum;
      readMarkers : Map KVSTimestamp ReadMarker;
      writeMarkers : Map KVSTimestamp WriteMarker;
    };

    type TimestampBound := mkTimestampBound {
      timestamp : KVSTimestamp;
      write : Bool
    };
    ```
    <!-- --8<-- [end:KeyData] -->

### `ShardLocalState`

<!-- --8<-- [start:ShardLocalState] -->
```juvix
type ShardLocalState := mkShardLocalState {
  keyStates : Map KVSKey KeyState;
  heardAllBounds : Map EngineID TimestampBound;
  dagStructure : List NarwhalBlock;
  anchors : List NarwhalBlock
};
```
<!-- --8<-- [end:ShardLocalState] -->

???+ quote "Arguments"

    `keyStates`
    : Map of keys to their timeline state including values, read markers and write markers

    `heardAllBounds`
    : Timestamp bounds from each worker engine before which all reads/writes are known

    `dagStructure`
    : DAG structure from mempool for ordering transactions

    `anchors`
    : Sequence of consensus decisions

## Timer handles

```juvix
syntax alias ShardTimerHandle := Unit;
```

The shard engine in V1 does not require timers. Therefore, we define the timer handle type as `Unit`.
## The Shard Environment

### `ShardEnv`

<!-- --8<-- [start:ShardEnv] -->
```juvix
ShardEnv : Type :=
  EngineEnv
    ShardLocalState
    ShardMailboxState
    ShardTimerHandle
    ShardMsg;
```
<!-- --8<-- [end:ShardEnv] -->

#### Instantiation

<!-- --8<-- [start:shardEnv] -->
```juvix extract-module-statements
module shard_environment_example;

  shardEnv : ShardEnv :=
    mkEngineEnv@{
      localState := mkShardLocalState@{
        keyStates := Map.empty;
        heardAllBounds := Map.empty;
        dagStructure := [];
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