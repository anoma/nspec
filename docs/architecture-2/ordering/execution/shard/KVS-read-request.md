# KVSReadRequest
<!-- --8<-- [start:blurb] -->
- _from_ [[Executor|Executor]]

## Purpose
Informs the Shard about a new read request, which happens
in either of the following cases:

- An [[Executor|Executor]] has determined that it actually needs
   the value at some [[KVSkey|key]] for which it has a lazy read
   (a may_read in the [[TransactionLabel]] of the
   [[TransactionCandidate]]).
  Now the executor is requesting that value from the Shard that stores
   it.
- A [[Executor|Executor]] has finished and does not need
  the value for some [[KVSkey|key]]
  for which it has a lazy read (a may_read in the
   [[TransactionLabel]]).

<!-- --8<-- [end:blurb] -->

<!-- --8<-- [start:details] -->

## Structure

| Field       | Type        | Description                                           |
|-------------|-------------|-------------------------------------------------------|
| `timestamp` | [[TxFingerprint]] | we need the value at this logical timestamp           |
| `key`       | [[KVSKey]]    | the value corresponds to this key                     |
| `actual`    | `bool`      | `true` iff we actually want a response                |

If `actual` is `false`, this just means that there is no dependency on
 this key in the current execution.

## Effects
A [[Shard]] should delay processing a [[KVSReadRequest]] until it has
 completed processing [[KVSAcquireLock]] for the
 [[TxFingerprint|same timestamp]].

Then, if `actual` is false, the Shard is done reading the value, and
 can remove the *may read* marker from state.

If `actual` is true, the Shard replaces the *may read* marker with a
 *will read* marker.
If the Shard knows the unique previous value written before
 [[TxFingerprint|this timestamp]], it sends that value in a [[KVSRead]] to
 the [[Executor|Executor]] and removes the *will read* marker from state.
Otherwise, future [[KVSWrite]]s and/or [[UpdateSeenAll]]s will
 identify this unique previous value written, and trigger the
 [[KVSRead]].

## Triggers

- _to_ [[Executor|Executor]]: [[KVSRead]]
  `if` the Shard has determined the unique value written prior to this "lock"
  `then` send a [[KVSRead]]-message to the relevant [[Executor|Executor]]
  to inform them of the value

<!-- --8<-- [end:details] -->
