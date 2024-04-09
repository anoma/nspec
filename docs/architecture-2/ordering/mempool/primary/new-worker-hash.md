#### NewWorkerHash

- _from_ [Worker](../worker.md)

##### Purpose

<!-- --8<-- [start:blurb] -->
The worker has completed a worker hash that the primary can process.
<!-- --8<-- [end:blurb] -->

##### Structure

| Field        | Type           | Description                                     |
|--------------|----------------|-------------------------------------------------|
| `batch_hash` | bytes          | the hash of the list of transactions            |
| `length`     | natural number | the number of transactions hashed               |
| `worker_id`  | ID             | the identifier of the sending worker            |
| `signature`  | bytes          | the signature of the worker over the batch hash |

##### Effects

- The primary's next block header should include this worker hash.

##### Triggers

There is nothing to do in `v1`
as all ordering information can be inferred by the execution.
<!--
- to [Primary](../primary.md): [`HeaderAnnouncement`](./header-announcement.md)
  `if` this worker hash completes a block header
  `then` announce the header to all (relevant) primaries
-->
