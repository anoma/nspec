# ExecutorPIDAssigned (EPID)
<!-- ANCHOR: blurp -->
## Purpose

Provides the worker with an ID for newly spawned or
available executor engine instance.

<!-- ANCHOR_END: blurp -->
<!-- ANCHOR: details -->


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

<!-- ANCHOR_END: details -->
