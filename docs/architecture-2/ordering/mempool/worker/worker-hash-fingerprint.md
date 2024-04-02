# WorkerHashFingerprint
- _from_ [Worker](../worker.md)

## Purpose
<!-- --8<-- [start:blurb] -->
The sending worker announces the completion of a worker hash so that the receiving worker can calculate a worker hash from the transaction data (that is being send independently).
<!-- --8<-- [end:blurb] -->

The worker hash subsequently is to be sent to the primary.

## Structure
| Field          | Type           | Description                                 |
|----------------|----------------|---------------------------------------------|
| `batch_number` | natural number | the batch number of the worker hash         |
| `last_tx`      | natural number | the maximum sequence number of transactions |
| `signature`    | bytes          | the signature of the worker                 |

Note that neither the transaction data itself nor their hashes are part of the fingerprint.
Transaction data is sent independently.

## Effects
- The worker can compute the worker hash
  after receiving (and storing) the relevant transaction data.

## Triggers
- to [Primary](../primary.md): [`WorkerHashAvailable`](../primary/worker-hash-available.md)
  `always` send the computed worker hash to the primary (signaling availability)
