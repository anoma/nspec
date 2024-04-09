# KVSWritten


## Purpose

Inform the worker about all values written for a given
executed TxFingerprint.

## Structure


| Field       | Type          | Description                             |
|-------------|---------------|-----------------------------------------|
| fingerprint | TxFingerprint | the transaction that finished execution |
| `values`    | `Key`⇀bytes   | a map of  values written                |
| `executor`  | ID-set        | the (set) of executors involved         |
