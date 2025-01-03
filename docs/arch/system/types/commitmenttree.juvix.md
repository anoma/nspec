---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - commitment-tree
  - merkle-tree
  - cryptographic-accumulator
  - state
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.commitmenttree;
    import prelude open;
    import arch.node.types.crypto open;
    import arch.system.types.commitment open;
    ```

# Commitment Trees

## Purpose

Commitment trees are a tree-like data structure that stores [[Commitment|commitments]] and
provide a way to efficiently store, retrieve those commitments, and verify
their inclusion in the tree.

Commitment trees are part of the [[State|state]] in the system.

## `CommitmentTreeOps`

The `CommitmentTreeOps` trait defines the stateless operations that a tree that
stores commitments must implement.

The `CommitmentTreeOps` type has the following type parameters:

- `A` : The type of the data that is being committed.
- `Tree` : The type of the tree that stores the commitments.
- `P` : The type of the path that is used to navigate through the tree.

```juvix
trait
type CommitmentTreeOps A (Tree : Type -> Type) P :=
  mkCommitmentTreeOps@{
    hashRoot : Tree A -> Digest;
    add : A -> Tree A -> Pair (Tree A) P;
    read : P -> Tree A -> Option (Commitment A);
    verify : P -> Commitment A -> Tree A -> Bool;
  };
```

???+ quote "`CommitmentTreeOps` operations"

    `hashRoot`
    : Returns the hash of the root of the given commitment tree.

    `add` : Adds a commitment to the commitment tree. Returns the new
    commitment tree and the path to the commitment.

    `read`
    : Returns the commitment at a `Path` in the commitment tree.

    `verify`
    : Verifies if a commitment is at a `Path` in the commitment tree.

## An instance of `CommitmentTreeOps`

We now define an instance of a `CommitmentTreeOps` for the `CTree` type.
Trees of this type can be used as *default* cryptographic accumulators.

The `CTree` type is defined as a specialised `MTree`, a general type of tree
that can be used as a cryptographic accumulator.

### `MTree`

A `MTree` is a data structure that accumulates the output related to the values
of its children in the node `merge`. In the leaves, we store the some particular
data.

```juvix
type MTree A B :=
  | mkMTreeLeaf@{ value : A }
  | mkMTreeNode@{
      merge : B;
      left : MTree A B;
      right : MTree A B }
  ;
```

???+ quote "`MTree` constructors"

    `mkMTreeLeaf`
    : A leaf node in the tree which stores some particular data.

    `mkMTreeNode`
    : An internal node in the tree which stores the merge of the two sub-trees,
      and the two sub-trees themselves.

### `CTree`

Trees of type `CTree` are specialised `MTree` where the leaf nodes store
[[Commitment|`Commitment` values]] and the internal nodes store [[hashes]],
precisely. These hashes, `Digest` values, in the internal nodes represent the
combined hash of their child nodes.

```juvix
CTree (A : Type) : Type := MTree (Commitment A) Digest;
```

Let us now define the `treeHash` function which computes the hash of a `CTree`.

```juvix
treeHash {A} (tree : CTree A) : Digest :=
  case tree of {
    | (mkMTreeLeaf@{ value := c }) := Commitment.commitment c
    | (mkMTreeNode@{ merge := digest}) := digest
  }
```

To retrieve commitments from a `CTree`, we need to define a *path* which is a
sequence of directions used to navigate through the tree.

### `PathDir`

A *path* is a sequence of `PathDir` values used to navigate through a tree such
as a `CTree` by specifying the direction to take at each node.

```juvix
type PathDir :=
  | PathDirLeft
  | PathDirRight
  | PathDirHere;
```

### `CTreePath`

A `CTreePath` is a sequence of `PathDir` values used to navigate through a `CTree`.

```juvix
CTreePath : Type := List PathDir;
```

### A `CTree` is a commitment tree

```
-- instance
thisShouldWork {A}: CommitmentTreeOps A CTree CTreePath :=
  mkCommitmentTreeOps@{
    hashRoot {A} (tree : CTree A) : Digest :=
      case tree of {
        | (mkMTreeNode@{ merge := digest}) := digest
        | (mkMTreeLeaf@{ value :=
          (mkCommitment@{ commitment := c }) }) := c
      };
    add := undef;
    read := undef;
    verify := undef;
  };
```