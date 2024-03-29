#### IntegrityCertificate
- _from_ [Primary](../primary.md)

##### Purpose
<!-- --8<-- [start:blurb] -->
Integrity Certificates are the components of the signed quorums in future block headers.
They are (learner-specific) proofs that a specific `Header` is unique for a specific primary and at a specific index (height).
<!-- --8<-- [end:blurb] -->

##### Structure
| Field         | Type                                      | Description                          |
|---------------|-------------------------------------------|--------------------------------------|
| `fingerprint` | [`HeaderFingerprint`](#HeaderFingerprint) | the fingerprint of the signed header |
| `signatures`  | bytes list                                | the actual signatures                |


##### Effects
- Integrity certificates can contribute to a new signed quorum,
  which is a component of future [`NarwhalBlockHeader`](../../types/allofthem-v1.md#narwhalblockheader)s.

##### Triggers
- to [Primary](../primary.md): [`HeaderAnnouncement`](./header-announcement.md)
  `if` the received integrity certificate completes a signed quorum for a new [`NarwhalBlockHeader`](../../types/allofthem-v1.md#narwhalblockheader)
  `then` announce the header to all (relevant) primaries (cf. the similar reaction to [NewWorkerHash](./new-worker-hash.md))
