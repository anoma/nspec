# ExecuteTransaction

<!-- --8<-- [start:blurb] -->
* _from_ [[Mempool Engines|Mempool]]

## Purpose

The [[Mempool Engines|mempool engines]] instruct the [[Executor]] that a new
 [[TransactionCandidate]] has been recorded, its locks are being
 acquired, and will eventually need to be executed.

<!-- --8<-- [end:blurb] -->
<!-- --8<-- [start:details] -->

## Structure

| Field        | Type                      | Description                                                                   |
|--------------|---------------------------|-------------------------------------------------------------------------------|
| `executable` | [[TransactionExecutable]] | "code" to be executed post-ordering                                           |
| `label`      | [[TransactionLabel]]      | information about keys that the transaction can rightfully access             |
| `timestamp`  | [[TxFingerprint|TxFingerprint]]         | (partial) ordering information (sufficient for V1)                            |
| `curator`    | [[ExternalIdentity]]      | the [[Worker Engine]] to be informed when execution completes (e.g. for logs) |
| `issuer`     | [[ExternalIdentity]]      | the ID of the sender of the [[TransactionRequest]]                            |

## Effects

This message is sent to an [[Executor]] that is already running.
Concurrently, when the [[Worker Engine]] sends a [[KVSAcquireLock]] to
 [[Shard]]s, they can include *eager reads*, which will result in
 [[KVSRead]]s sent to this [[Executor]].

## Triggers

- {[[KVSReadRequest|KVSReadRequest]], [[KVSWrite]]}→[[Shard]]s:
  In the course of evaluating the
   *executor function*,
   lazy reads are requested, and final writes are output.

  - [[KVSReadRequest|KVSReadRequest]] to [[Shard]]
  - [[KVSWrite]] to [[Shard]]

  !!! todo
      make this precise :-/
<!-- --8<-- [end:details] -->

## Notes

- Getting served read requests amounts to locks being granted by the shards.

!!! todo

    contention footprint description
