# RequestLogs
<!-- --8<-- [start:blurb] -->
- _from_ [[User|User]], [[Solver|Solver]]

## Purpose

Request the log of a finished execution.

<!-- --8<-- [end:blurb] -->

<!-- --8<-- [start:details] -->

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

<!-- --8<-- [end:details] -->

