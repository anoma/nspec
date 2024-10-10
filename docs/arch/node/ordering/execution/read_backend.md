---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Read Backend

The ReadBackend is a component intended for light client reads.

!!! todo

    We have not spent much time thinking about this one.

##### Incoming Messages

###### From Light Client (over network)
```
type ReadTransactionRequest = SignedMessage<ExecuteReadTransaction>
```
##### Outgoing Messages

###### To Executor
See [`ExecuteReadTransaction`](#ExecuteReadTransaction).

!!! todo

    make a folder for the read backend
