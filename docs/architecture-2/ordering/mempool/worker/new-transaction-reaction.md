---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Incoming `NewTransaction` processing

Typical direct causes are:

- [[Worker]]s, having received a new transaction candidate

## Purpose

<!-- --8<-- [start:blurb] -->
The sending worker is forwarding a copy of 
a new transaction candidate `tx`
for the purpose of storing a copy 
(until after execution).
<!-- --8<-- [end:blurb] -->

##### Structure

| Field         | Type                              | Description                   |
|---------------|-----------------------------------|-------------------------------|
| `tx_data`     | [`TxData`](#TxData)               | the transaction data to store |
| `fingerprint` | [`TxFingerprint`](#TxFingerprint) | the transaction's fingerprint |

##### Effects

- A correct worker will keep the message available until
  post-ordering execution has signaled success.
- The transaction data is tagged with a
  [batch number](#BatchNumber) and a
  [sequence number](#SequenceNumber)
  determined by the receiving worker.

##### Triggers

- to [Primary](../primary.md): [`WorkerHashAvailable`](../primary/worker-hash-available.md)
  `If` the received transaction is completing the underlying data of a received worker hash
  `then` send the worker hash to the primary (signaling its availability)
