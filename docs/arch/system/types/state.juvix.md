
---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.types.state;
    import prelude open;
    import arch.system.types.nullifier open;
    ```

# State

```juvix
type State := mkState {
  -- commitmentAccumulator : CommitmentAccumulator;
  -- secondCommitmentAccumulator : CommitmentAccumulator;
  nullifierSet : Set Nullifier;
  -- hierarchicalIndex : HierarchicalIndex;
  -- dataBlobStorage : DataBlobStorage;
};
```

??? quote "Arguments"

    `commitmentAccumulator`
    : a commitment accumulator that maps timestamps (part of CMtree) onto finite
    field elements

    `secondCommitmentAccumulator`
    : a second commitment accumulator that maps finite field x timestamp pairs
    onto finite field elements

    `nullifierSet` 
    : a nullifier set that is a map from a finite field element to a finite
    field element

    `hierarchicalIndex`
    : a hierarchical index that is a chained hash set that maps tree paths to
    finite field elements

    `dataBlobStorage`
    : a data blob storage that is a key-value store mapping finite field
    elements to (variable length byte array, deletion criterion) pairs

    `deletionCriteria`
    : a deletion criterion.

??? quote "Auxiliary Juvix code"

    ```juvix
    deriving
    instance
    stateEq : Eq State;
    ```

    ```juvix
    deriving
    instance
    stateOrd : Ord State;
    ```

