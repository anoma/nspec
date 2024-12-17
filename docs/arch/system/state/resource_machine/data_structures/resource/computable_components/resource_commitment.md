---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Commitment

Resource commitment is a unique identifier of a resource used to prove the resource's existence and address the resource. Using resource commitment allows to decouple resource semantics (contained in the resource object) and the fact of the resource's existence. For a resource `r`, `r.commitment() = commitmentHash(r)`.
<!--ᚦ«@ "prove the resource's existence": that is not a proof as in proving systems, right?
    I would go as far as the usage of the word _prove_ is confusing.
»-->
<!--ᚦ«r.commitment() = commitmentHash(r) could be mentioned in page that's up» -->

To establish the resource's existence, its commitment is added to a global structure called a commitment tree. This structure is external to the resource machine but the resource machine can read from it.

<!--ᚦ«@"commitment tree" rather, more generally, a cryptography accumulator, right?»-->
<!--ᚦ«put (wiki)links»-->

!!! note

    The resource commitment is also used as the resource's address $r.addr$ in the content-addressed storage.
    <!--ᚦ«... but is computed the same way?»-->

!!! note

    Consumption of the resource does not necessarily affect the resource's status in the storage (e.g., it doesn't get deleted).
    <!--ᚦ«+"However consumption does "lead to" insertion of a nullifier in the nullifier set"~?»-->
