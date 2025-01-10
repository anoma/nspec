---
icon: material/database
search:
  exclude: false
categories:
- resource machine
tags:
- data structures
---

??? quote "Juvix imports"
    ```juvix
    module arch.resource_machine.DataStructures;

    import prelude open;
    ```

## Overview

This file centralizes the essential data structures and their associated
traits that the Resource Machine (RM) relies on.

The RM utilizes the following primary containers and their operations:

- **Set**: To store unique items like resource commitments and nullifiers.
- **Map**: For key-value associations, such as environment references or application data.
- **List**: For ordered sequences, such as enumerating proofs or iterating over resources.

The resource machine (RM) uses various containers—`Set`, `Map`, `List`—from the 
prelude. However, certain interfaces like `ISet` or an ordered-set trait aren't 
already present in the library, and the RM references them in older planning or 
discussions. This file collects **everything** the RM needs regarding data structures.

Above, we **re-import** the standard types/ops that the RM uses and also **provide** 
traits that aren’t in the library. The RM requires specific traits to parameterize by
different potential implementations of these containers.

- **FixedSize**: Ensures that certain types have a fixed bit length.
- **Arithmetic**: Provides basic arithmetic operations, inheriting from `FixedSize`.
- **Hash**: Defines hashing functionality, inheriting from `FixedSize`.
- **ISet**: An interface defining standard set operations.
- **IOrderedSet**: Extends `ISet` to maintain elements in a specific order.
- **IMap**: An interface defining standard map operations.

### Aliases

#### Hash Aliases

The RM frequently uses hashes for commitments and nullifiers. To standardize the hash type across the RM, we define a `Digest` alias.

```juvix
syntax alias Digest := ByteString;
```

There are a variety of hashes of unspecified character appearing in the RM which
we declare here as aliases to `ByteString`.

```juvix
syntax alias ValueHash := ByteString;
syntax alias DeltaHash := ByteString;
syntax alias LabelHash := ByteString;
syntax alias LogicHash := ByteString;
```

#### Numeric Aliases

There are two numeric types of unspecified character mentioned in the RM, which
we declare here as aliases to `Nat`.

```juvix
syntax alias Quantity := Nat;
syntax alias Balance := Nat;
```

#### Unspecified Types

The RM specs reference a "Nonce" type which is left undefined.

```juvix
axiom Nonce : Type;
```

The RM specs reference a "RandSeed" type which is left undefined.

```juvix
axiom RandSeed : Type;
```

### FixedSize Trait

The `FixedSize` trait ensures that certain types have a fixed bit 
length, which is essential for resource integrity and security.

```juvix
trait
type FixedSize (A : Type) :=
  mkFixedSize@{
    bitSize : Nat;
  };
```

#### Instance for Nat

An instance of `FixedSize` for natural numbers with a bit size of 256.

```juvix
instance
fixedSizeNat256 : FixedSize Nat :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### Instance for ByteString

An instance of `FixedSize` for bytestrings with a bit size of 256.

```juvix
instance
fixedSizeByteString256 : FixedSize ByteString :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### Instance for Nonce

An instance of `FixedSize` for nonces with a bit size of 256.

```juvix
instance
fixedSizeNonce256 : FixedSize Nonce :=
  mkFixedSize@{
    bitSize := 256
  };
```

#### Instance for RandSeed

An instance of `FixedSize` for random seeds with a bit size of 256.

```juvix
instance
fixedSizeRandSeed256 : FixedSize RandSeed :=
  mkFixedSize@{
    bitSize := 256
  };
```

### Arithmetic Trait

The `Arithmetic` trait defines basic arithmetic operations required
by the RM, such as addition and subtraction. It implies `FixedSize`
as we will always assume that's present when using an `Arithmetic`
instance.

```juvix
trait
type Arithmetic (A : Type) :=
  mkArithmetic@{
    {{fixedSize}} : FixedSize A;
    add : A -> A -> A;
    sub : A -> A -> A;
  };
```

#### Instance for Nat

An instance of `Arithmetic` for natural numbers.

```juvix
instance
arithmeticNat : Arithmetic Nat :=
  mkArithmetic@{
    add := \{x y := x + y};
    sub := sub
  };
```

### Hash Trait

The `Hash` trait provides a standardized interface for hashing 
operations within the RM. It implies `FixedSize` as we will always
assume that's present when using an `Hash` instance.

```juvix
trait
type Hash (H : Type) :=
  mkHash@{
    {{fixedSize}} : FixedSize H;
    hash : H -> Digest;
  };
```

#### Instance for Nat

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

#### Instance for ByteString

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

### ISet Trait

The `ISet` trait defines the essential operations for set manipulation,
defining a standard interface for any Set implementation used by the RM.

```juvix
trait
type ISet (S : Type) (A : Type) :=
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

#### Instance for Prelude's Set

An instance of `ISet` for the standard `Set` type.

```juvix
instance
iSetForStdSet {A : Type} {{Ord A}} : ISet (Set A) A :=
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

### IOrderedSet Trait

`IOrderedSet` is intended to represent a list without repeated elements; 
that is, a set equipped with a permutation. The interface is left mostly
unspecified. Details are not given in the original RM specs, so this is
a speculative interface.

```juvix
trait
type IOrderedSet (S : Type) (A : Type) :=
  mkIOrderedSet@{
    {{iset}} : ISet S A;
    -- Returns elements in order as a list
    toList : S -> List A;
    -- Creates from a list, preserving order of first occurrence
    fromList : List A -> S;
  };
```

### Instance for Set + Permutation

An ordered set as a regular set plus a list of indices defining the permutation.

```juvix
type OrderedSet (A : Type) := mkOrderedSet {
  elements : Set A;
  permutation : List Nat -- List of indices
};
```

```juvix
setToListWithPerm {A} {{Ord A}} (indices : List Nat) (elements : Set.Set A) : List A :=
  let
    -- First convert set to sorted list
    sorted : List A := Set.toList elements;
    -- Then map each index to the element at that position
    access (index : Nat) : Option A := 
      case splitAt index sorted of {
        | (mkPair _ (x :: _)) := some x
        | (mkPair _ _) := none
      }
  in catMaybes (map access indices);

orderedSetToList {A} {{Ord A}} (s : OrderedSet A) : List A := 
  setToListWithPerm (OrderedSet.permutation s) (OrderedSet.elements s);

-- Find position where x would go in sorted order
findPosition {A} {{Ord A}} (x : A) (elements : Set.Set A) : Nat :=
  let
    sorted : List A := Set.toList elements;
    go : List A -> Nat
      | [] := 0
      | (y :: ys) := 
        if | (x <= y) := 0
           | else := suc (go ys);
  in go sorted;

orderedSetFromList {A} {{Ord A}} : List A -> OrderedSet A := 
  foldl 
    (\{acc x := if | (Set.isMember x (OrderedSet.elements acc)) := acc
                   | else := let pos := findPosition x (OrderedSet.elements acc)
                             in mkOrderedSet 
                                  (Set.insert x (OrderedSet.elements acc)) 
                                  ((OrderedSet.permutation acc) ++ [pos])})
    (mkOrderedSet Set.empty []);

instance
orderedSetInstance {A} {{Ord A}} : IOrderedSet (OrderedSet A) A :=
  mkIOrderedSet@{
    iset := mkISet@{
      newSet := mkOrderedSet Set.empty [];
      size := \{s := Set.size (OrderedSet.elements s)};
      insert := \{x s := 
        if | (Set.isMember x (OrderedSet.elements s)) := s
           | else := mkOrderedSet 
                      (Set.insert x (OrderedSet.elements s))
                      ((OrderedSet.permutation s) ++ [Set.size (OrderedSet.elements s)])
      };
      union := \{s1 s2 := orderedSetFromList (orderedSetToList s1 ++ orderedSetToList s2)};
      intersection := \{s1 s2 := 
        orderedSetFromList (filter (\{x := Set.isMember x (OrderedSet.elements s2)}) (orderedSetToList s1))
      };
      difference := \{s1 s2 := 
        orderedSetFromList (filter (\{x := not (Set.isMember x (OrderedSet.elements s2))}) (orderedSetToList s1))
      };
      contains := \{x s := Set.isMember x (OrderedSet.elements s)}
    };
    toList := orderedSetToList;
    fromList := orderedSetFromList;
  };
```

### IMap Trait

The `IMap` trait defines the standard operations for map manipulation, 
defining a standard interface for any Map implementation used by the RM.

```juvix
trait
type IMap (M : Type) (K : Type) (V : Type) :=
  mkIMap@{
    emptyMap : M;
    insert : K -> V -> M -> M;
    lookup : K -> M -> Option V;
    delete : K -> M -> M;
    keys : M -> List K;
    values : M -> List V;
  };
```

#### Instance for Prelude's Map

An instance of `IMap` for the standard `Map` type.

```juvix
instance
iMapForStdMap {K : Type} {{Ord K}} {V : Type} : IMap (Map K V) K V :=
  mkIMap@{
    emptyMap := Map.empty;
    insert := \{k v m := Map.insert k v m};
    lookup := \{k m := Map.lookup k m};
    delete := \{k m := Map.delete k m};
    keys := \{m := Map.keys m};
    values := \{m := Map.values m}
  };
```
