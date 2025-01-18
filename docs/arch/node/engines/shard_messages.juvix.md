---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- shard-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.shard_messages;
    import prelude open;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    ```

# Shard Messages

These are the messages that the Shard engine can receive/respond to.

## Message interface

--8<-- "./shard_messages.juvix.md:ShardMsg"

## Message sequence diagrams

### Transaction Lock and Read Flow

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
    participant WorkerEngine
    participant Shard
    participant Executor
    participant Mempool
    participant Consensus

    WorkerEngine->>Shard: KVSAcquireLock
    Shard->>WorkerEngine: KVSLockAcquired
    Executor->>Shard: KVSReadRequest
    Mempool->>Shard: UpdateSeenAll
    Consensus->>Shard: AnchorChosen
    Shard->>Executor: KVSRead
    Executor->>Shard: KVSWrite
```

<figcaption markdown="span">
Sequence Diagram: Transaction Lock and Read Flow
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->


## Message types

### `KVSReadRequestMsg`

Read request from an [[Executor Engine]].

<!-- --8<-- [start:KVSReadRequestMsg] -->
```juvix
type KVSReadRequestMsg : Type :=
  mkKVSReadRequestMsg {
    timestamp : TxFingerprint;
    key : KVSKey;
    actual : Bool
  }
```
<!-- --8<-- [end:KVSReadRequestMsg] -->

???+ quote "Arguments"

    `timestamp`
    : The logical timestamp identifying the transaction at which to read

    `key`
    : The key to read

    `actual`
    : True if value is actually needed, false if just cleaning up a lazy read

### `KVSWriteMsg`

Write request from an [[Executor Engine]].

<!-- --8<-- [start:KVSWriteMsg] -->
```juvix
type KVSWriteMsg : Type :=
  mkKVSWriteMsg {
    timestamp : TxFingerprint;
    key : KVSKey;
    datum : Option KVSDatum
  }
```
<!-- --8<-- [end:KVSWriteMsg] -->

???+ quote "Arguments"

    `timestamp`
    : The logical timestamp identifying the transaction in which to write

    `key`
    : The key to write to

    `datum`
    : The data to write, or `none` to indicate no write

### `UpdateSeenAllMsg`

Update about seen transactions from a [[Mempool Worker Engine]].

<!-- --8<-- [start:UpdateSeenAllMsg] -->
```juvix
type UpdateSeenAllMsg : Type :=
  mkUpdateSeenAllMsg {
    timestamp : TxFingerprint;
    write : Bool
  }
```
<!-- --8<-- [end:UpdateSeenAllMsg] -->

???+ quote "Arguments"

    `timestamp`
    : The logical timestamp at which to push the SeenAll value.

    `write`
    : Whether it is the `SeenAllReads` or `SeenAllWrites` to update.


### `KVSAcquireLockMsg`

Request to acquire locks for transaction execution.

<!-- --8<-- [start:KVSAcquireLockMsg] -->
```juvix
type KVSAcquireLockMsg : Type :=
  mkKVSAcquireLockMsg {
    lazy_read_keys : Set KVSKey;
    eager_read_keys : Set KVSKey;
    will_write_keys : Set KVSKey;
    may_write_keys : Set KVSKey;
    worker : EngineID;
    executor : EngineID;
    timestamp : TxFingerprint
  }
```
<!-- --8<-- [end:KVSAcquireLockMsg] -->

???+ quote "Arguments"

    `lazy_read_keys`
    : Keys this transaction may read (only send values read in response to `KVSReadRequest`s)

    `eager_read_keys`
    : Keys this transaction will read (send values read as soon as possible)

    `will_write_keys`
    : Keys this transaction will write

    `may_write_keys`
    : Keys this transaction may write

    `worker`
    : The Worker Engine in charge of the transaction

    `executor`
    : The Executor for this transaction

    `timestamp`
    : Specifies the transaction affiliated with these locks

### `KVSLockAcquiredMsg`

Confirmation that locks were acquired.

<!-- --8<-- [start:KVSLockAcquiredMsg] -->
```juvix
type KVSLockAcquiredMsg : Type :=
  mkKVSLockAcquiredMsg {
    timestamp : TxFingerprint
  }
```
<!-- --8<-- [end:KVSLockAcquiredMsg] -->

???+ quote "Arguments"

    `timestamp`
    : The timestamp of the transaction which was locked.

### `KVSReadMsg`

Value read response to executor.

<!-- --8<-- [start:KVSReadMsg] -->
```juvix
type KVSReadMsg : Type :=
  mkKVSReadMsg {
    timestamp : TxFingerprint;
    key : KVSKey;
    data : KVSDatum
  }
```
<!-- --8<-- [end:KVSReadMsg] -->

???+ quote "Arguments"

    `timestamp`
    : The timestamp of the transaction which was read.

    `key`
    : The key which was read.

    `data`
    : The the data read.

### `ShardMsg`

<!-- --8<-- [start:ShardMsg] -->
```juvix
type ShardMsg :=
  | ShardMsgKVSReadRequest KVSReadRequestMsg
  | ShardMsgKVSWrite KVSWriteMsg
  | ShardMsgKVSAcquireLock KVSAcquireLockMsg
  | ShardMsgKVSLockAcquired KVSLockAcquiredMsg
  | ShardMsgKVSRead KVSReadMsg
  | ShardMsgUpdateSeenAll UpdateSeenAllMsg
  ;
```
<!-- --8<-- [end:ShardMsg] -->
