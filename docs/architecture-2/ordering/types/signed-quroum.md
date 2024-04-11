---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# `SignedQuorum`

A signed quorum is a signature over a list of blocks whose creators together form a learner-specific quorum.

| Field          | Type                  | Description                       |
|----------------|-----------------------|-----------------------------------|
| `learner`      | [[Learner]]           | the learner in question           |
| `block_quorum` | [[NarwhalBlock]] list | the quorum of blocks              |
| `id`           | [[Identifier]]        | the ɪᴅ of the signing entity      |
| `signature`    | bytes                 | the signature over `block_quorum` |
