---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Worker

## Purpose

Workers are one of the [[Mempool Engines|mempool engines]].
All workers receive transaction requests from users and solvers.
Given the "stream" of requests that they are receiving from users and solvers as input,
each worker produces a sequence of batches of transaction candidates.
Transaction batches are stored and worker hashes for them are fabricated
and sent to their primary, which is building the actual mempool DAG
that is referencing the batches via hashes.



---

!!! note

	here is a (temporary) list of references to the TLA+ spec, 
	called [Doris](https://en.wikipedia.org/wiki/Doris_(Oceanid))

### tla-types

- [Batches](https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L69-L75) in the formal spec are abstracting away from the containing transaction candidates. Thus, the internal structure of batches is only specified in specs.anaoma.net / nspec.

### tla-actions

The list of all action is described in the [tla-spec](https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L742-L789)

- [BatchBC](https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L755-L758)
  - [def](https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L809-L842)

```
(* - Batch broadcast "BatchBC" (message "Batch"):                          *)
(*                                                                         *)
(*   A worker broadcasts a                                                 *)
(*   batch, stores it, and forwards it to its primary for vertex inclusion. *)
```



- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L760-L763

```
(* - Batch storing "StoreBatch" (NO message ):                             *)
(*                                                                         *)
(*   Reception of a batch, storing and hashing such that recieved vertices   *)
(*   can be validated and acknowledged by the primary.                     *)
```
- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L765-L770
```
(* - Batch broadcast "BatchBC" (message "Batch"):                          *)
(*                                                                         *)
(*   A worker broadcasts a                                                 *)
(*   batch, stores it, and forwards it to its primary for vertex inclusion. *)
```

- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L772-L774
```
(* - Vertex acknowledgement "Ack" (message "Ack")                           *)
(*                                                                         *)
(*   Receive a vertex, check its validity, store it, & acknowledge it.      *)
```

- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L776-L779
```
(* - Certificate broadcats "CertBC" (message "Cert")                       *)
(*                                                                         *)
(*   Take an acknowledgement quorum of a proposed vertex, aggregate it      *)
(*   into a ceritificate, and broadcast the certificate.                   *)
```

- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L781-L783
```
(* - Store a vertex certificate "StoreVertex" (NO message)                   *)
(*                                                                         *)
(*   “Receive” a certificate of availability and store it.                 *)
```

- https://github.com/anoma/typhon/blob/2e810a1e0546a66c1c530d978c330967010ce080/tla/Doris.tla#L785-L788
```
(* - Advancing the local round 'AdvanceRound' (NO message)                 *)
(*                                                                         *)
(*   A validator moves to the next round,                                  *)
(*   after receiving a quorum of vertex certificates.                       *)
```

-
```
```

-
```
```

-
```
```

-
```
```

-
```
```

-
```
```



---

##

!!! todo

	fix/revise the rest of this page

<!--[^4]-->
The worker receives transaction requests from users and
[[Solver#solver|solvers]] and batches these transaction requests, assigning a
unique [[TxFingerprint#txfingerprint|TxFingerprint]] to every new transaction.
Each transaction candidate will be sent to an [[Executor#executor|Executor]]
inside an [[ExecuteTransaction#executetransaction|ExecuteTransaction]] message.
Once the worker has received a [[KVSLockAcquired]] for every part of the
transaction request's label (from the shards of the same Anoma validator in
response to [[KVSAcquireLock]]-messages), it knows that this transaction
candidate has been _"seen"_ by all [[Shard#shard|Shards]], which implies that
all shards are prepared to process lock requests from execution processes (see
[[KVSReadRequest]] and [[KVSWrite]] for details). This information about locks
being recorded is distributed to all [[Shard#shard|shards]] via
[[UpdateSeenAll#updateseenall|UpdateSeenAll]] messages, which contain the most
recent [[TxFingerprint#txfingerprint|TxFingerprint]] for which it is certain
that _all_ [[Shard#shard|Shards]] have _"seen"_ this transaction candidate and
all previous ones from the same worker (and they are thus prepared to grant
locks). Note that if [[Shard#shard|shards]] receive transaction candidates in a
different order than the final total order of transactions,
[[UpdateSeenAll#updateseenall|UpdateSeenAll]] messages are necessary to avoid
that [[Shard#shard|shards]] grant locks before all locks of previous transaction
executions have been served.

Workers also are in charge of collecting and curating logs of transaction
execution. Success is equivalent to all reads and writes being successful and an
[[ExecutorFinished]]-message from the [[Executor#executor|executor]] that was
spawned to execute the message.
<!--[^6]-->
<!--ᚦ from v2 onward, we signed summaries -->

<!--ᚦ additionally, workers might send
batched sets of read write lables to shards---which might be _empty_!
- similarly/alternatively (?), updateseenall might also be only sent
  once per batch (to avoid the number of messages passed)
- KVSAcquireLock could be send by worker instead of execution
  at least in principle
-->

## State

Each worker keeps track of

- the current batch number (consecutively numbered)

- the list of [[TransactionCandidate|transaction candidate|]]s in each batch

- a unique [[TxFingerprint]] for each transaction candidate,
  at least in previous batches

- the set of relevant received [[KVSLockAcquired]]-acquired messages

- the set of relevant sent [[UpdateSeenAll]]-messages

- [[ExecutionSummary|execution summaries]] for each transaction

There is no precise state representation described by the V1 specs.

!!! todo

    the following almost certainly are not the template we want -->

## [[ExecutorFinished]]

--8<-- "worker/executor-finished.md:blurp"

<details  markdown="1">
  <summary>Details</summary>
--8<-- "worker/executor-finished.md:details"
</details>

## [[TransactionRequest]]

--8<-- "worker/transaction-request.md:blurp"

<details  markdown="1">
  <summary>Details</summary>
--8<-- "worker/transaction-request.md:details"
</details>

## [[ExecutorPIDAssigned]]

--8<-- "worker/executor-PID-assigned.md:blurp"

<details  markdown="1">
  <summary>Details</summary>
--8<-- "worker/executor-PID-assigned.md:details"
</details>

## [[KVSLockAcquired]]

--8<-- "worker/KVS-lock-acquired.md:blurb"

<details  markdown="1">
  <summary>Details</summary>
--8<-- "worker/KVS-lock-acquired.md:details"
</details>

## [[RequestLogs]]

--8<-- "worker/request-logs.md:blurb"

<details  markdown="1">
  <summary>Details</summary>
--8<-- "worker/request-logs.md:details"
</details>

<!--
## [`NewTransaction`](worker/new-transaction.md)

from Worker may trigger:

- `WorkerHashAvailable` → Primary
  --8<-- "./primary/worker-hash-available.md:blurb"
-->

<!--
## [`WorkerHashFingerprint`](worker/worker-hash-fingerprint.md)

from Worker may trigger:

- `WorkerHashAvailable` → Primary
  --8<-- "./primary/worker-hash-available.md:blurb"
-->

!!! todo

    we need to find better places for these footnotes

[^1]: It might be too expensive to check from genesis;
    transaction requests could have a parameter for
    how long the duplicate check is active.

[^2]: This condidtion can be added to avoid
    too many waiting/idling executor processes.
    (This comes at the price of a sliver of
    additional latencey for the first transactions in a batch.)
    Note that this cannot lead to deadlocks
    as the lock acquisition messages
    (KVSAcquireLock,KVSLockAcquired,UpdateSeenAll)
    are completely independent of spawning transactions.
    In more detail,
    if we were missing a KVSAcquireLock message for a transaction,
    the executor could not start operating (even if it is spawned).

[^3]: This can be done by use of a executor process supervisor
    in the implementation.

[^4]: In all future versions of Anoma,
    workers will be organized around primaries;
    however, in V1, we can omit primaries as they do not serve any purpose.
    In V1, there is only a single worker,
    which can be though of as featuring also as its primary.

[^5]: In future versions,
    IO is output of results from the responsible workers
    (and their fellow/mirror workers) to some fixed address.
    Inputs may allow for non-trivial validator inputs,
    according to a orthogonal protocol (an may fail deterministically).

[^6]: In V1,
    we report all the data about a single transaction back to the submitter
    as part of execution.
-->
