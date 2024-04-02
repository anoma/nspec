# ExecutorFinished
<!-- --8<-- [start:blurp] -->
- _from_ [[Executor]]

## Purpose
Informs the mempool about execution of a transaction.
<!--  do we need this? Cf. "How to give definitive signals for deletion of transaction data" ...  https://github.com/orgs/anoma/projects/14/views/1?pane=issue&itemId=36828426 -->

<!-- --8<-- [end:blurp] -->

<!-- --8<-- [start:details] -->


## Structure
| Field         | Type                  | Description                                                |
|---------------|-----------------------|------------------------------------------------------------|
| `fingerprint` | [[TxFingerprint]]     | a descriptor for executed transaction                      |
| `log_key`     | [[Local Storage Key]] | handle to the transaction log of the transaction execution |



<!--
```rust!
struct ExecutorFinished {
  executable_hash : Hash, // a hash of the [TransactionExecutable] should uniquely identify it without being too repetitive. 
  timestamp : Timestamp, // the timestamp at which the transaction was executed (represents its position in the Mempool DAG)
}
```
-->

## Effects
This message is a pre-requisite for enabling garbage collection in the mempool.
The log_key can be used by the user to request data about the transaction.
In V1, this is kept as long as the instance is running.
<!--
Also, it allows for compiling block data and signing their hashes as commitment.
-->

## Triggers
none
<!--
- to [[User]],[[Worker]]: [[ExecutionSummary]]  
  send the user information about how the transaction was executed
  including logs, valued read and the like
-->

<!-- --8<-- [end:details] -->
