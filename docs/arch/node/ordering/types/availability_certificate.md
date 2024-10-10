---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Availability Certificate

An availability certificate is a block header together with
a [[Global Weak Quorum|global weak quorum]] of signatures from primaries.
The signatures might either be a plain list,
but aggregated signature are a suitable optimization because
the creator of the block header is collecting all the signatures from primaries.

| Field        | Type             | Description                                                 |
|--------------|------------------|-------------------------------------------------------------|
| `header`     | [[Block Header]] | the block header that is signed                             |
| `signatures` | bytes list       | a list of signatures from a global weak quorum of primaries |
