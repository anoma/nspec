# KVSLockAcquired
<!-- ANCHOR: blurb -->
- _from_ [[Shard]]s

## Purpose

This message informs the [[Worker Engine]] that the sending [[Shard]]
 has recorded upcoming read or write requests to a key specified in an
 earlier [[KVSAcquireLock]] from the [[Worker Engine]].
It is an asynchronous response.

<!-- ANCHOR_END: blurb -->

<!-- ANCHOR: details -->

## Structure
<!-- This is mainly meant to specify which lock was acquired -->

| Field         | Type              | Description                                                                             |
|---------------|-------------------|-----------------------------------------------------------------------------------------|
| `fingerprint` | [[TxFingerprint]] | the fingerprint of the [[TransactionCandidate|TransactionCandidate]] for which some locks have been recorded |
| `key`         | [[KVSKey]]        | the key in the key value store that will be accessed                                    |
| `write`       | `bool`            | `true` for write, `false` for read                                                      |
| `optional`    | `bool`            | `true` for may_write or may_read, `false` for will_write or will_read                   |

## Effects
- The [[Worker Engine]] adds this lock to a store of lock acquisitions
   that have been recorded by the shards such that it may be able to
   send  [[UpdateSeenAll]] messages with greater [[TxFingerprint]]s
   than the last one sent.
  - Once an [[UpdateSeenAll]] message is sent, all information the
     [[Worker Engine]] stores concerning [[KVSLockAcquired]]-message
     for earlier transactions can be freed.

## Triggers
- to [[Shard]]s: [[UpdateSeenAll]]  
  `if`  we can now be certain that there is some new [[TxFingerprint]] `T`,
  after (the last one) of the previously sent [[UpdateSeenAll]],
  such that no more [[KVSAcquireLock]]-messages featuring timestamps
  at or before `T` will be sent by the same [[Worker Engine]]:  
  `then`  send [[UpdateSeenAll]] with `T` to all [[Shard]]s.

<!-- ANCHOR_END: details -->

## Note

Otherwise, a Shard might hear about a
 [[KVSAcquireLock]] only after
 it has heard [[UpdateSeenAll]] with a later [[TxFingerprint]], 
 causing it to execute the "later" transaction before it learned of
 the "earlier" one, which could allow the "later" transaction to read
 the wrong value from state. 
Therefore, it is important to let [[Worker Engine]]s know which
 [[KVSAcquireLock]]s the shard has received.


[^1]: In this way, a lock may be granted without knowing about declared access
that would have to be served before.
