---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

# Resource Commitment

Information flow control property implies working with flexible privacy requirements, varying from transparent contexts, where almost everything is publicly known, to contexts with stronger privacy guarantees, where as little information as possible is revealed.

From the resource model perspective, stronger privacy guarantees require operating on resources that are not publicly known in a publicly verifiable way. Therefore, proving the resource's existence has to be done without revealing the resource's plaintext.

One way to achieve this would be to publish a **commitment** to the resource plaintext. For a resource $r$, the resource commitment is computed as $r.cm = h_{cm}(r)$. Resource commitment has binding and hiding properties, meaning that the commitment is tied to the created resource but does not reveal information about the resource beyond the fact of creation. From the moment the resource is created, and until the moment it is consumed, the resource is a part of the system's state.

>
> The resource commitment is also used as the resource's address $r.addr$ in the content-addressed storage.
> Consumption of the resource does not necessarily affect the resource's status in the storage (e.g., it doesn't get deleted).

### Commitment accumulator

All resource commitments are stored in an append-only data structure called a **commitment accumulator** $CMacc$. Every time a resource is created, its commitment is added to the commitment accumulator. The resource commitment accumulator $CMacc$ is external to the resource machine, but the resource machine can read from it. A commitment accumulator is a [cryptographic accumulator](https://arxiv.org/abs/2103.04330) that allows to prove membership for elements accumulated in it, provided a witness and the accumulated value.

Each time a commitment is added to the $CMacc$, the accumulator and all witnesses of the already accumulated commitments are updated.
For a commitment that existed in the accumulator before a new one was added, both the old witness and the new witness (with the corresponding accumulated value parameter) can be used to prove membership. However, the older the witness (and, consequently, the accumulator) that is used in the proof, the more information about the resource it reveals (an older accumulator gives more concrete boundaries on the resource's creation time). For that reason, it is recommended to use fresher parameters when proving membership.

#### Accumulator functionality

The commitment accumulator $Acc$ must support the following functionality:

- `ADD(acc, cm)` adds an element to the accumulator, returning the witness used to prove membership.
- `WITNESS(acc, cm)` for a given element, returns the witness used to prove membership if the element is present, otherwise returns nothing.
- `VERIFY(cm, w, val)` verifies the membership proof for an element $cm$ with a membership witness $w$ for the accumulator value $val$.
- `VALUE(acc)` returns the accumulator value.

#### Instantiation
Currently, the commitment accumulator is assumed to be a Merkle tree $CMtree$ of depth $depth_{CMtree}$, where the leaves contain the resource commitments and the intermediate nodes' values are computed using a hash function $h_{CMtree}$.

> The hash function $h_{CMtree}$ used to compute the nodes of the $CMtree$ Merkle tree is not necessarily the same as the function used to compute commitments stored in the tree $h_{cm}$.


For a Merkle tree, the witness is the path to the resource commitment, and the tree root represents the accumulated value. To support the systems with stronger privacy requirements, the witness for such a proof must be a private input when proving membership.
