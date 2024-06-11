---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Incoming transaction ordering request processing

<!-- --8<-- [start:blurp] -->
- _from_ [[User|User]], [[Solver|Solver]]

## Purpose

A [[User|user]] or [[Solver|solver]] has sent a [[TransactionRequest]] 
that contains a [[TransactionCandidate|transaction candidate]] `tx`,
and requests that the latter be included into the mempool
(to be ordered by [[consesus|Consensus Engines]]).

<!-- --8<-- [end:blurp] -->
<!-- --8<-- [start:details] -->

## Reaction description

- The receiving worker is obliged to store the new transaction candidate `tx`
  (until after execution).[^1]
  
- If the received transaction candidate `tx` completes the current batch,
  the batch will be finalized
  (_now_, but possibly in one of the "immediately"[^3] next steps).
  
- The worker immediately assigns a [[Batch Number|batch number]]
  (the number of the current batch)
  and—possibly later,<!--
  --> but before the closing of the batch—a
  [[Transaction Number|transaction number]]
  (such that the enclosed transaction candidate `tx` can be referenced
  via the corresponding [[TxFingerprint]]).[^2]
  
- The worker broadcastes a [[NewTransaction]] message to 
  all its mirror workers,
  i.e., all workers on a different validator that have the same _index_.
  
!!! todo

	agree on index of worker on validator as terminology
	cf. the [TLA+-spec](https://github.com/anoma/typhon/blob/0bd2bc01d82298fc346c4139520331e6062c17b4/tla/MempoolSpec.tla#L114)

## Guarded reactions

- [[NewTransaction]]→[[Worker]]:  
  `if` the worker has not seen the enclosed [[TransactionCandidate]] `tx`
  <!-- duplication: should we have nested guards? !!! -->
  `then` send [[NewTransaction]] for the transaction candidate `tx` to
  all mirror workers

!!! todo

	fix the rest of the page after settling on 
	how to create engine ids
	
---	

<!-- new ! -->
- [[KVSAcquireLock]]→[[Shard]], [[SpawnExecutor]]→[[Execution Supervisor]]
  `if` the worker has not seen the enclosed [[TransactionCandidate]]
   yet
  `and` a [[TxFingerprint]] is assigned to the transaction candidate `tx` 
  `then`
  - send [[KVSAcquireLock]]-messages to the relevant [[Shard]]s

<!-- there's this spurious stuff here .. -->

  - spawn an [[Executor Engine]] for the enclosed transaction candidate `tx`
    with the hash of the [[TransactionRequest]] as spawn-ticket

<!-- in view of the following todo -->

!!! todo

    move this as a response to EPID message / reaction to engine has spawned event 

- to [[Executor]]: [[ExecuteTransaction]]
    `if` the worker has not seen this [[TransactionCandidate]]
    before (or "recently") after resubmission <!-- [lost footnote] -->
    `and` a [[TxFingerprint]] is assigned to the transaction candidate
    `and` (as an optional pre-condition)
        the worker has seen a [[KVSLockAcquired]] message for this transaction
    `then` spawn a new executor process and send it <!-- the issue is that this is not necessarily non-atomic -->
        an [[ExecuteTransaction]] message
<!-- --8<-- [end:details] -->


<!-- footnotes -->

---

[^1]: In V2, we elide fee mechanisms, and "out of storage" handling.

[^3]: We may want to maximize for throughput, but only if latency is only slightly affected. 

[^2]: In V2, we elide mechanisms for transmission resubmission. (The original Narwhal does not cover that situation either.)
   
