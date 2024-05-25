---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

## Transaction life cycle: from request to execution

Consider the “life cycle” of a transparent asset transfer $T$.

### Mempool

- First,
  user $U$ sends a [[TransactionRequest|transaction request]]
  $R_T$ to a [[Worker Engine|worker]] $W$.
  The user could be a [[Solver]] that is also operating a validator
  and thus likely will choose one of its own workers to process the request.
  The transaction will be included in the current batch of transactions
  or a later one.

- Workers [[TransactionAck|acknowledge]] transaction requests by sending
  a local wall clock time stamp at which they have opened the batch into which
  the transaction is packaged
  accompanied by the assigned [[TxFingerprint]],[^1] i.e.,
  - a _batch number_ $n_B$, and
  - a _transaction number_ $n_{R_T}$ within batch $B$.

<!-- (this will help in the future to complement ferveo for additional MEV protection (so that txs that are submitted in encrypted form to a worker should be processes speedily)
-->
- The [[Worker Engine|worker]] also
  [[ExecuteTransaction|sends the transaction]] to the
  [[Execution Engines|execution engine]],
  starting a new executor process.

- The [[Worker Engine|worker]] informs the [[Shards|shard]] about
  read and write requests that are to be performed now and later
  via [[KVSAcquireLock]] messages.

- Worker $W$ will eventually complete the current batch of transactions $B$
  (after  receiving a number of additional transactions);
  a _batch_ is simply a list of transactions.
  The worker $W$ numbers batches consecutively with natural numbers,
  called _batch numbers_.
  Whenever a new batch is opened,
  the worker also take the local wall clock time stamp for the new batch.

<!--
After closing batch $B$, worker $W$:

- informs its primary $P$ (another engine within the same validator) of the
    [[NewWorkerHash|new worker hash]] $H_B$ for the batch $B$
overkill for V1 as we might scratch the primary anyway
- sends acknowledgments to users in the form of
  a transaction hash with two time stamps
  - one for when the including [[Batch|batch]] was opened
  - and one for when the [[Batch|batch]] was closed
    and the corresponding worker hash was sent off to the primary[^1 time stamp]
-->

### Consensus

As consensus is trivial in the single validator setting,
the ordering of transactions by the worker is already a total order,
namely the lexicographic order on [[TxFingerprint|transaction fingerprints]].
Thus,
what in general would only be _partial_ ordering information by the worker,
is already fixing a total order.

### Execution

- When the [[Worker Engine|mempool worker]] has spawned
  a new [[Executor Process|Executor]] (via the supervisor),
  [[ExecuteTransaction|transaction]] $T$
  to the [[Execution Engines|execution engine]],

- State within the replicated state machine is divided into Key-Value pairs.
  For each portion of Key space $T$'s label permits it to read or
  write.
  For a transparent asset transfer $T$,
  the keys read store proofs
  that the sender has the asset (and has not yet transfered it), and
  the keys written store proofs that the sender has transferred
  the asset.
  Note that some keys can be both read and written.

- For each key read,
  when the relevant [[Shard|shard]] has all information to
  determine the precise data to be read at that time,<!--
  (identifies a unique previous transaction and
  learns the data written by that transaction)-->
  it [[KVSRead|communicates that data]] to the
  [[Execution Engines|executor]].

- While running $T$,
  when the [[Executor Engine|executor]] learns
  any final value to be written to a key,
  it [[KVSWrite|informs the relevant shards]].

<!--
<<👇 maybe v2⁺ because expensive and tx ack should do the trick for V1 >>
- Transaction $T$ can instruct the [[Executor Engine|executor]] to
   perform other side effects
   (such as sending messages to the client), so long as the state
   changes $T$ makes remain deterministic, depending only on $T$ and
   on the values read.
-->

- If $T$ completes without writing values to
  some of the keys on which it has write locks,
  it [[KVSWrite|informs the relevant shards]]
  that they should not update those values,
  effectively releasing the granted locks.

- When $T$ completes, it
  [[ExecutorFinished|informs the mempool worker]] that this
  transaction is finished.
  This information will be used for garbage collection
  from V2 onward.
