---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Mempool

The mempool receives transaction requests
and stores them such that they are available for the
[[Execution Engines|execution engines]].
The mempool triggers the execution of transaction candidates
for all transaction candidates received by any validator.
Finally,
it also provides partial ordering information to shards,
and contributes to
the dissemination of future lock requests to the state.
In V0.2.0 and below,
the mempool is roughly a FIFO queue that takes
transaction requests and passes them on to execution.
It has only one [[Worker Engine]] and as such requires no ``primary.''

## Components

- [[Worker Engine|Workers]] receive
  transaction requests from users or solvers and
  keep transaction data available for executors,
  which they spawn for the purpose of executing transactions
  (in cooperation with shards).
  After successful execution,
  workers keep execution logs available.[^1]

[^1]: In V0.2.0 and below, this will be only for a limited period of time.
