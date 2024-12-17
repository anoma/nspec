---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

!!! warning
    Will be updated soon

# Stored data format
<!--ᚦ
    «can we separate out the data types that are only relevant for
        post-ordering execution?»
-->

The ARM state that needs to be stored includes resource objects, the commitment accumulator and the nullifier set.
The table below defines the format of that data assumed by the ARM.

|Name|Structure|Key Type|Value Type
|-|-|-|-|
Commitment accumulator (node) | Cryptographic accumulator | timestamp | $\mathbb{F}$
Commitment accumulator (leaf) | - | (`timestamp`, $\mathbb{F}$) | $\mathbb{F}$
Nullifier set | Set | $\mathbb{F}$ | $\mathbb{F}$
Hierarchical index | Chained Hash sets | Tree path | $\mathbb{F}$
Data blob storage | Key-value store with deletion criterion | $\mathbb{F}$ | (`variable length byte array`, `deletion criterion`)

<!--ᚦ
    «What is 𝔽»
-->

## `CMtree`

Each commitment tree node has a timestamp associated with it, such that a lower depth (closer to the root) tree node corresponds to a less specified timestamp: a parent node timestamp is a prefix of the child node timestamp, and only the leaves of the tree have fully specified timestamps (i.e. they are only prefixes of themselves). For a commitment tree of depth $d$, a timestamp for a commitment $cm$ would look like $t_{cm} =t_1:t_2:..:t_d$, with the parent node corresponding to it having a timestamp $t_1:t_2:..:*$. The timestamps are used as keys for the key-value store. For the tree leaves, $<cm, t_{cm}>$ pairs are used as keys. Merkle paths to resource commitments can be computed from the hierarchy of the timestamps.
<!--ᚦ
    «@can be computed from the hierarchy of the timestamps
    How?
    Can we have some more explnations / links (applies also to future versions)?
    »
-->

## `NFset`

Nullifiers are used as keys in the key-value store. In future versions, a more complex structure that supports efficient non-membership proofs might be used for storing the nullifier set.

## Hierarchical index
The hierarchical index is organised as a tree where the leaves refer to the resources, and the intermediate nodes refer to resource _subkinds_ that form a hierarchy. The label of a resource $r$ stored in the hierarchical index tree is interpreted as an array of *sublabels*: $r.label = [label_1, label_2, label_3, ...]$, and the i-th subkind is computed as $r.subkind_i = H_{kind}(r.l, r.label_i)$.

> In the current version, only the subkinds derived from the same resource logic can be organized in the same hierarchical index path.

The interface of the tree enables efficient querying of all children of a specific path and verifying that the returned children are the requested nodes. Permissions to add data to the hierarchical index are enforced by the resource logics and do not require additional checks.

## Data blob storage

Data blob storage stores data without preserving any specific structure. The data is represented as a variable length byte array and comes with a deletion criterion that determines for how long the data will be stored. The deletion criterion, in principle, is an arbitrary predicate, which in practice currently is assumed to be instantiated by one of the following options:

1. delete after $block$
2. delete after $timestamp$
3. delete after $sig$ over $data$
4. delete after either predicate $p_1$ or $p_2$ is true; the predicates are instantiated by options from this list
5. store forever


<!--ᚦtags:nits,unstable-->
