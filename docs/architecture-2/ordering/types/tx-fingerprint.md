---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# TxFingerprint

## Purpose

The fingerprint of a transaction allows to refer to a transaction succinctly
and gives additional information about the provenance,
primarily used by engines of the ordering machine.

## Structure

| Field          | Type                 | Description                                                            |
|----------------|----------------------|------------------------------------------------------------------------|
| `collector_id` | [[ExternalIdentity]] | the ɪᴅ of the worker engine that collected the transaction             |
| `batchNumber`  | natural number       | the number of the batch into which the transaction was batched         |
| `txNumber`     | natural number       | the transaction number within the batch identified by the batch number |
| `last`         | boolean              | true if and only if the txNumber is the maximal one in this batch      |

## Note

We do not have any field of the hash of the referenced transaction.
A `TxFingerprint` is ordering information that is
only used directly within the ordering machine.
