# KVSRead

<!-- --8<-- [start:blurb] -->
- _from_ [[Shard]]

## Purpose

[[Executor]]s have to read data from keys to execute
 [[TransactionCandidate]]s.
When a [[Shard]] has determined what the value read is at the
 appropriate [[TxFingerprint|timestamp]],
 it sends a [[KVSRead]] to the appropriate [[Executor]].


<!-- --8<-- [end:blurb] -->
<!-- --8<-- [start:details] -->

## Structure

| Field       | Type              | Description                               |
|-------------|-------------------|-------------------------------------------|
| `timestamp` | [[TxFingerprint|TxFingerprint]] | the timestamp at which the datum was read |
| `key`       | [[KVSKey]]          | the key from which the datum is read      |
| `data`      | [[KVSDatum]]        | the datum read                            |

The [[TxFingerprint|timestamp]] should match the
 [[TxFingerprint|timestamp]] of the [[TransactionCandidate]] for this
 [[Executor]].

## Effects

These read values are input for the [[TransactionExecutable]].
Some may be lazy inputs, and some may never be used, but they're all
 inputs.
If this lets us finish the [[TransactionExecutable]], it may trigger
 [[KVSWrite]]s (outputs of the executable), and shutting down the
 [[Executor]] entirely.

## Triggers

- to [[Shard]]: [[KVSWrite]]
  `for each` value the [[TransactionExecutable]] outputs to write
  send a [[KVSWrite]] message to the appropriate [[Shard]]
- to [[Shard]]: [[KVSReadRequest|KVSReadRequest]]
  `for each` lazy read the [[TransactionExecutable]] now requires, and
   each lazy read the [[TransactionExecutable]] hasn't read when it
   terminates:
  send a [[KVSReadRequest|KVSReadRequest]] message to the appropriate [[Shard]]
- to [[Worker Engine]]: [[ExecutorFinished]]
  `If` [[TransactionExecutable]] has terminated
  `then` notify the `curator` specified in [[ExecuteTransaction]]
  <!-- Not used in V1
  or [[ExecuteReadTransaction]]
  -->
  that the transaction is done with an [[ExecutorFinished]].
- to [[User]],[[Solver]]: [[ExecutionSummary]]
  The issuer of the [[TransactionRequest|transaction request]]
  is always provided with the [[ExecutionSummary]]

<!-- --8<-- [end:details] -->
