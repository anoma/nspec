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
    import Stdlib.Trait.Eq open using {==} public;
    import Stdlib.Debug.Fail open using {failwith};

    ```

# Common Types - Juvix Base Prelude

The following are frequent and basic abstractions used in the Anoma
specification. Most of them are defined in the Juvix standard library and are
used to define more complex types in the Anoma Specification.

## Combinators

Identity function

```juvix
id {A} (a : A) : A := a;
```

Constant function

```juvix
const {A B} (a : A) : B -> A :=
  \{_ := a};
```

Flip arguments to a function

```juvix
flip {A B C} (f : A -> B -> C) (b : B) (a : A) : C :=
  f a b;
```

Function application

```
apply {A B} (f : A -> B) : A -> B := f;
```

Function composition

```juvix
compose {A B C} (f : B -> C) (g : A -> B) (x : A) : C := 
  f (g x);
```

## Useful Type Classes

Two-argument functor

```juvix
trait
type Bifunctor (F : Type -> Type -> Type) :=
  mkBifunctor@{
    bimap : {A B C D : Type} -> (A -> C) -> (B -> D) -> F A B -> F C D
  };
```

Product with associators

```juvix
trait
type SemigroupalProduct (F : Type -> Type -> Type) :=
  mkSemigroupalProduct@{
    assocLeft : {A B C : Type} -> F A (F B C) -> F (F A B) C;
    assocRight : {A B C : Type} -> F (F A B) C -> F A (F B C)
  };
```

Product with commuters

```juvix
trait
type CommutativeProduct (F : Type -> Type -> Type) :=
  mkCommutativeProduct@{
    swap : {A B : Type} -> F A B -> F B A;
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
    ite; -- TODO: remove this, use if | ... | else ... instead
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

Exlusive or

```juvix
xor (a b : Bool) : Bool := 
  case a of {
    | true := not b
    | false := b
  };
```

Not and

```juvix
nand (a b : Bool) : Bool := not (and a b);
```

Not or

```juvix
nor (a b : Bool) : Bool := not (or a b);
```

Boolean if

```juvix
ifb {A : Type} (a : Bool) (t f : A) : A :=
  case a of {
    | true := t
    | false := f
  };
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
    min;
    max;
  } public;
```

For example,

```juvix
ten : Nat := 10;
```

Predecessor function for natural numbers.

```juvix
pred (n : Nat) : Nat :=
  case n of {
    | zero := zero
    | suc k := k
  };
```

Convert boolean to a Bool to a Nat in the standard way of circuits.

```juvix
boolToNat (b : Bool) : Nat :=
  case b of {
    | false := 1
    | true := 0
  };
```

Check if a natural number is zero.

```juvix
isZero (n : Nat) : Bool :=
  case n of {
    | zero := true
    | suc k := false
  };
```

Parity checking functions

```juvix
isEven (n : Nat) : Bool := mod n 2 == 0
```

```juvix
isOdd (n : Nat) : Bool := mod n 2 == 1
```

Fold over natural numbers.

```juvix
terminating
foldNat {B : Type} (z : B) (f : Nat -> B -> B) (n : Nat) : B :=
  case n of {
    | zero := z
    | suc k := f k (foldNat z f k)
  };
```

Itteration of a function.

```juvix
iter {A : Type} (f : A -> A) (n : Nat) (x : A) : A :=
  foldNat x \{_ y := f y} n;
```

Exponentiation

```juvix
exp (base : Nat) (exponent : Nat) : Nat :=
  foldNat 1 \{_ product := base * product} exponent;
```

Factorial

```juvix
factorial : Nat -> Nat :=
  foldNat 1 \{k r := suc k * r};
```

Greatest Common Divisor

```juvix
terminating
gcd (a b : Nat) : Nat :=
  case b of {
    | zero := a
    | suc _ := gcd b (mod a b)
  };
```

Least Common Multiple

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

The type `String` represents sequences of characters. Used for text and communication.

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

## ByteString

```juvix
ByteString : Type := String;
```

A basic type for representing binary data.

```juvix
emptyByteString : ByteString := "";
```

## Unit

The type `Unit` represents a type with a single value. Often used when a function does not return any meaningful value.

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

Unique function to the unit. Universal property of terminal object.

```juvix
unitU {A : Type} : A -> Unit := const unit;
```

## Pair A B

The type `Pair A B` represents a tuple containing two elements of types `A` and `B`.
Useful for grouping related values together.

```juvix
import Stdlib.Data.Pair as Pair;
open Pair using { Pair } public;
open Pair using { , };
```

```juvix
-- necessary for Isabelle-translation
import Stdlib.Data.Fixity open;
syntax operator mkPair none;
syntax alias mkPair := ,;
```

For example,

```juvix
pair : Pair Nat Bool := mkPair 42 true;
```

Projections

```juvix
fst {A B} : Pair A B -> A
  | (mkPair a _) := a;
```

```juvix
snd {A B} : Pair A B -> B
  | (mkPair _ b) := b;
```

Swap components

```juvix
instance
PairCommutativeProduct : CommutativeProduct Pair :=
  mkCommutativeProduct@{
    swap := \{p := mkPair (snd p) (fst p)}
  };
```

Pair associations

```juvix
instance
PairSemigroupalProduct : SemigroupalProduct Pair :=
  mkSemigroupalProduct@{
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

Map functions over pairs

```juvix
instance
PairBifunctor : Bifunctor Pair :=
  mkBifunctor@{
    bimap := \{f g p := mkPair (f (fst p)) (g (snd p))};
  };
```

Universal property of pairs

```juvix
fork {A B C : Type} (f : C -> A) (g : C -> B) (c : C) : Pair A B :=
  mkPair (f c) (g c);
```

Curry a function

```juvix
curry {A B C : Type} (f : Pair A B -> C) (x : A) (y : B) : C :=
  f (mkPair x y);
```

Uncurry a function

```juvix
uncurry {A B C : Type} (f : A -> B -> C) (p : Pair A B) : C :=
  f (fst p) (snd p);
```

## Result A B

The `Result A B` type represents either a success with a value of `ok x` with `x` of type `A` or an error
with value `error e` with `e` of type `B`.

```juvix
import Stdlib.Data.Result.Base as Result;
open Result using { Result; ok; error } public;
```

## Either A B

The type `Either A B`, or sum type of `A` and `B`, represents a value of type
`A` or `B`. It is equivalent to `Result A B`, however, the meaning of the values
is different. There is no such thing as an error or success value in the
`Either` type, instead the values are either `left A` or `right B`. either `left
A` or `right B`.

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

Check components of either.

```juvix
isLeft {A B : Type} (e : Either A B) : Bool := 
  case e of {
    | left _ := true
    | right _ := false
  };
```

```juvix
isRight {A B : Type} (e : Either A B) : Bool := 
  case e of {
    | left _ := false
    | right _ := true
  };
```

Get left element (with default)

```juvix
fromLeft {A B : Type} (d : A) (e : Either A B) : A :=
  case e of {
    | left x := x
    | right _ := d
  };
```

Get right element (with default)

```juvix
fromRight {A B : Type} (d : B) (e : Either A B) : B :=
  case e of {
    | left _ := d
    | right x := x
  };
```

Swap elements

```juvix
instance
EitherCommutativeProduct : CommutativeProduct Either :=
mkCommutativeProduct@{
  swap {A B} : Result A B -> Result B A
      | (left x) := right {B} {A} x
      | (right x) := left x
};
```

Map onto elements of either

```
instance
EitherBifunctor : Bifunctor Either :=
  mkBifunctor@{
    bimap := \{f g e :=
      case e of {
        | left a := left (f a)
        | right b := right (g b)
      }}
  };
```

Universal property of coproduct

```juvix
fuse {A B C : Type} (f : A -> C) (g : B -> C) (e : Either A B) : C :=
  case e of {
    | left x := f x
    | right x := g x
  };
```

Assiosiation functions for either

```
EitherSemigroupalProduct : SemigroupalProduct Either :=
  mkSemigroupalProduct@{
    assocLeft := \{e :=
      case e of {
        | left x := left (left x)
        | right ebc :=
          case ebc of {
            | left y := left (right y)
            | right z := right z
          }
      }};
    assocRight := \{e :=
      case e of {
        | left eab :=
          case eab of {
            | left x := left x
            | right y := right (left y)
          }
        | right z := right (right z)
      }};
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
  ++;
  reverse;
} public;
```

For example,

```juvix
numbers : List Nat := 1 :: 2 :: 3 :: nil;
-- alternative syntax:
niceNumbers : List Nat := [1 ; 2 ; 3];
```

Prepend element to a list

```juvix
snoc {A : Type} (xs : List A) (x : A) : List A :=
  xs ++ [x];
```

Check if all elements satisfy a predicate

```juvix
all : List Bool -> Bool :=
  foldl (\{acc x := and acc x}) true;
```

```juvix
allMap {A : Type} (p : A -> Bool) : List A -> Bool :=
  compose all (map p);
```

Check if any element satisfies a predicate

```juvix
any : List Bool -> Bool :=
  foldl (\{acc x := or acc x}) true;
```

```juvix
anyMap {A : Type} (p : A -> Bool) : List A -> Bool :=
  compose any (map p);
```

Zip two lists

```juvix
terminating
zip {A B : Type} (xs : List A) (ys : List B) : List (Pair A B) :=
  case xs of {
    | nil := nil
    | x :: xs' :=
      case ys of {
        | nil := nil
        | y :: ys' := (mkPair x y) :: (zip xs' ys')
      }
  };
```

Zip with a function

```juvix
zipWith {A B C : Type} (f : A -> B -> C) (xs : List A) (ys : List B) : List C :=
  map (uncurry f) (zip xs ys);
```

Unzip a list of pairs into two lists

```juvix
terminating
unzip {A B : Type} (xs : List (Pair A B)) : Pair (List A) (List B) :=
  case xs of {
    | nil := mkPair nil nil
    | p :: ps :=
      let unzipped := unzip ps
      in mkPair (fst p :: fst unzipped) (snd p :: snd unzipped)
  };
```

Partition a list

```juvix
partition {A B : Type} (es : List (Either A B)) : Pair (List A) (List B) :=
  foldr
    (\{e acc :=
      case e of {
        | left a := mkPair (a :: (fst acc)) (snd acc)
        | right b := mkPair (fst acc) (b :: (snd acc))
      }})
    (mkPair nil nil)
    es;
```

```juvix
partitionWith {A B C : Type} (f : C -> Either A B) (es : List C) : Pair (List A) (List B) :=
  partition (map f es)
```

## Option A

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

- Check if an optional value is `none`:

    ```juvix
    isNone {A} (x : Option A) : Bool
      := case x of {
      | none := true
      | some _ := false
      }
    ```

- Check if an optional value is `some`:

    ```juvix
    isSome {A} (x : Option A) : Bool := not (isNone x);
    ```

- Extract the value from an `Option` term:

    ```juvix
    fromOption {A} (x : Option A) (default : A) : A := case x of {
      | none := default
      | some x := x
    };
    ```


## Map K V

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

## Set A

The type `Set A` represents a collection of unique elements of type `A`. Used
for sets of values.

```juvix

import Stdlib.Data.Set as Set public;
open Set using {
    Set;
  } public;
```

For example,

```juvix
uniqueNumbers : Set Nat := Set.fromList [1 ; 2 ; 2 ; 2; 3];
```


### `disjointUnion`

```juvix
--- Computes the disjoint union of two ;Set;s.
disjointUnion {T} {{Ord T}} (s1 s2 : Set T) : Result (Set T) (Set T) :=
  case Set.intersection s1 s2 of
    | Set.empty := ok (Set.union s1 s2)
    | s := error s;
```


## Undefined values

The term `undef` is a placeholder for unspecified values.

### `undef`

```juvix
axiom undef : {A : Type} -> A;
```

### `TODO`

```juvix
axiom TODO : {A : Type} -> A;
```

### `UNUSED`

```juvix
--- A type describing the absence of a types.
--- NOTE: This can be used in instantiated interfaces for type parameters that are not used.
UNUSED : Type := Unit;
```

### `MISSING_DEFINITION`

```juvix
--- A type describing an unknown type that must be clarified.
--- NOTE: This can be used in instantiated interfaces for type parameters that are not unknown.
MISSING_DEFINITION : Type := Unit;
```

### `MISSING_SIZE`

```juvix
MISSING_SIZE : Nat := 0;
```

### `NOT_REQUIRED`

```juvix
--- A placeholder for an implementation that is not required for the private testnet.
NOT_REQUIRED : {A : Type} → A :=
  failwith "THIS IS NOT REQUIRED FOR THE PRIVATE TESTNET";
```

### `MISSING_JUVIX_IMPLEMENTATION`

```juvix
--- A placeholder for a missing Juvix implementation.
MISSING_JUVIX_IMPLEMENTATION : {A : Type} → A :=
  failwith "THIS MUST BE IMPLEMENT BY JUVIX";
```

### `MISSING_ANOMA_BUILTIN`

```juvix
--- A placeholder for a missing Anoma builtin.
MISSING_ANOMA_BUILTIN : {A : Type} → A :=
  failwith "THIS MUST BE PROVIDED AS AN ANOMA BUILTIN IN JUVIX";
```

### `ANOMA_BACKEND_IMPLEMENTATION`

```juvix
--- A placeholder for an implementation that must be implemented on by the Anoma instantiator in the backend, but is not supposed to be called from Juvix.
ANOMA_BACKEND_IMPLEMENTATION : {A : Type} → A :=
  failwith
    "THIS BACKEND IMPLEMENTATION IS NOT SUPPOSED TO BE CALLED FROM JUVIX";
```

For example,

```juvix
undefinedNat : Nat := undef;
```

## Functor

```juvix
import Stdlib.Trait.Functor.Polymorphic as Functor;
```

## Applicative

```juvix
import Stdlib.Data.Fixity open public;
import Stdlib.Trait.Applicative open using {Applicative; mkApplicative} public;
open Applicative public;
```

## Monad

```juvix
import Stdlib.Trait.Monad open using {Monad; mkMonad} public;
open Monad public;
```

## AVLTree

```juvix
import Stdlib.Data.Set.AVL as AVLTree public;
open AVLTree using {
    AVLTree;
} public;
```
