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
