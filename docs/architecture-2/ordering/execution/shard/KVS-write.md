---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# KVSWrite

- _from_ [[Executor|Executor]]

## Purpose

<!-- --8<-- [start:blurb] -->
Informs the Shard about a new write request, which happens
in either of the following two cases:

- A [[TransactionExecutable]] has determined that it actually will
   write the value at some [[KVSKey|key]] for which it has a write
   (in its [[TransactionLabel]]).
  Now the [[Executor|Executor]] is requesting that value from the [[Shard]]
   that stores it.
- A [[TransactionExecutable]] has finished, and does not actually need
   to write a value for some [[KVSKey|key]] for which it has a lazy write
   (a may_write in the [[TransactionLabel]]).
<!-- --8<-- [end:blurb] -->

<!-- ‼ can we combine KVSWrite and KVSReadRequest into a single message ? -->
<!-- ‼ Yes, but would that save anything? I'm assuming the underlying messaging infrastructure is capable of concatenating 2 messageds together into 1 big message if it has 2 messages to send at the same time, and if that would help.  -->

## Structure

| Field       | Type               | Description                                                                                                                  |
|-------------|--------------------|------------------------------------------------------------------------------------------------------------------------------|
| `timestamp` | [[TxFingerprint]]  | the logical time at which we are writing this data.                                                                          |
| `key`       | [[KVSKey]]           | the key used. With fancy hierarchical keys or suchlike, we could even specify a range of keys                                |
| `datum`     | [[KVSDatum]] option | the new data to be associated with the key. No datum should only be used in a "may_write," and means don't change this value |

#### Effects

A [[Shard]] should delay processing a [[KVSWrite]] until it has
 completed processing [[KVSAcquireLock]] for the
 [[TxFingerprint|same timestamp]].

If the `datum` is `None`, then remove the *may write* marker from
 [[TxFingerprint|this timestamp]] in state.
Any reads waiting to read what is written here must instead read from
 the previous write.
- One way to accomplish this is to copy the previous write as a
    "value written" at [[TxFingerprint|this timestamp]] in state.

If `datum` is occupied, then remove the *may write* or *will write*
 marker from  [[TxFingerprint|this timestamp]] in state, and record the
 value written at [[TxFingerprint|this timestamp]] in state.

This may trigger a [[KVSRead]] if there are any *will read* markers
 for which  [[TxFingerprint|this timestamp]] is the unique previous
 write.

<!--
any garbage collection of old locking info is elided in V1
-->

## Triggers

- _to_ [[Executor|Executor]]: [[KVSRead]]
   `for each` *will read* lock dependent on this write:
    send a [[KVSRead]] to the  [[Executor|relevant Executor]] with the value written.
