---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - commitment-tree
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

## `MTree`

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
## `CTree`

The `CTree` type is formally defined as a specialised `MTree` where the leaf
nodes store [[Commitment|`Commitment` values]] and the internal nodes store
[[hashes]], precisely. These hashes, `Digest` values, in the internal nodes
represent the combined hash of their child nodes. See *merkle trees* for more
information.

```juvix
CTree (A : Type) : Type := MTree (Commitment A) Digest;
```

## `Path`

A *path* is a sequence of `PathDir` values used to navigate through a `CTree` by
specifying the direction to take at each node.

### `PathDir`

```juvix
type PathDir :=
  | PathDirLeft
  | PathDirRight
  | PathDirHere;
```

```juvix
Path : Type := List PathDir;
```

## `CommitmentTree`

A *commitment tree* is a read-append-only structure that allows you to store
commitments, and to verify that a commitment is in the tree.

```juvix
trait
type CommitmentTree A :=
  mkCommitmentTree@{
    add : Commitment A -> CTree A -> Path;
    path : Commitment A -> CTree A -> Option Path;
    hashRoot : CTree A -> Digest;
    verify : Path -> Commitment A ->  Bool;
  };
```

???+ quote "`CommitmentTree` constructors"

    `add`
    : Adds a `Commitment` to the `CommitmentTree`.

    `path`
    : Returns the `Path` to a `Commitment` in the `CommitmentTree`.

    `hashRoot`
    : Returns the `Digest` of the root of the `CommitmentTree`.

    `verify`
    : Verifies a `Path` of a `Commitment` in the `CommitmentTree`.

### `CommitmentTree` instance

In particular, a `CTree` is an instance of the `CommitmentTree` trait.

!!! todo

    Update the definitions below for CTree.

#### `addToMTree`

```
terminating
addToMTree {A} (tree : MTree A) (a : A) : MTree A :=
  case tree of {
  | MTreeLeaf rval := MTreeNode (MTreeLeaf a) (MTreeLeaf rval)
  | MTreeNode lTree rTree := MTreeNode (addToMTree lTree a) rTree
  }
```

#### `getMTreePath`

```
terminating -- TODO: it's failing to see that the function is terminating
getMTreePath {A} {{Eq A}} (tree : MTree A) (a : A) : Option Path :=
  case tree of {
  |  (MTreeLeaf rval) :=
        if  | a == rval := some [PathDirHere]
            | else := none
  | (MTreeNode lTree rTree) :=
        case getMTreePath lTree a of {
          | some lPath := some (PathDirLeft :: lPath)
          | none :=
            case getMTreePath rTree a of {
              | some rPath := some (PathDirRight :: rPath)
              | none := none
            }
        }
  }
```