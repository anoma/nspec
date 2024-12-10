### Commitment accumulator
<!--ᚦ«why level 3 heading?»-->

All resource commitments are stored in an append-only data structure called a **commitment accumulator**. Every time a resource is created, its commitment is added to the commitment accumulator. The resource commitment accumulator is external to the resource machine, but the resource machine can read from it. A commitment accumulator is a [cryptographic accumulator](https://arxiv.org/abs/2103.04330) that allows to prove membership for elements accumulated in it, provided a witness and the accumulated value.

<!--ᚦ«Who is adding commitmens, when, how, why?»-->
<!--ᚦ«
@"cryptographic accumulator"
preferably, use BibTeX references 
https://specs.anoma.net/latest/tutorial/md/citations.html?h=bibtex#citing-in-markdown
»-->
<!--ᚦ«explain `witness` and `accumulated value`»-->

Each time a commitment is added to the accumulator, the accumulator and all witnesses of the already accumulated commitments are updated.
For a commitment that existed in the accumulator before a new one was added, both the old witness and the new witness (with the corresponding accumulated value parameter) can be used to prove membership. However, the older the witness (and, consequently, the accumulator) that is used in the proof, the more information about the resource it reveals (an older accumulator gives more concrete boundaries on the resource's creation time). For that reason, it is recommended to use fresher parameters when proving membership.

<!--ᚦ«This paragraph may be put into
a helpful note for _using_ the system;
it strictly need not be part of the specs
»-->
<!--ᚦ«
"older accumulator"
→?
"older accumulated value"
»-->

#### Accumulator functionality

The commitment accumulator has type `Accumulator` and is parametrised over the types `Witness`,`CommitmentIdentifier`, and `AccumulatedValue`. The commitment accumulator interface must support the following functionality:

1. `add(Accumulator, CommitmentIdentifier) -> Witness` adds an element to the accumulator, returning the witness used to prove membership.
2. `witness(Accumulator, CommitmentIdentifier) -> Maybe Witness` for a given element, returns the witness used to prove membership if the element is present, otherwise returns nothing.
3. `verify(CommitmentIdentifier, Witness, AccumulatedValue) -> Bool` verifies the membership proof for a commitment identified with `CommitmentIdentifier` element with a membership witness `witness` for the accumulated value `value`.
4. `value(Accumulator) -> AccumulatedValue` returns the accumulator value.

<!--ᚦ«Is `Accumulatedvalue` sth. like (the hash of) the state of the accumulator?»-->

#### Merkle tree
Currently, the commitment accumulator is assumed to be a Merkle tree `CMTree` of depth $depth_{CMtree}$, where the leaves contain the resource commitments and the intermediate nodes' values are of type [`MerkleTreeNodeHash`](./fixed_size_type/hash.md).

<!--ᚦ«can we have a glossary entry and/or wikilink?»-->

!!! note
    The type `MerkleTreeNodeHash` of the `CMTree` nodes and the type of the leafs `Commitment` are distinct types.

##### Interface

For a Merkle tree:

1. `CommitmentIdentifier` type corresponds to the identifier of the resource commitment used to locate the commitment's position in the tree
2. `Witness` element is a path to the stored commitment
3. `AccumulatedValue` corresponds to the Merkle tree root

and the functions:

1. `Add` adds the resource commitment to the tree, returning the path to the commitment
2. `Witness` finds the resource commitment in the tree and returns the path to it
3. `Verify` uses the resource commitment and the path to reconstruct the root. Returns `True` if the constructed value is equal to the provided value
4. `Value` returns the tree root


!!! warning
    TODO shielded notes: To support the systems with stronger privacy requirements, the witness for such a proof must be a private input when proving membership.

<!--ᚦ«where in the life cycle of a resource/tx do private (or public) inputs come into play?»-->
<!--ᚦ«nit: we do not have notes in the specs any more
(except for in comparison to zCash),
right?»-->
