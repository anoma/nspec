---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# ExecutionSummary

## Purpose

The data structure for holding all information about
the execution of a transaction candidate
that could be made available to the issuer of
the corresponding transaction request.

## Structure

| Field            | Type                          | Description                                  |
|------------------|-------------------------------|----------------------------------------------|
| `success`        | boolean                       | true iff the execution finished successfully |
| `values_read`    | ([[KVSKey]]×[[KVSDatum]]) set | the set of values read for keys              |
| `values_written` | ([[KVSKey]]×[[KVSDatum]]) set | the set of values written to keys            |
| `log_key`        | [[Local Storage Key]]         | the key at which the execution log is stored |

## Note

By default, the `log_key` is the hash of the execution log.
