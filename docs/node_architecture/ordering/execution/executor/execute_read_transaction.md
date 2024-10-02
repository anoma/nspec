---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### ExecuteReadTransaction

---
* _from_ [ReadBackend](#ReadBackend)

### Purpose

Much like the mempool can start executor threads, so can the Read Backend. It's just that the read backend can only specify read-only transactions.

### Structure

| Field | Type | Description |
| ----- | ---- | ----------- |
| `executable` | [`TransactionExecutable`](#TransactionExecutable) | everything this transaction needs to do post-ordering, including any interesting calculations, or proof checks |
| `label` | [`ReadLabel`](#ReadLabel) | but used to specify which parts of the KVS this transaction IS ALLOWED to read |
| `timestamp` | [`Timestamp`](#Timestamp) | represents the transaction's position in the Mempool DAG. As the execution engine gets more information (see `TimestampOrderingInformation`, this lets us order transactions. |
| `initiator` | [`Identity`](#Identity) | who should be informed once all the shards and whatnot have acquired all the locks and such? Usually this is any ReadBackend worker or suchlike involved |

### Effects

This actually creates a new Taiga executor thread (or assigns one from some kind
of thread pool) which will have its own [[Identity]], which we will
then send to the relevant shards. Relevancy is determined using the label.

Note that figuring out how to receive these is hard: we don't want a bottleneck
thread that has to receive and process all of these. Instead, they should
efficiently spin up and/or assign new Executor threads in parallel.

### Triggers

- _to_ [Execution shards](#Shards): [[KVSAcquireLock]]
  `for each` key mentioned in this transaction `label`:
   send a [[KVSAcquireLock]] to the appropriate shard.
