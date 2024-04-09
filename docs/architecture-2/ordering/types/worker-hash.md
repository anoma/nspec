# WorkerHash


In V1,
we do not use worker hashes in the sense of Narwhal
or related DAG-based mempools.

<!--
A _worker hash_ is the hash of [[Transaction Batch|batch of transactions]]
(and accompanying information)
that are sent to primaries for the purpose of
referencing the respective transactions.

| Field         | Type           | Description                                       |
|---------------|----------------|---------------------------------------------------|
| `hash`        | [[Hash]]       | the hash of a non-empty list of transactions      |
| `batchNumber` | natural number | the [[Batch Number]] of the underlying batch      |
| `length`      | natural number | the count of transactions hashed                  |
| `signature`   | bytes          | the signature by the worker over the above fields |
| `creator`     | [[Identity]]   | the ɪᴅ of the creating worker                     |
-->
