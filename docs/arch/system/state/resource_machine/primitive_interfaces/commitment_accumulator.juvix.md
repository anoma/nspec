---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module arch.system.state.resource_machine.primitive_interfaces.commitment_accumulator;
```


# Commitment accumulator

All resource commitments are stored in an append-only data structure called a **commitment accumulator**. Every time a resource is created, its commitment is added to the commitment accumulator. The resource commitment accumulator is external to the resource machine, but the resource machine can read from it. A commitment accumulator is a [cryptographic accumulator](https://arxiv.org/abs/2103.04330) that allows to prove membership for elements accumulated in it, provided a witness and the accumulated value.

Each time a commitment is added to the accumulator, the accumulator and all witnesses of the already accumulated commitments are updated.
For a commitment that existed in the accumulator before a new one was added, both the old witness and the new witness (with the corresponding accumulated value parameter) can be used to prove membership. However, the older the witness (and, consequently, the accumulator) that is used in the proof, the more information about the resource it reveals (an older accumulator gives more concrete boundaries on the resource's creation time). For that reason, it is recommended to use fresher parameters when proving membership.

#### Accumulator functionality

!!! note
    The witness we are talking about here is not related to proving system witness. It is a distinct concept of cryptographic accumulators.

The commitment accumulator has type `Accumulator` and is parametrised over the types `AccumulatorWitness`,`CommitmentIdentifier`, and `AccumulatedValue`. The commitment accumulator interface must support the following functionality:

1. `add(Accumulator, CommitmentIdentifier) -> AccumulatorWitness` adds an element to the accumulator, returning the accumulator witness used to prove membership.
2. `witness(Accumulator, CommitmentIdentifier) -> Maybe AccumulatorWitness` for a given element, returns the accumulator witness used to prove membership if the element is present, otherwise returns nothing.
3. `verify(CommitmentIdentifier, AccumulatorWitness, AccumulatedValue) -> Bool` verifies the membership proof for a commitment identified with `CommitmentIdentifier` element with a membership witness `AccumulatorWitness` for the accumulated value `AccumulatedValue`.
4. `value(Accumulator) -> AccumulatedValue` returns the accumulator value.

#### Merkle tree
Currently, the commitment accumulator is assumed to be a Merkle tree `CMTree` of depth $depth_{CMtree}$, where the leaves contain the resource commitments and the intermediate nodes' values are of type [[Hash | `MerkleTreeNodeHash`]].

!!! note
    The type `MerkleTreeNodeHash` of the `CMTree` nodes and the type of the leafs `Commitment` are distinct types.

##### Interface

For a Merkle tree:

1. `CommitmentIdentifier` type corresponds to the identifier of the resource commitment used to locate the commitment's position in the tree
2. `AccumulatorWitness` element is a path to the stored commitment
3. `AccumulatedValue` corresponds to the Merkle tree root

and the functions:

1. `add` adds the resource commitment to the tree, returning the path to the commitment
2. `witness` finds the resource commitment in the tree and returns the path to it
3. `verify` uses the resource commitment and the path to reconstruct the root. Returns `True` if the constructed value is equal to the provided value
4. `value` returns the tree root


!!! todo

    shielded notes: To support the systems with stronger privacy requirements, the witness for such a proof must be a private input when proving membership.
