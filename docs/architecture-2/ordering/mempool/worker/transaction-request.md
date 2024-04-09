# TransactionRequest

<!-- --8<-- [start:blurp] -->
- _from_ [[User|User]], [[Solver|Solver]]

## Purpose

A [[User#user|user]] or [[Solver#solver|solver]] requests that
a [[TransactionCandidate#transactioncandidate|transaction candidate]]
be ordered and executed.
<!-- --8<-- [end:blurp] -->
<!-- --8<-- [start:details] -->

## Structure

| Field          | Type                     | Description                          |
|----------------|--------------------------|--------------------------------------|
| `tx`           | [[TransactionCandidate]] | the actual transaction to be ordered |
| `resubmission` | [[TxFingerprint]] option | reference to the previous occurrence |

The resubmission indicates if there was a previous occurrence of
the very same transaction candidate which either has failed or
a needs to be executed again, e.g., because it is a recurring payment.

This is the "bare-bone" version for V1.
Additional user preferences can be supplied in future versions concerning
- how the response will be given
- how long duplicate checks are to be performed
- etc.

## Effects

- The receiving worker is obliged to store the new transaction
  (until after execution)
  _unless it is out of storage_.
  (Suitable fee mechanisms may be introduced to ensure that
    the probability of sufficient storage is relatively high,
    which involves a trade-off against cheap fees.)
- The received transaction request might complete the current batch.  <!--
  (which then is followed up with the creation of a new worker hash in V2).-->
- The worker assigns
  a [[Batch Number|batch number]]
  (the number of the current batch)
  and a [[Transaction Number|transaction number]]
  (before the closing of the batch)
  such that this transaction candidate can be referenced
  via the corresponding [[TxFingerprint]]—_unless
  the worker already has received a request
  for the same transaction candidate_ after the `resubmission` time stamp.
  If the exact same transaction candidate has already been ordered,
  the request is disregarded;
  optional messages may be sent to the sender of the request.
  <!--BE ALERT: consecutive transaction numbers, but arbitrary order-->

## Triggers

<!-- new ! -->
- [[KVSAcquireLock]]→[[Shard]], [[SpawnExecutor]] → [[Execution Supervisor]]
  `if` the worker has not seen this [[TransactionRequest]]
  before (or "recently")
  `and` a [[TxFingerprint]] is assigned to the transaction candidate
  `then`
  - send [[KVSAcquireLock]]-messages to the relevant [[Shard]]s
  - send [[SpawnExecutor]] to the [[Execution Supervisor]]

!!! todo

    move this as a response to EPID message

- to [[Executor]]: [[ExecuteTransaction]]
    `if` the worker has not seen this [[TransactionCandidate]]
    before (or "recently") after resubmission [^1]
    `and` a [[TxFingerprint]] is assigned to the transaction candidate
    `and` (as an optional pre-condition)
        the worker has seen a [[KVSLockAcquired]] message for this transaction
    `then` spawn a new executor process and send it
        an [[ExecuteTransaction]] message
<!-- --8<-- [end:details] -->