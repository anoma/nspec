#### `NewTransaction`
- _from_ [Worker](#Worker)

##### Purpose
The sending worker is forwarding transaction data for
the purpose of storing a copy (a trivial erasure coding share)
at the receiving worker.

##### Structure

| Field           | Type                    | Description                    |
| -----           | ----                    | -----------                    |
| `tx_data`       | [`TxData`](#TxData)     | the transaction data to store  |
| `fingerprint`   | [`TxFingerprint`]()     | the transaction's fingerprint  |
| ...             | ...                     | ...                            |


##### Effects
- A correct worker will keep the message available until post-order execution.

##### Triggers
- to [Primary](#Primary): [`WorkerHashAvailable`](#WorkerHashAvailable)
  `If` the received transaction data is completing a worker hash copy / erasure coding share  
  `then` notify the primary that the respective worker hash is available  
- to ["execution"](#execution)
  `If` {TODO get this sorted} conditions to be figured out 😅
  `then` notify the relevant shards that they will get tx data from this worker (if they want?)
