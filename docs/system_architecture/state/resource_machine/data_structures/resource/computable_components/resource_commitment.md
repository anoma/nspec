---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Commitment

Resource commitment is a unique identifier of a resource used to prove the resource's existence and address the resource. Using resource commitment allows to decouple resource semantics (contained in the resource plaintext) and the fact of the resource's existence. For a resource `r`, `r.commitment() = CommitmentHash(r)`.

To establish the resource's existence, its commitment is added to a global structure called a commitment tree. This structure is external to the resource machine but the resource machine can read from it.

!!! note
    The resource commitment is also used as the resource's address $r.addr$ in the content-addressed storage.
 
!!! note
    Consumption of the resource does not necessarily affect the resource's status in the storage (e.g., it doesn't get deleted).

