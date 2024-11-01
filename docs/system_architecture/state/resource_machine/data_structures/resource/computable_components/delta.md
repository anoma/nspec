---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Delta
Resource delta is used to reason about the total quantities of different kinds of resources in transactions. For a resource `r`, its delta is computed as `r.delta() = DeltaHash(r.kind(), r.quantity)`.


