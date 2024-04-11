---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ExecutorPIDAssigned (EPID)

<!-- --8<-- [start:blurp] -->
## Purpose

Provides the worker with an ID for newly spawned or
available executor engine instance.

<!-- --8<-- [end:blurp] -->
<!-- --8<-- [start:details] -->

## Structure

| Field  | Type                 | Description                                        |
|--------|----------------------|----------------------------------------------------|
| `epid` | [[ExternalIdentity]] | the ID of the spawned [[executor|Executor]]-engine instance |

## Effects

The receiving worker can request the eager reads and start the execution.

## Triggers

- [[executetransaction|ExecuteTransaction]]→[[executor|Executor]], [[KVSReadRequest]]→[[Shard]]s:
  for the next transaction to be executed,
  the worker sends
  - the [[executetransaction|ExecuteTransaction]]-message to the executor
  - the will-read [[KVSReadRequest]]s to the relevant [[Shard]]s

<!-- --8<-- [end:details] -->
