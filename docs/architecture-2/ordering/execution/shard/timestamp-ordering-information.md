---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

### TimestampOrderingInformation

* _from_ [Mempool](#Mempool)

#### Purpose

While each transaction comes with a `Timestamp`, the shards do not actually know the order of those timestamps until the DAG is built, and consensus decisions are made. This message represents the mempool communicating (partial) timestamp ordering. These are broadcast to all shards.

#### Structure

!!! todo

    One way to convey this is to include the entire DAG structure (albeit without the transaction contents of each worker batch).
    For now, I do not know what the internal structure of this message looks like.

!!! todo

    check whether,
    ① worker-timestamp (= tx fingerprint),
    ② primary-timestamp (= pure DAG structure based on blocks/headers),
    ③ consensus-timestamp (= total order)
    are sufficiently many cases or we need yet another intermediate gradual step of ordering.
    E.g., does is make sense to also take into account local headers that (without integrity votes).

### Effects

As shards learn more ordering information, they can finally complete reads (since they learn which writes most recently occurred).

### Triggers

- _to_ [Executor](./index.md): [`KVSRead`](../executor/KVS-read.md)
  `for each` locked key for which we have established a unique write value,
  send a `KVSRead` message to the appropriate Executor
