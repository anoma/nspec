# UpdateSeenAll

- _from_ [[Mempool Engines|Mempool Engines]]

## Purpose

In order to actually serve read requests,
the Shard needs to know that it will not receive more
write requests before a  [[TxFingerprint|certain timestamp]].
These are in general broadcast to all [[Shard]]s.

It is important that  [[Worker Engine|the Worker Engine]] has received
[[KVSLockAcquired]]-messages for all [[KVSAcquireLock]]s it has sent (or will ever send) at or before [[TxFingerprint|the timestamp]].
In other words,
shards know about all possible read and write requests of [[TransactionCandidate]]s
for which the worker is curator and may come earlier.

!!! todo

    rephrase the above paragraph

Each [[Worker Engine|worker engine]] only needs to send the [[Shard Engine]] [[UpdateSeenAll]] messages concerning worker-specific ordering (batch number and sequence number within the batch).
This means that each [[Shard Engine]] needs to hear from  [[Worker Engine|every Worker Engine]] periodically to be sure it is not waiting for any transactions.
From there, the Shard uses [[TimestampOrderingInformation]] about the Narwhal DAG and Consensus to fill in a total order.

## Structure

| Field       | Type              | Description                                                    |
|-------------|-------------------|----------------------------------------------------------------|
| `timestamp` | [[TxFingerprint]] | represents a the position in the total order (in V1)           |
| `write`     | `bool`            | seen all read and seen all write can (and should) be separate. |

For V1, we only care about `write = true`
because we don't garbage collect and assume multi-version storage.
From V2 onward,
the Shard is keeping additional ordering information
and we do have garbage collection protocols.

## Effects

Shards can now identify the unique previous write prior to each read at or before [[TxFingerprint|this timestamp]].
<!-- In V2, this is not necessarily true: they may not have total order yet. -->
If that unique previous write has a value written, and the read is marked *will read*, they can send a [[KVSRead]] with that value to the [[Executor|relevant Executor]].

## Triggers

- _to_ [[Executor|Executor]]: [[KVSRead]]
  `for each` *will read* for which we have established a unique previous write value
  send a `KVSRead` message to the relevant [[Executor|Executor]]
