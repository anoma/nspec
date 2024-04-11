---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# `NarwhalBlockHeader`

Primaries organize batches of transactions into block headers that may also contain signed quorums,
each of which reference a quorum of blocks.

| Field            | Type                               | Description                                          |                 |
|------------------|------------------------------------|------------------------------------------------------|-----------------|
| `id`             | [[architecture-2/abstractions:Identity]]                       | the ɪᴅ of the creating primary                       |                 |
| `height`         | natural number                     | the creator-relative height of the block header      |                 |
| `worker_hashes`  | [[WorkerHash]] list                | the list of [[Worker Hash                            | worker hashes]] |
| `predecessor`    | [[AvailabilityCertificate]] option | the availability certificate of the preceding header |                 |
| `signed_qourums` | [[Signed Quorum]] list             | the list of signed quorums                           |                 |
| `signature`      | bytes                              | the signature by the primary over the above fields   |                 |

The height of genesis is zero and at that is the only height where the availability certificate is `none`.
The list of signed quorums may be empty and must be empty at genesis, i.e., if `height` is zero.

The predecessor uniquely determines the vector of learner-specific heights and
the signed_quorums may only reference the directly preceding block for each
learner.

!!! todo

    spell this out and/or link it

