# TransactionAck
<!-- ANCHOR: blurp -->
- _from_ [[Worker]]

## Purpose

The worker acknowledges a transaction request
with local ordering information and a local wall clock time stamp
that the requester can use as evidence for submission of
a specific transaction candidate.
<!-- ANCHOR_END: blurp -->

<!-- ANCHOR: details -->

## Structure
| Field          | Type              | Description                                                   |
|----------------|-------------------|---------------------------------------------------------------|
| `txHash`       | [[Hash]]          | the hash of the acknowledged transaction candidate            |
| `batch_number` | natural number    | the batch into which the transaction will go                  |
| `timeStamp`    | [[WallClockTime]] | the worker local time stamp of batch opening                  |
| `signature`    | bytes             | the signature of the acknowledging worker over the above data |

The time stamp is the time of when the batch with `batch_number` was opened.
The exact inclusion time into the batch is not communicated to the requester.

## Effects
- The user has evidence for having submitted a transaction to a worker.

## Triggers
none

<!-- ANCHOR_END: details -->
