---
icon: material/database
search:
  exclude: false
categories:
- resource-machine
tags:
- data-structures
---

??? quote "Juvix imports"

    ```juvix
    module arch.system.state.resource_machine.prelude;
    import prelude open;
    import arch.node.types.crypto open using {Digest};
    ```

## Overview

This file defines the core data structures and traits (interfaces) used by the Resource Machine (RM).

The RM uses three main container types:

- `Set`: Stores unique items like resource commitments and nullifiers.
- `Map`: Holds key-value pairs, such as environment references or application data.
- `List`: Keeps ordered sequences, like proofs or resources.

Additionally, the RM requires several traits for its data structures listed
below.

- `FixedSize`: Ensures that certain types have a fixed bit length.
- `Arithmetic`: Provides basic arithmetic operations, inheriting from `FixedSize`.
- `Hash`: Defines hashing functionality, inheriting from `FixedSize`.
- `ISet`: An interface defining standard set operations.
- `IOrderedSet`: Extends `ISet` to maintain elements in a specific order.
- `IMap`: An interface defining standard map operations.

### Aliases

The RM frequently uses hashes for commitments and nullifiers.

There are a variety of hashes of unspecified character appearing in the RM which
we declare here as aliases of `Digest`.

#### `ValueHash`

```juvix
syntax alias ValueHash := Digest;
```

#### `DeltaHash`

```juvix
syntax alias DeltaHash := Digest;
```

#### `LabelHash`

```juvix
syntax alias LabelHash := Digest;
```

#### `LogicHash`

```juvix
syntax alias LogicHash := Digest;
```

#### `KindHash`

```juvix
syntax alias KindHash := Digest;
```

#### `ExtraInput`

```juvix
syntax alias ExtraInput := ByteString;
```

#### `Quantity`

There are two numeric types of unspecified character mentioned in the RM, which
we declare here as aliases to `Nat`.

```juvix
syntax alias Quantity := Nat;
```

#### `Balance`

```juvix
syntax alias Balance := Nat;
```

#### `Nonce`

The RM specs reference a `Nonce` type which is left undefined.
Let's define it as a some kind of `Nat` for now, as we later need to have a
`Eq` instance for it.

```juvix
type Nonce := mkNonce@{
  nonce : Nat;
};
```

```juvix
deriving
instance
eqNonce : Eq Nonce;

deriving
instance
ordNonce : Ord Nonce;
```

#### `RandSeed`

The RM specs reference a `RandSeed` type which is left undefined.

```juvix
axiom RandSeed : Type;
```

### `FixedSize` Trait

The `FixedSize` trait ensures that certain types have a fixed bit
length, which is essential for resource integrity and security.

```juvix
trait
type FixedSize A :=
  mkFixedSize@{
    bitSize : Nat;
  };
```

#### `FixedSize` instance for `Nat`

An instance of `FixedSize` for natural numbers with a bit size of 256.

```juvix
instance
fixedSizeNat256 : FixedSize Nat :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### `FixedSize` instance for `ByteString`

An instance of `FixedSize` for bytestrings with a bit size of 256.

```juvix
instance
fixedSizeByteString256 : FixedSize ByteString :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### `FixedSize` instance for `Nonce`

An instance of `FixedSize` for nonces with a bit size of 256.

```juvix
instance
fixedSizeNonce256 : FixedSize Nonce :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### `FixedSize` instance for `RandSeed`

An instance of `FixedSize` for random seeds with a bit size of 256.

```juvix
instance
fixedSizeRandSeed256 : FixedSize RandSeed :=
  mkFixedSize@{
    bitSize := 256
  };
```

### `Arithmetic` Trait

The `Arithmetic` trait defines addition and subtraction operations. It requires
a `FixedSize` instance.

```juvix
trait
type Arithmetic A :=
  mkArithmetic@{
    {{fixedSize}} : FixedSize A;
    add : A -> A -> A;
    sub : A -> A -> A;
  };
```

#### `Arithmetic` instance for `Nat`

An instance of `Arithmetic` for natural numbers.

```juvix
instance
arithmeticNat : Arithmetic Nat :=
  mkArithmetic@{
    add := \{x y := x + y};
    sub := sub
  };
```

### `Hash` Trait

The `Hash` trait provides a standardized interface for hashing
operations within the RM. It implies `FixedSize` as we will always
assume that's present when using a `Hash` instance.

```juvix
trait
type Hash H :=
  mkHash@{
    {{fixedSize}} : FixedSize H;
    hash : H -> Digest;
  };
```

#### `Hash` instance for `Nat`

Assuming `Nat` can be directly hashed, we provide an instance of `Hash` for it.

```juvix
axiom computeNatHash : Nat -> Digest;
```

```juvix
instance
hashNat : Hash Nat :=
  mkHash@{
    fixedSize := fixedSizeNat256;
    hash := computeNatHash
  };
```

#### `Hash` instance for `ByteString`

Assuming `ByteString` can be directly hashed, we provide an instance of `Hash` for it.

```juvix
axiom computeByteStringHash : ByteString -> Digest;
```

```juvix
instance
hashByteString : Hash ByteString :=
  mkHash@{
    fixedSize := fixedSizeByteString256;
    hash := computeByteStringHash
  };
```

### `ISet` Trait

The `ISet` trait defines the essential operations for set manipulation,
defining a standard interface for any `Set` implementation used by the RM.
The type parameter `S` is the set type, and `A` is the element type.

```juvix
trait
type ISet S A :=
  mkISet@{
    newSet : S;
    size : S -> Nat;
    insert : A -> S -> S;
    union : S -> S -> S;
    intersection : S -> S -> S;
    difference : S -> S -> S;
    contains : A -> S -> Bool;
  };
```

#### `ISet` instance for Prelude's `Set`

An instance of `ISet` for the standard `Set` type.

```juvix
instance
iSetForStdSet
  {A} {{Ord A}} : ISet (Set A) A :=
  mkISet@{
    newSet := Set.empty;
    size := Set.size;
    insert := Set.insert;
    union := Set.union;
    intersection := Set.intersection;
    difference := Set.difference;
    contains := Set.isMember
  };
```

### `IOrderedSet` Trait

`IOrderedSet` is intended to represent a list without repeated elements;
that is, a set equipped with a permutation. The interface is left mostly
unspecified. Details are not given in the original RM specs, so this is
a speculative interface.

```juvix
trait
type IOrderedSet S A :=
  mkIOrderedSet@{
    {{iset}} : ISet S A;
    -- Returns elements in order as a list
    toList : S -> List A;
    -- Creates from a list, preserving order of first occurrence
    fromList : List A -> S;
  };
```

### `OrderedSet`

An ordered set as a regular set plus a list of indices defining the permutation.

```juvix
type OrderedSet A := mkOrderedSet {
  elements : Set A;
  permutation : List Nat -- List of indices
};
```

#### `setToListWithPerm`

```juvix
setToListWithPerm
  {A} {{Ord A}}
  (indices : List Nat)
  (elements : Set.Set A) : List A :=
  let
    -- First convert set to sorted list
    sorted : List A := Set.toList elements;
    -- Then map each index to the element at that position
    access (index : Nat) : Option A :=
      case splitAt index sorted of {
        | (mkPair _ (x :: _)) := some x
        | (mkPair _ _) := none
      }
  in catOptions (map access indices);
```

#### `orderedSetToList`

```juvix
orderedSetToList
  {A} {{Ord A}}
  (s : OrderedSet A) : List A :=
  setToListWithPerm (OrderedSet.permutation s) (OrderedSet.elements s);
```

#### `findPosition`

Find position where `x` would go in sorted order

```juvix
findPosition
  {A} {{Ord A}}
  (x : A) (elements : Set.Set A) : Nat :=
  let
    sorted : List A := Set.toList elements;
    go : List A -> Nat
      | [] := 0
      | (y :: ys) :=
        if | (x <= y) := 0
           | else := suc (go ys);
  in go sorted;
```

#### `orderedSetFromList`

```juvix
orderedSetFromList
  {A} {{Ord A}} : List A -> OrderedSet A :=
    foldl
      (\{acc x :=
        if | (Set.isMember x (OrderedSet.elements acc)) := acc
           | else := let pos := findPosition x (OrderedSet.elements acc)
                     in mkOrderedSet
                          (Set.insert x (OrderedSet.elements acc))
                          ((OrderedSet.permutation acc) ++ [pos])})
    (mkOrderedSet Set.empty []);
```

#### `IOrderedSet` instance for `OrderedSet`

```juvix
instance
orderedSetInstance
  {A} {{Ord A}} : IOrderedSet (OrderedSet A) A :=
  mkIOrderedSet@{
    -- ISet instance
    iset := mkISet@{
      newSet := mkOrderedSet Set.empty [];
      size := \{s := Set.size (OrderedSet.elements s)};
      insert := \{x s :=
        if | (Set.isMember x (OrderedSet.elements s)) := s
           | else := mkOrderedSet
                      (Set.insert x (OrderedSet.elements s))
                      ((OrderedSet.permutation s) ++ [Set.size (OrderedSet.elements s)])
      };
      -- Union
      union := \{s1 s2 := orderedSetFromList (orderedSetToList s1 ++
      orderedSetToList s2)};

      -- Intersection
      intersection := \{s1 s2 :=
        orderedSetFromList (filter (\{x := Set.isMember x (OrderedSet.elements s2)}) (orderedSetToList s1))
      };

      -- Difference
      difference := \{s1 s2 :=
        orderedSetFromList (filter (\{x := not (Set.isMember x (OrderedSet.elements s2))}) (orderedSetToList s1))
      };

      -- Contains
      contains := \{x s := Set.isMember x (OrderedSet.elements s)}
    };

    -- toList
    toList := orderedSetToList;

    -- fromList
    fromList := orderedSetFromList;
  };
```

### `IMap` Trait

The `IMap` trait defines the standard operations for map manipulation,
defining a standard interface for any Map implementation used by the RM.

```juvix
trait
type IMap M K V :=
  mkIMap@{
    emptyMap : M;
    insert : K -> V -> M -> M;
    lookup : K -> M -> Option V;
    delete : K -> M -> M;
    keys : M -> List K;
    values : M -> List V;
  };
```

#### `IMap` instance for Prelude's `Map`

An instance of `IMap` for the standard `Map` type.

```juvix
instance
iMapForStdMap
  {K} {{Ord K}} {V : Type} : IMap (Map K V) K V :=
  mkIMap@{
    emptyMap := Map.empty;
    insert := \{k v m := Map.insert k v m};
    lookup := \{k m := Map.lookup k m};
    delete := \{k m := Map.delete k m};
    keys := \{m := Map.keys m};
    values := \{m := Map.values m}
  };
```
