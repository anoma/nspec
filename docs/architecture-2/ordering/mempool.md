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
In V1,
the mempool is roughly a FIFO queue that takes
transaction requests and passes them on to execution.

## Components

- [[Worker Engine|Workers]] receive
  transaction requests from users or solvers and
  keep transaction data available for executors,
  which they spawn for the purpose of executing transactions
  (in cooperation with shards).
  After successful execution,
  workers keep execution logs available.[^1]

- [[Execution Supervisor]]s are the engines that are in charge
  of spawning new executor processes that workers then use
  to execute transaction requests.

[^1]: In V2, this will be only for a limited period of time.


---

**TODO** 
1. **TODO**  find old  version s (main / v2 / v1 ) of this page
2. **TODO**  conglomerated them and take care of execution !!! 

---
