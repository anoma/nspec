---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

<!-- --8<-- [start:all] -->

# KVSAcquireLock

- _from_ [[Worker Engine|Mempool Worker]] <!-- formerly from [[Executor]] -->

## Purpose

<!-- --8<-- [start:blurp] -->
Inform the shard about keys that a transaction may/will read and/or
 write, at a transaction fingerprint.
<!-- --8<-- [end:blurp] -->
<!-- the range is the novelty w.r.t. to earlier versions of the specs -->

## Structure

| Field | Type | Description |
|-------|------|-------------|
| `lazy_read_keys` | [[KVSKey]] set | Keys this transaction _may_ read (only send values read in response to [[KVSReadRequest]]s)|
| `eager_read_keys` | [[KVSKey]] set| Keys this transaction _will_ read (send values read as soon as possible) |
| `will_write_keys` | [[KVSKey]] set| Keys this transaction _will_ write. Future reads are dependent _only_ on the [[KVSWrite]] for this [[TxFingerprint]].|
| `may_write_keys`  | [[KVSKey]] set| Keys this transaction _may_ write. Future reads are dependent on the [[KVSWrite]] for this [[TxFingerprint]], or, if that has a `None`, the previous value.|
| `curator`| [[ExternalIdentity]] | the [[Worker Engine]] in charge of the corresponding transactions     |
| `executor`| [[ExternalIdentity]] | the [[Executor|Executor]] for this [[TransactionCandidate]]|
| `timestamp`| [[TxFingerprint]] | specifies the transaction affiliated with these locks.

The `lazy_read_keys` and `eager_read_keys` may not overlap.
In the same way,  `will_write_keys` and `may_write_keys` must be
 disjoint.
There must be one `KVSAcquireLock` per [[Shard]]
 per [[TxFingerprint]]: for a given [[Shard]] and [[TxFingerprint]],
 all information is to be provided in totality or not at all.[^1]

Note that future versions may use some kind of structured `Key`s to
 encode "Sets" containing infinitely many `Key`s.
For V1, however, simple HashSets or similar are fine.

## Effects

- The [[Shard]] stores the respective "locks" for all keys in its timeline.
  - these are the "markers" described in [[Shard]] State.
- The `eager_read_keys` will be served as soon as possible
  (by sending `KVSRead`-messages to the [[Executor|executor]]).
- The [[Shard]] immediately informs the [[Worker Engine|curator]] that
   the locks are acquired, using a [[KVSLockAcquired]] message, so the
   [[Worker Engine|curator]] can prepare [[UpdateSeenAll]] messages.

## Triggers

- _to_ [[Worker Engine]]: [[KVSLockAcquired]]
  send a [[KVSLockAcquired]] message to the [[Worker Engine|curator]],
      signaling that the locks of this message will be accounted for.
- to [[Executor|executor]]:  [[KVSRead]]
  `for each` recorded `eager_read_key` in this shard's timeline
  for which the most recent written value is established:
  send a [[KVSRead]] message to the [[Executor|Executor]].

[^1]: Note that transaction requests come with all this information
    at once for each transaction candidate.

<!-- --8<-- [end:all] -->