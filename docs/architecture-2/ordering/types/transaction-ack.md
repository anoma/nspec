# TransactionAck


## Purpose


A `TransactionAck` is
a potentially instant notification for a received transaction
notifying about the batch number of the worker
and when this batch was started according to the worker's local time.

## Structure


| Field          | Type                 | Description                                                  |
|----------------|----------------------|--------------------------------------------------------------|
| `hash`         | bytes                | the hash of the transaction request acknowledged             |
| `batch_number` | natural number       | the batch number assigned                                    |
| `batch_start`  | wall clock time      | the wall clock time of the worker when opening the batch     |
| `collector_id` | [[ExternalIdentity]] | the ɪᴅ of the worker engine that collected the transaction   |
| signature      | bytes                | the signature of the collecting worker engine over the above |


## Note


We cannot make use of a [[TxFingerprint]] of the transaction,
because there might be a slight delay between message reception
and assignation of transaction number for the acknowledged
transaction candidate that is contained in a request.
Also,
there might be several requests for the same transaction candidate
even if this is the not the standard scenario.
