# Read Backend
The ReadBackend is a component intended for light client reads.
{TODO We have not spent much time thinking about this one.} **TODO**
##### Incoming Messages
###### From Light Client (over network)
```
type ReadTransactionRequest = SignedMessage<ExecuteReadTransaction>
```
##### Outgoing Messages
###### To Executor
See [`ExecuteReadTransaction`](#ExecuteReadTransaction).
{TODO make a folder for the read backend}
