#### WorkerHashAvailable
- _from_ [Worker](../worker.md)

##### Purpose
<!-- --8<-- [start:blurb] -->
The worker has stored all the transactions associated with this worker hash.
This means the primary can commit to making this content available.
<!-- --8<-- [end:blurb] -->

[//WorkerHashAvailableDiscardIssue]: # (
It might be useful to add the possibility to
tell the worker to "forget" about this worker hash
)

##### Structure
| Field         | Type                        | Description            |
|---------------|-----------------------------|------------------------|
| `worker_hash` | [`WorkerHash`](#WorkerHash) | the stored worker hash |

The worker hash is really all the information needed.

##### Effects
- The primary stores the worker hash until after the block header it is containing is executed.

[//WorkerHashAvailableDiscardIssueAgain]: # (
see above WorkerHashAvailableDiscardIssue
)

##### Triggers
- to [Primary](../primary.md): [`HeaderCommitment`](./header-commitment.md)
  `if` the worker hash completes an announced header
  _and_ signing this header contributes to an availability certificate
  `then` the primary sends a signature over the header to the creator of the header
