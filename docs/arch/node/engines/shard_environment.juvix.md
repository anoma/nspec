---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- shard
- execution
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.shard_environment;
    import prelude open;
    import arch.node.engines.shard_messages open;
    import arch.node.types.engine_environment open;
    ```

# Shard Environment

## Overview
!!! todo
    This repeats what is already in `shard.juvix.md` should we move that content here? Keep it there?

The Shards together store and update the
 [state](../index.md#state) of the replicated state machine and
  together are a component of the [[Execution Engines]].
They provide [[Executor]]s with input data and update the state
 according to the results of [[Executor]]s' computations.

 Different shards may be on different physical machines.
 <!--
   Redistributing state between shards is called *Re-Sharding*.
   Each Shard is specific to exactly one learner.
   However,
   as an optimization,
   an implementation could conceivably use a single process to do
   the work of multiple shards with different learners
   so long as those shards are identical, and
   fork that process if and when the learners diverge.
-->


Each shard is responsible for a set of [[KVSKey]]s
and these sets are disjoint for different shards.
For each of the keys that a shard is responsible for, the shard maintains a
 (partially-ordered) timeline of Timestamps of
 [[TransactionCandidate|transaction candidates]] that may read or write to keys.
Shards also keep a history of data written by each
 [[TransactionCandidate]] to each key.
This is [multi-version concurrent storage](
    https://en.wikipedia.org/wiki/Multiversion_concurrency_control).


## Mailbox states
!!! todo
    Figure out what a mailbox state is, what makes it special, and if we're just using Unit.

The Shard Engine does not require complex mailbox states.
We define the mailbox state as `Unit`.

### `ShardMailboxState`

```juvix
syntax alias ShardMailboxState := Unit;
```

## Local state
!!! todo
    This repeats what is already in `shard.juvix.md` should we move that content here? Keep it there?

For each [[Worker Engine|Worker Engine]], the Shard maintains:

-  A Timestamp, such that all
   _[[KVSAcquireLock|write lock requests]]_[^1] for
   transaction candidates with earlier timestamps that this worker curates
   have already been received.
  Together, these timestamps represent [`heardAllWrites`](#heardallwrites).
- Another Timestamp, before which
   the Shard will receive no further *read* requests from this
   [[Worker Engine|Worker Engine]].
  For [[WorkerEngine]], this cannot be *after* the corresponding
   *write* Timestamps.
  We will also maintain these from each Read Backend worker.
  Together, these represent `heardAllReads`.

For each [key](#state) (assigned to this Shard):

- A set of [[TxFingerprint|time‍stamps]] of known
   [[TransactionCandidate|transaction candidates]] that read and/or write that key, and for
   each, some subset of:
  - A value written to that key at that [[TxFingerprint|time‍stamps]]
     by that [[TransactionCandidate]] using a [[KVSWrite]] message
  - A marker indicating that this [[TransactionCandidate]] may
     (or will) write to this key, but this Shard has not yet received
     a corresponding [[KVSWrite]] message.
  - A marker indicating that this [[TransactionCandidate]] *will* read
     this value, and an [[ExternalIdentity]] corresponding to the
     relevant [[Executor]].
    This marker is only stored so long as the Shard doesn't know the
     value.
    When this value is determined, this Shard must remove this marker
     and send a [[KVSRead]] message to the [[Executor]].
  - A marker indicating that this [[TransactionCandidate]] *may* read
     this value, and an [[ExternalIdentity]] corresponding to the
     relevant [[Executor]].
    If the [[Executor]] sends a [[KVSReadRequest]] for this key, the
     Shard updates this marker to a "*will* read" marker.
- If a Timestamp has no corresponding markers or
   values written, we don't have to store it.
- If a value written is before `heardAllReads`, and there are no pending
   reads or writes before it, then we can remove all *earlier* values
   written.

Additionally, in versions beyond v0.2.0, the Shard maintains:

- A complete copy of the DAG structure produced by the
   [[Mempool Engines]].
  This includes a set of all [[NarwhalBlockHeader]]s.
  For Timestamps before `SeenAllRead`, if there are
   no keys with a pending read or write before that
   Timestamp, we can delete old DAG structure.
- A complete copy of the sequence of Anchors chosen
   by [[Consensus Engine]].
  This is a sequence of consensus decisions.
  For Timestamps before `heardAllReads`, if there are
   no keys with a pending read or write before that
   Timestamp, we can delete old anchors.

### `ShardLocalState`
!!! todo
    using the below template from commitment, write the local state for a mempool worker (including the stuff in the list above)

```juvix
type WorkerHeardAll := mkWorkerHeardAll@{
  writes : TxFingerprint; -- the shard will receive no further write [[KVSAcquireLock]]s before this time from this worker
  reads : TxFingerprint; -- the shard will receive no further read [[KVSAcquireLock]]s before this time from this worker. Must be before (or equal to) writes.
}
```
???+ quote "Arguments"

    `writes`:
    : the shard will receive no further write [[KVSAcquireLock]]s before this time from this worker

    `reads`:
    : the shard will receive no further read [[KVSAcquireLock]]s before this time from this worker. Must be before (or equal to) writes.
    
```juvix
type ShardLocalState := mkShardLocalState@{
  heard_all : Map ExternalIdentity WorkerHeardAll; -- together, these represent `heardAllReads` and `heardAllWrites`
  timeline : Unit;
};
```
!!! todo
    establish a data structure for storing the timeline for each key, in accordance with what is written in the local state section above. 
    This is complicated by the use of range queries (see state ART report)


## Timer Handle
!!! todo
    figure out what a Timer Handle is, and if a shard needs one.

The Shard Engine does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

### `ShardTimerHandle`

```juvix
syntax alias ShardTimerHandle := Unit;
```

## The Shard Environment

### `ShardEnvironment`

```juvix
ShardEnvironment : Type :=
  EngineEnvironment
    ShardLocalState
    ShardMailboxState
    ShardTimerHandle;
```

### Instantiation
!!! todo
    using the commitment engine template, create a (small) example shard
    this involves figuring out how to isntantiate a map, a worker, and txfingerprints

<!-- --8<-- [start:shardEnvironment] -->
```juvix extract-module-statements
module shard_environment_example;


shardEnvironment : ShardEnvironment :=
    mkEngineEnvironment@{
      name := "shard";
      localState := mkShardLocalState@{
        heard_all := fromList [(worker, mkWorkerHeardAll{writes : genesis, reads : genesis})];
        timeline := unit;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:mempoolWorkerEnvironment] -->
