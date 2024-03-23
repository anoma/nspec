# RequestLogs
<!-- ANCHOR: blurb -->
- _from_ [[User|User]], [[Solver|Solver]]

## Purpose

Request the log of a finished execution.

<!-- ANCHOR_END: blurb -->

<!-- ANCHOR: details -->

## Structure
<!-- This is mainly meant to specify which lock was acquired -->

| Field         | Type                  | Description                                                            |
|---------------|-----------------------|------------------------------------------------------------------------|
| `fingerprint` | [[TxFingerprint]]     | the fingerprint of the [[TransactionCandidate|TransactionCandidate]] for logs are requested |
| `log_key`     | [[Local Storage Key]] | the key for retrieving the log                                         |

## Effects
none

## Triggers
- to [[User|User]], [[Solver|Solver]]: [[SendLog]]  
  Answer the request with the data requested.

<!-- ANCHOR_END: details -->

