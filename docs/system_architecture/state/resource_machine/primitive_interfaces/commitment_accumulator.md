### Commitment accumulator

All resource commitments are stored in an append-only data structure called a **commitment accumulator** $CMacc$. Every time a resource is created, its commitment is added to the commitment accumulator. The resource commitment accumulator $CMacc$ is external to the resource machine, but the resource machine can read from it. A commitment accumulator is a [cryptographic accumulator](https://arxiv.org/abs/2103.04330) that allows to prove membership for elements accumulated in it, provided a witness and the accumulated value.

Each time a commitment is added to the $CMacc$, the accumulator and all witnesses of the already accumulated commitments are updated.
For a commitment that existed in the accumulator before a new one was added, both the old witness and the new witness (with the corresponding accumulated value parameter) can be used to prove membership. However, the older the witness (and, consequently, the accumulator) that is used in the proof, the more information about the resource it reveals (an older accumulator gives more concrete boundaries on the resource's creation time). For that reason, it is recommended to use fresher parameters when proving membership.

#### Accumulator functionality

The commitment accumulator `Accumulator` parametrised over the types `Witness`,`Commitment`, and `AccumulatedValue`, must support the following functionality:

1. `Add(Accumulator, Commitment) -> Witness` adds an element to the accumulator, returning the witness used to prove membership.
2. `Witness(Accumulator, Commitment) -> Maybe Witness` for a given element, returns the witness used to prove membership if the element is present, otherwise returns nothing.
3. `Verify(Commitment, Witness, AccumulatedValue) -> Bool` verifies the membership proof for an element `commitment` with a membership witness `witness` for the accumulated value $value$.
4. `Value(Accumulator) -> AccumulatedValue` returns the accumulator value.

#### Merkle tree
Currently, the commitment accumulator is assumed to be a Merkle tree $CMtree$ of depth $depth_{CMtree}$, where the leaves contain the resource commitments and the intermediate nodes' values are computed using a hash function $h_{CMtree}$.

!!! note
    The hash function $h_{CMtree}$ used to compute the nodes of the $CMtree$ Merkle tree is not necessarily the same as the function used to compute commitments stored in the tree [`Commitment`](./fixed_size_type/hash.md).

##### Interface

For a Merkle tree:

1. `Commitment` type corresponds to resource commitments
2. `Witness` element is a path to the stored`Commitment`
3. `AccumulatedValue` corresponds to the Merkle tree root

and the functions:

1. `Add` adds the resource commitment to the tree, returning the path to the commitment
2. `Witness` finds the resource commitment in the tree and returns the path to it
3. `Verify` uses the resource commitment and the path to reconstruct the root. Returns `True` if the constructed value is equal to the provided value
4. `Value` returns the tree root


!!! warning
    TODO shielded notes: To support the systems with stronger privacy requirements, the witness for such a proof must be a private input when proving membership.
