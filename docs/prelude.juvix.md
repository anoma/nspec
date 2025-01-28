---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Juvix-Types
- Juvix-Prelude
---

??? quote "Juvix imports"

    ```juvix
    module prelude;
    import Stdlib.Trait open public;
    import Stdlib.Trait.Ord open using {Ordering; mkOrd; Equal; isEqual} public;
    import Stdlib.Trait.Eq open using {Eq; mkEq; ==} public;
    import Stdlib.Debug.Fail open using {failwith};
    import Stdlib.Data.Fixity open public;
    ```

# Juvix Specs Prelude

The following are frequent and basic abstractions used in the Anoma
specification.

## Combinators

```juvix
import Stdlib.Function open
  using {
    <<;
    >>;
    const;
    id;
    flip;
    <|;
    |>;
    iterate;
    >->;
  }
```

## Useful Type Classes

### `Functor`

```juvix
import Stdlib.Trait.Functor.Polymorphic as Functor;
```

### `Applicative`

```juvix
import Stdlib.Trait.Applicative open using {Applicative; mkApplicative} public;
open Applicative public;
```

### `Monad`

```juvix
import Stdlib.Trait.Monad open using {Monad; mkMonad} public;
open Monad public;
```

#### `join`

Join function for monads

```juvix
join
  {M : Type -> Type}
  {A}
  {{Monad M}}
  (mma : M (M A)) : M A :=
  bind mma id;  -- using the built-in `bind`
```

### `Bifunctor`

Two-argument functor

```juvix
trait
type Bifunctor (F : Type -> Type -> Type) :=
  mkBifunctor@{
    bimap {A B C D} :  (A -> C) -> (B -> D) -> F A B -> F C D
  };
```

### `AssociativeProduct`

Product with associators

```juvix
trait
type AssociativeProduct (F : Type -> Type -> Type) :=
  mkAssociativeProduct@{
    assocLeft {A B C} : F A (F B C) -> F (F A B) C;
    assocRight {A B C} : F (F A B) C -> F A (F B C)
  };
```

### `CommutativeProduct`

Product with commuters

```juvix
trait
type CommutativeProduct (F : Type -> Type -> Type) :=
  mkCommutativeProduct@{
    swap {A B} : F A B -> F B A;
  };
```

### `UnitalProduct`

Product with units

```juvix
trait
type UnitalProduct U (F : Type -> Type -> Type) :=
  mkUnitalProduct@{
    unitLeft {A} : A -> F U A;
    unUnitLeft {A} : F U A -> A;
    unitRight {A} : A -> F A U;
    unUnitRight {A} : F A U -> A;
  };
```

### `Traversable`

Traversable type class.

```juvix
trait
type Traversable (T : Type -> Type) :=
  mkTraversable@{
    {{functorI}} : Functor T;
    {{foldableI}} : Polymorphic.Foldable T;
    sequence :
      {F : Type -> Type} ->
      {A : Type} ->
      {{Applicative F}} ->
      T (F A) -> F (T A);
    traverse :
      {F : Type -> Type} ->
      {A B : Type} ->
      {{Applicative F}} ->
      (A -> F B) -> T A -> F (T B);
  };
```

## Bool

The type `Bool` represents boolean values (`true` or `false`). Used for logical operations and conditions.

```juvix
import Stdlib.Data.Bool as Bool
  open using
  { Bool;
    true;
    false;
    &&;
    ||;
    not;
    or;
    and;
  } public;
```

For example,

```juvix
verdad : Bool := true;
```

### `xor`

Exlusive or

```juvix
xor (a b : Bool) : Bool :=
  if
    | a := not b
    | else := b
  ;
```

### `nand`

Not and

```juvix
nand (a b : Bool) : Bool := not (and a b);
```

### `nor`

Not or

```juvix
nor (a b : Bool) : Bool := not (or a b);
```

## Nat

The type `Nat` represents natural numbers (non-negative integers). Used for
counting and indexing.

```juvix
import Stdlib.Data.Nat as Nat
  open using
  { Nat;
    zero;
    suc;
    natToString;
    +;
    sub;
    *;
    div;
    mod;
    ==;
    <=;
    >;
    <;
    min;
    max;
  } public;
```

For example,

```juvix
ten : Nat := 10;
```

### `pred`

Predecessor function for natural numbers.

```juvix
pred (n : Nat) : Nat :=
  case n of {
    | zero := zero
    | suc k := k
  };
```

### `boolToNat`

Convert boolean to a Bool to a Nat in the standard way of circuits.

```juvix
boolToNat (b : Bool) : Nat :=
  if
    | b := 0
    | else := 1
  ;
```

### `isZero`

Check if a natural number is zero.

```juvix
isZero (n : Nat) : Bool :=
  case n of {
    | zero := true
    | suc k := false
  };
```

### `isEven` and `isOdd`

Parity checking functions

```juvix
isEven (n : Nat) : Bool := mod n 2 == 0;
```

```juvix
isOdd (n : Nat) : Bool := not (isEven n);
```

### `foldNat`

Fold over natural numbers.

```juvix
terminating
foldNat {B} (z : B) (f : Nat -> B -> B) (n : Nat) : B :=
  case n of {
    | zero := z
    | suc k := f k (foldNat z f k)
  };
```

### `iter`

Iteration of a function.

```juvix
iter {A} (f : A -> A) (n : Nat) (x : A) : A :=
  foldNat x \{_ y := f y} n;
```

### `exp`

The exponentiation function.

```juvix
exp (base : Nat) (exponent : Nat) : Nat :=
  iter \{product := base * product} exponent 1;
```

### `factorial`

The factorial function.

```juvix
factorial : Nat -> Nat := foldNat 1 \{k r := suc k * r};
```

### `gcd`

Greatest common divisor function.

```juvix
terminating
gcd (a b : Nat) : Nat :=
  case b of {
    | zero := a
    | suc _ := gcd b (mod a b)
  };
```

### `lcm`

Least common multiple function.

```juvix
lcm (a b : Nat) : Nat :=
  case b of {
    | zero := zero
    | suc _ :=
      case a of {
        | zero := zero
        | suc _ := div (a * b) (gcd a b)
      }
    };
```

## String

The type `String` represents sequences of characters. Used for text and
communication.

```juvix
import Stdlib.Data.String
  as String
  open using
  { String;
    ++str;
  } public;
```

For example,

```juvix
hello : String := "Hello, World!";
```

### String Comparison

```juvix
axiom stringCmp : String -> String -> Ordering;

instance
StringOrd : Ord String :=
  mkOrd@{
    cmp := stringCmp;
  };
```

## ByteString

```juvix
ByteString : Type := String;
```

A basic type for representing binary data.

```juvix
emptyByteString : ByteString := "";
```

## Unit

The type `Unit` represents a type with a single value. Often used when a
function does not return any meaningful value.

```juvix
import Stdlib.Data.Unit
  as Unit
  open using {
    Unit;
    unit
  } public;
```

For example,

```juvix
unitValue : Unit := unit;
```

### `trivial`

Unique function to the unit. Universal property of terminal object.

```juvix
trivial {A} : A -> Unit := const unit;
```

## Empty

The type `Empty` represents a type with a single value. Often used when a
function does not return any meaningful value.

```juvix
axiom Empty : Type;
```

### `explode`

Unique function from empty. Universal property of initial object.

```juvix
axiom explode {A} : Empty -> A;
```

## Pair A B

The type `Pair A B` represents a tuple containing two elements of types `A` and
`B`. Useful for grouping related values together.

```juvix
import Stdlib.Data.Pair as Pair;
open Pair using { Pair } public;
open Pair using { , };

import Stdlib.Data.Pair as Pair
  open using
  { ordProductI;
    eqProductI
  } public;
```

```juvix
import Stdlib.Data.Fixity open;
syntax operator mkPair none;
syntax alias mkPair := ,;
```

For example,

```juvix
pair : Pair Nat Bool := mkPair 42 true;
```

### `fst` and `snd`

Projections

```juvix
fst {A B} : Pair A B -> A
  | (mkPair a _) := a;
```

```juvix
snd {A B} : Pair A B -> B
  | (mkPair _ b) := b;
```

### `PairCommutativeProduct`

Swap components

```juvix
instance
PairCommutativeProduct : CommutativeProduct Pair :=
  mkCommutativeProduct@{
    swap := \{p := mkPair (snd p) (fst p)}
  };
```

### `PairAssociativeProduct`

Pair associations

```juvix
instance
PairAssociativeProduct : AssociativeProduct Pair :=
  mkAssociativeProduct@{
    assocLeft := \{p :=
      let pbc := snd p;
      in mkPair (mkPair (fst p) (fst pbc)) (snd pbc)
    };
    assocRight := \{p :=
      let pab := fst p;
      in mkPair (fst pab) (mkPair (snd pab) (snd p))
    }
  };
```

### `PairUnitalProduct`

Unit maps for pairs and units

```juvix
instance
PairUnitalProduct : UnitalProduct Unit Pair :=
  mkUnitalProduct@{
    unitLeft := \{a := mkPair unit a};
    unUnitLeft := snd;
    unitRight := \{a := mkPair a unit};
    unUnitRight := \{{A} := fst};
  };
```

### `PairBifunctor`

Map functions over pairs

```juvix
instance
PairBifunctor : Bifunctor Pair :=
  mkBifunctor@{
    bimap := \{f g p := mkPair (f (fst p)) (g (snd p))};
  };
```

### `fork`

Universal property of pairs

```juvix
fork
  {A B C}
  (f : C -> A)
  (g : C -> B)
  (c : C) : Pair A B :=
  mkPair (f c) (g c);
```

## Result A B

The `Result A B` type represents either a success with a value of `ok x` with
`x` of type `A` or an error with value `error e` with `e` of type `B`.

```juvix
import Stdlib.Data.Result.Base as Result;
open Result using { Result; ok; error } public;
```

## Either A B

The type `Either A B`, or sum type of `A` and `B`, represents a value of type
`A` or `B`. It is equivalent to `Result A B`, however, the meaning of the values
is different. There is no such thing as an error or success value in the
`Either` type, instead the values are either `left a` of type `A` or `right b`
of type `B`.

```juvix
syntax alias Either := Result;
syntax alias left := error;
syntax alias right := ok;
```

For example,

```juvix
thisString : Either String Nat := left "Error!";
thisNumber : Either String Nat := right 42;
```

### `isLeft` and `isRight`

Check components of either.

```juvix
isLeft {A B} (e : Either A B) : Bool :=
  case e of {
    | left _ := true
    | right _ := false
  };
```

```juvix
isRight {A B} (e : Either A B) : Bool :=
  case e of {
    | left _ := false
    | right _ := true
  };
```

### `fromLeft`

Get left element (with default)

```juvix
fromLeft {A B} (e : Either A B) (d : A) : A :=
  case e of {
    | (left x) := x
    | (right _) := d
  };
```

### `fromRight`

Get right element (with default)

```juvix
fromRight {A B} (e : Either A B) (d : B) : B :=
  case e of {
    | (left _) := d
    | (right x) := x
  };
```

### `EitherCommutativeProduct`

Swap elements

```juvix
swapEither {A B} (e : Either A B) : Either B A :=
  case e of {
    | (left x) := right x
    | (right x) := left x
  };
```

```juvix
instance
EitherCommutativeProduct : CommutativeProduct Either :=
  mkCommutativeProduct@{
    swap := swapEither;
  };
```

### `EitherBifunctor`

Map onto elements of either

```juvix
eitherBimap
  {A B C D}
  (f : A -> C)
  (g : B -> D)
  (e : Either A B) : Either C D :=
  case e of {
    | (left a) := left (f a)
    | (right b) := right (g b)
  };
```

```juvix
instance
EitherBifunctor : Bifunctor Either :=
  mkBifunctor@{
    bimap := eitherBimap
  };
```

### `EitherUnitalProduct`

Unit maps for Either and Empty

#### `unUnitLeftEither`

```juvix
unUnitLeftEither {A} (e : Either Empty A) : A :=
  case e of {
    | left x := explode x
    | right x := x
  };
```

#### `unUnitRightEither`
```juvix
unUnitRightEither {A} (e : Either A Empty) : A :=
  case e of {
    | left x := x
    | (right x) := explode x
  };
```

#### `EitherUnitalProduct`

Unit maps for Either and Empty

```juvix
instance
EitherUnitalProduct : UnitalProduct Empty Either :=
  mkUnitalProduct@{
    unitLeft := right;
    unUnitLeft := unUnitLeftEither;
    unitRight := \{{A} := left};
    unUnitRight := unUnitRightEither;
  };
```

### `fuse`

Universal property of coproduct

```juvix
fuse
  {A B C}
  (f : A -> C)
  (g : B -> C)
  (e : Either A B) : C :=
  case e of {
    | (left x) := f x
    | (right x) := g x
  };
```

### `EitherAssociativeProduct`

Association functions for either

#### `assocLeftEither`

```juvix
assocLeftEither
  {A B C}
  (e : Either A (Either B C)) : Either (Either A B) C :=
  case e of {
    | (left x) := left (left x)
    | (right ebc) :=
      case ebc of {
        | (left y) := left (right y)
        | (right z) := right z
      }
  };
```

#### `assocRightEither`

```juvix
assocRightEither
  {A B C}
  (e : Either (Either A B) C)
  : Either A (Either B C) :=
  case e of {
    | (left eab) :=
      case eab of {
        | (left x) := left x
        | (right y) := right (left y)
      }
    | (right z) := right (right z)
  };
```

#### `EitherAssociativeProduct`

```juvix
instance
EitherAssociativeProduct : AssociativeProduct Either :=
  mkAssociativeProduct@{
    assocLeft := assocLeftEither;
    assocRight := assocRightEither;
  };
```

## `Option A`

The type `Option A` represents an optional value of type `A`. It can be either
`Some A` (containing a value) or `None` (no value). This type is an alias for
`Maybe A` from the standard library.

```juvix
import Stdlib.Data.Maybe as Maybe;
open Maybe using {
    Maybe;
    just;
    nothing
  };
```

```juvix
syntax alias Option := Maybe;
syntax alias some := just;
syntax alias none := nothing;
```

### `isNone`

Check if an optional value is `none`:

```juvix
isNone {A} (x : Option A) : Bool
  := case x of {
  | none := true
  | some _ := false
  }
```

### `isSome`

Check if an optional value is `some`:

```juvix
isSome {A} (x : Option A) : Bool := not (isNone x);
```

### `fromOption`

Extract the value from an `Option` term:

```juvix
fromOption {A} (x : Option A) (default : A) : A :=
  case x of {
  | none := default
  | some x := x
};
```

### `option`

Map over option with default

```juvix
option
  {A B}
  (o : Option A)
  (default : B)
  (f : A -> B)
  : B :=
  case o of {
    | none := default
    | some x := f x
  };
```

### `filterOption`

Filter option according to predicate

```juvix
filterOption
  {A}
  (p : A -> Bool)
  (opt : Option A) : Option A :=
  case opt of {
    | none := none
    | some x :=
      if
        | p x := some x
        | else := none
  };
```

## List A

The type `List A` represents a _sequence_ of elements of type `A`. Used for collections and ordered data.

```juvix
import Stdlib.Data.List as List
  open using {
  List;
  nil;
  ::;
  isElement;
  head;
  tail;
  length;
  take;
  drop;
  ++;
  reverse;
  any;
  all;
  zip;
  splitAt;
  filter;
} public;
```

For example,

```juvix
numbers : List Nat := 1 :: 2 :: 3 :: nil;
-- alternative syntax:
niceNumbers : List Nat := [1 ; 2 ; 3];
```

### `findIndex`

Get the first index of an element satisfying a predicate if such an index exists and none, otherwise.

```juvix
findIndex {A} (predicate : A -> Bool) : List A -> Option Nat
  | nil := none
  | (x :: xs) :=
    if
      | predicate x := some zero
      | else := case findIndex predicate xs of
        | none := none
        | some i := some (suc i);
```

### `last`

Get last element of a list

```juvix
last {A} (lst : List A) (default : A) : A :=
  head default (reverse lst);
```

### `most`

Get list with last element dropped

```juvix
most {A} (lst : List A) : List A :=
  tail (reverse lst);
```

### `snoc`

Prepend element to a list

```juvix
snoc {A} (xs : List A) (x : A) : List A :=
  xs ++ [x];
```

### `uncons`

Split one layer of list

```juvix
uncons {A} : List A -> Option (Pair A (List A))
  | nil := none
  | (x :: xs) := some (mkPair x xs)
```

### `unsnoc`

Split one layer of list from the end

```juvix
unsnoc {A} : List A -> Option (Pair (List A) A)
  | nil := none
  | (x :: xs) := some (mkPair (most (x :: xs)) (last xs x))
```

### `unfold`

Unfold a list, layerwise

```juvix
terminating
unfold {A B}
  (step : B -> Option (Pair A B))
  (seed : B) : List A :=
  case step seed of
    | none := nil
    | some (x, seed') := x :: unfold step seed';
```

### `unzip`

Unzip a list of pairs into two lists

```juvix
terminating
unzip {A B}
  (xs : List (Pair A B)) : Pair (List A) (List B) :=
  case xs of {
    | nil := mkPair nil nil
    | p :: ps :=
      let unzipped := unzip ps
      in mkPair (fst p :: fst unzipped) (snd p :: snd unzipped)
  };
```

#### `partitionEither`

Partition a list

```juvix
partitionEither
  {A B} (es : List (Either A B)) : Pair (List A) (List B) :=
  foldr
    (\{e acc :=
      case e of {
        | left a := mkPair (a :: (fst acc)) (snd acc)
        | right b := mkPair (fst acc) (b :: (snd acc))
      }})
    (mkPair nil nil)
    es;
```

#### `partitionEitherWith`

```juvix
partitionEitherWith
  {A B C}
  (f : C -> Either A B)
  (es : List C) : Pair (List A) (List B) :=
  partitionEither (map f es);
```

### `catOptions`

Collapse list of options

```juvix
catOptions {A} : List (Option A) -> List A :=
  foldr
    (\{opt acc :=
      case opt of {
        | none := acc
        | some x := x :: acc
      }})
    nil;
```

### `maximumBy`

Get the maximal element of a list.

```juvix
maximumBy {A B} {{Ord B}}
  (f : A -> B)
  (lst : List A)
  : Option A :=
  let maxHelper := \{curr acc :=
    case acc of {
      | none := some curr
      | some maxVal :=
        if
          | f curr > f maxVal := some curr
          | else := some maxVal
    }
  };
  in foldr maxHelper none lst;
```

### `minimumBy`

Get the minimal element of a list.

```juvix
minimalBy {A B} {{Ord B}}
  (f : A -> B)
  (lst : List A)
  : Option A :=
  let minHelper := \{curr acc :=
    case acc of {
      | none := some curr
      | some minVal :=
        if
          | f curr < f minVal := some curr
          | else := some minVal
    }
  };
  in foldr minHelper none lst;
```

### `traversableListI`

Traversable instance for lists

```juvix
instance
traversableListI : Traversable List :=
  mkTraversable@{
    sequence
      {F : Type -> Type}
      {A}
      {{appF : Applicative F}}
      (xs : List (F A)) : F (List A) :=
      let
        cons : F A -> F (List A) -> F (List A)
          | x acc := liftA2 (::) x acc;

        go : List (F A) -> F (List A)
          | nil := pure nil
          | (x :: xs) := cons x (go xs);
      in go xs;

    traverse
      {F : Type -> Type}
      {A B}
      {{appF : Applicative F}}
      (f : A -> F B) (xs : List A) : F (List B) :=
      let
        cons : A -> F (List B) -> F (List B)
          | x acc := liftA2 (::) (f x) acc;

        go : List A -> F (List B)
          | nil := pure nil
          | (x :: xs) := cons x (go xs);
      in go xs;
  };
```

### `chunksOf`

Splits a list into chunks of size `n`. The last chunk may be smaller than `n` if the
length of the list is not divisible by `n`.

Example:

- chunksOf 2 [1;2;3;4;5] = [[1;2]; [3;4]; [5]]

```juvix
terminating
chunksOf {A} : (chunkSize : Nat) -> (list : List A) -> List (List A)
  | zero _ := nil
  | _ nil := nil
  | n xs := take n xs :: chunksOf n (drop n xs);
```

### `sliding`

Returns all contiguous sublists of size `n`. If `n` is larger than the list length,
returns empty list. If `n` is zero, returns empty list.

Example:
- sliding 2 [1;2;3;4] = [[1;2]; [2;3]; [3;4]]

```juvix
sliding {A} : (windowSize : Nat) -> (list : List A) -> List (List A)
  | zero _ := nil
  | n xs :=
    let
      len : Nat := length xs;
      terminating
      go : List A -> List (List A)
        | nil := nil
        | ys :=
          if
            | length ys < n := nil
            | else := take n ys :: go (tail ys);
    in if
      | n > len := nil
      | else := go xs;
```

### `span`

Takes a predicate and a list, and returns a tuple where:

- First element is the longest prefix of the list that satisfies the predicate
- Second element is the remainder of the list

```juvix
span {A} (p : A -> Bool) : List A -> Pair (List A) (List A)
  | nil := mkPair nil nil
  | (x :: xs) :=
    if
      | p x :=
        let
          (ys1, ys2) := span p xs;
        in mkPair (x :: ys1) ys2
      | else := mkPair nil (x :: xs);
```

### `groupBy` and `group`

Groups consecutive elements in a list that satisfy a given equality predicate.

Example:

- groupBy (==) [1;1;2;2;2;3;1;1] = [[1;1];[2;2;2];[3];[1;1]]

```juvix
terminating
groupBy {A} (eq : A -> A -> Bool) : List A -> List (List A)
  | nil := nil
  | (x :: xs) :=
    case span (eq x) xs of
      ys1, ys2 := (x :: ys1) :: groupBy eq ys2;
```

```juvix
group {A} {{Eq A}} : List A -> List (List A) := groupBy (==)
```

#### `nubBy`

Returns a list with duplicates removed according to the given equivalence
function, keeping the first occurrence of each element. Unlike regular ;nub;,
this function allows specifying a custom equality predicate.

Examples:

- nubBy (\{x y := mod x 3 == mod y 3}) [1;2;3;4;5;6] = [1;2;3]
- nub [1;1;2;2;3;3] = [1;2;3]

```juvix
nubBy {A} (eq : A -> A -> Bool) : List A -> List A :=
  let
    -- Checks if an element is already in the accumulator
    elemBy (x : A) : List A -> Bool
      | nil := false
      | (y :: ys) := eq x y || elemBy x ys;

    go : List A -> List A -> List A
      | acc nil := reverse acc
      | acc (x :: xs) :=
        if
          | elemBy x acc := go acc xs
          | else := go (x :: acc) xs;
  in go nil;
```

#### `nub`
```juvix
nub {A} {{Eq A}} : List A -> List A := nubBy (==);
```

### `powerlists`

Generate all possible sublists of a list. Each element can either be included or not.

```juvix
powerlists {A} : List A -> List (List A)
  | nil := nil :: nil
  | (x :: xs) :=
    let
      rest : List (List A) := powerlists xs;
      withX : List (List A) := map ((::) x) rest;
    in rest ++ withX;
```

## `Set A`

The type `Set A` represents a collection of unique elements of type `A`. Used
for sets of values.

```juvix
import Stdlib.Data.Set as Set public;
open Set using {
    Set;
    difference;
    union;
    eqSetI;
    ordSetI;
    isSubset;
  } public;
```

For example,

```juvix
uniqueNumbers : Set Nat := Set.fromList [1 ; 2 ; 2 ; 2; 3];
```

#### `setMap`

```juvix
setMap {A B} {{Ord B}} (f : A -> B) (set : Set A) : Set B :=
  Set.fromList (map f (Set.toList set));
```

#### `setJoin`

Collapse a set of sets into a set

```juvix
setJoin {A} {{Ord A}} (sets : Set (Set A)) : Set A :=
  for (acc := Set.empty) (innerSet in sets) {
    Set.union acc innerSet
  };
```

#### `disjointUnion`

```juvix
--- Computes the disjoint union of two ;Set;s.
disjointUnion {T} {{Ord T}} (s1 s2 : Set T) : Result (Set T) (Set T) :=
  case Set.intersection s1 s2 of
    | Set.empty := ok (Set.union s1 s2)
    | s := error s;
```

#### `symmetricDifference`

Caclulate the symmetric difference of two sets.

```juvix
symmetricDifference
  {A} {{Ord A}} (s1 s2 : Set A) : Set A :=
  let
    in1not2 := difference s1 s2;
    in2not1 := difference s2 s1;
  in union in1not2 in2not1;
```

### `cartesianProduct`

Generate the set of all cartesian products of a set.

```juvix
cartesianProduct
  {A B}
  {{Ord A}} {{Ord B}}
  (s1 : Set A)
  (s2 : Set B)
  : Set (Pair A B) :=
  let
    -- For a fixed element from set1, create a set of all pairs with elements from s2
    pairsForElement (a : A) : Set (Pair A B) :=
      for (acc := Set.empty) (b in s2) {
        Set.insert (mkPair a b) acc
      };

    -- Create set of sets, each containing pairs for one element from s1
    pairSets : Set (Set (Pair A B)) :=
      for (acc := Set.empty) (a in s1) {
        Set.insert (pairsForElement a) acc
      };
  in setJoin pairSets;
```

### `powerset`

Generate the powerset (set of all subsets) of a set.

```juvix
powerset {A} {{Ord A}} (s : Set A) : Set (Set A) :=
  let
    elements := Set.toList s;
    subLists := powerlists elements;
  in Set.fromList (map Set.fromList subLists);
```

### `isProperSubset`

Checks if all elements of `set1` are in `set2`, and that the two sets are not the same.

```juvix
isProperSubset {A} {{Eq A}} {{Ord A}} (set1 set2 : Set A) : Bool :=
  isSubset set1 set2 && not (set1 == set2)
```

## `Map K V`

The type `Map K V` represents a collection of key-value pairs, sometimes called
a dictionary, where keys are of type `K` and values are of type `V`.

```juvix
import Stdlib.Data.Map as Map public;
open Map using {
    Map
  } public;
```

For example,

```juvix
codeToken : Map Nat String := Map.fromList [ (1 , "BTC") ; (2 , "ETH") ; (3, "ANM")];
```

### `updateLookupWithKey`

Updates a value at a specific key using the update function and returns both the
old value (if the key existed) and the updated map.

```juvix
updateLookupWithKey
  {Key Value}
  {{Ord Key}}
  (updateFn : Key -> Value -> Option Value)
  (k : Key)
  (map : Map Key Value)
  : Pair (Option Value) (Map Key Value) :=
  let
    oldValue : Option Value := Map.lookup k map;
    newMap : Map Key Value :=
      case oldValue of {
        | none := map
        | some v :=
          case updateFn k v of {
            | none := Map.delete k map
            | some newV := Map.insert k newV map
          }
      };
  in oldValue, newMap;
```

### `mapKeys`

Maps all keys in the Map to new keys using the provided function. If the mapping
function is not injective (maps different keys to the same key), later entries
in the map will overwrite earlier ones with the same new key.

```juvix
mapKeys
  {Key1 Key2 Value}
  {{Ord Key2}}
  (fun : Key1 -> Key2)
  (map : Map Key1 Value)
  : Map Key2 Value :=
  Map.fromList
    (for (acc := nil) ((k, v) in Map.toList map) {
      (fun k, v) :: acc
    });
```

### `restrictKeys`

Restrict a map to only contain keys from the given set.

```juvix
restrictKeys
  {Key Value}
  {{Ord Key}}
  (map : Map Key Value)
  (validKeys : Set.Set Key)
  : Map Key Value :=
  for (acc := Map.empty) (k, v in map) {
    if
      | Set.isMember k validKeys := Map.insert k v acc
      | else := acc
  };
```

### `withoutKeys`

Remove all entries from a map whose keys appear in the given set.

```juvix
withoutKeys
  {Key Value}
  {{Ord Key}}
  (map : Map Key Value)
  (invalidKeys : Set.Set Key)
  : Map Key Value :=
  for (acc := Map.empty) (k, v in map) {
    if
      | Set.isMember k invalidKeys := acc
      | else := Map.insert k v acc
  };
```

### `mapPartition`

Split a map according to a predicate on values.
Returns a pair of maps, (matching, non-matching).

```juvix
mapPartition
  {Key Value}
  {{Ord Key}}
  (predicate : Value -> Bool)
  (map : Map Key Value)
  : Pair (Map Key Value) (Map Key Value) :=
  for (matching, nonMatching := Map.empty, Map.empty) (k, v in map) {
    if
      | predicate v := Map.insert k v matching, nonMatching
      | else := matching, Map.insert k v nonMatching
  };
```

### `partitionWithKey`

Split a map according to a predicate that can examine both key and value.
Returns a pair of maps, (matching, non-matching).

      ```juvix
      partitionWithKey
        {Key Value}
        {{Ord Key}}
        (predicate : Key -> Value -> Bool)
        (map : Map Key Value)
        : Pair (Map Key Value) (Map Key Value) :=
        for (matching, nonMatching := Map.empty, Map.empty) (k, v in map) {
          if
            | predicate k v := Map.insert k v matching, nonMatching
            | else := matching, Map.insert k v nonMatching
        };
      ```

### `mapOption`

Apply a partial function to all values in the map, keeping only the entries where the function returns 'some'.

```juvix
mapOption
  {Key Value1 Value2} {{Ord Key}}
  (f : Value1 -> Option Value2)
  (map : Map Key Value1)
  : Map Key Value2 :=
  for (acc := Map.empty) (k, v in map) {
    case f v of {
      | none := acc
      | some v' := Map.insert k v' acc
    }
  };
```

### `mapOptionWithKey`

Same as mapOption but allows the function to examine the key as well.

```juvix
mapOptionWithKey
  {Key Value1 Value2} {{Ord Key}}
  (f : Key -> Value1 -> Option Value2)
  (map : Map Key Value1)
  : Map Key Value2 :=
  for (acc := Map.empty) (k, v in map) {
    case f k v of {
      | none := acc
      | some v' := Map.insert k v' acc
    }
  };
```

### `mapEither`

Apply a function that returns Either to all values in the map.

```juvix
mapEither
  {Key Value Error Result}
  {{Ord Key}}
  (f : Value -> Either Error Result)
  (map : Map Key Value)
  : Pair (Map Key Error) (Map Key Result) :=
  for (lefts, rights := Map.empty, Map.empty) (k, v in map) {
    case f v of {
      | error e := Map.insert k e lefts, rights
      | ok r := lefts, Map.insert k r rights
    }
  };
```

### `mapEitherWithKey`

Same as mapEither but allows the function to examine the key as well.

```juvix
mapEitherWithKey
  {Key Value Error Result}
  {{Ord Key}}
  (f : Key -> Value -> Either Error Result)
  (map : Map Key Value)
  : Pair (Map Key Error) (Map Key Result) :=
  for (lefts, rights := Map.empty, Map.empty) (k, v in map) {
    case f k v of {
      | error e := Map.insert k e lefts, rights
      | ok r := lefts, Map.insert k r rights
    }
  };
```

## Undefined values

The term `undef` is a placeholder for unspecified values.

### `undef`

```juvix
axiom undef {A} : A;
```

### `TODO`

```juvix
axiom TODO {A} : A;
```

## `AVLTree`

```juvix
import Stdlib.Data.Set.AVL as AVLTree public;
open AVLTree using {
    AVLTree;
} public;
```
