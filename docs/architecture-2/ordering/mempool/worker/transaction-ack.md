---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Acknowledgment of incoming transaction requests

Typical direct causes are:

- A [[User|user]] sending a transaction request to the worker.
- A [[Solve|solver]] sending a transaction request to the worker.
- A timer that is set to send acknowledgments to more than one user.

<!-- --8<-- [start:blurp] -->

## Purpose

A worker may acknowledge incoming transaction requests
with local partial ordering information and
a local wall clock time stamp.
The requesting user may use this acknowledgement as evidence
for submission of a specific transaction candidate.[^1]

[^1]: This is the weakest form of pre-confirmation.

<!-- --8<-- [end:blurp] -->

<!-- --8<-- [start:details] -->

## Structure

| Field          | Type              | Description                                                   |
|----------------|-------------------|---------------------------------------------------------------|
| `txHash`       | [[Hash]]          | the hash of the acknowledged transaction candidate            |
| `batch_number` | natural number    | the number of the batch that will contain the transaction candidatae                  |
| `timeStamp`    | [[WallClockTime]] | the worker local time stamp of batch opening                  |
| `signature`    | bytes             | the signature of the acknowledging worker over the above data |

The time stamp is the time of when the batch with `batch_number` was opened.
The exact inclusion time into the batch is not communicated to the requester,
neither a specific `transaction_number` within the batch.

## Effects

- The user has evidence for having submitted a transaction to a worker.

## Triggers

none

<!-- --8<-- [end:details] -->
