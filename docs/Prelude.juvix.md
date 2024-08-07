---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Juvix-Types
- Juvix-Prelude
---


```juvix
module juvix_commons;

import Stdlib.Trait open public;
```

# Common Types - Juvix Base Prelude

The following are fundamental types provided by the Juvix standard library and others, used to define more complex types in Anoma Specification.

## Nat

The type `Nat` represents natural numbers (non-negative integers). Used for counting and indexing.

```juvix
import Stdlib.Data.Nat as Nat
  open using
  { Nat;
    zero;
    suc;
    natToString
  } public;
```

For example,

```juvix
ten : Nat := 10;
```

Natural numbers are used (for now) to represent hash values, bytes sizes, and other non-negative integers.

```juvix
syntax alias Hash := Nat;
```

## Bool

The type `Bool` represents boolean values (`true` or `false`). Used for logical operations and conditions.

```juvix
import Stdlib.Data.Bool as Bool
  open using
  { Bool;
    true;
    false
  } public;
```

For example,

```juvix
verdad : Bool := true;
```

## String

The type `String` represents sequences of characters. Used for text and communication.

```juvix
import Stdlib.Data.String
  as String
  open using
  { String
  } public;
```

For example,

```juvix
hello : String := "Hello, World!";
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

## Either A B

The type `Either A B` represents a value of type `A` or `B`.

```juvix
type Either (A  B : Type) : Type :=
  | Left A
  | Right B;
```

For example,

```juvix
error : Either String Nat := Left "Error!";
answer : Either String Nat := Right 42;
```

## List A

The type `List A` represents a _sequence_ of elements of type `A`. Used for collections and ordered data.

```juvix
import Stdlib.Data.List as List
  open using {
  List;
  nil;
  ::
} public;
```

For example,

```juvix
numbers : List Nat := 1 :: 2 :: 3 :: nil;
-- alternative syntax:
niceNumbers : List Nat := [1 ; 2 ; 3];
```

## Maybe A

The type `Maybe A` represents an optional value of type `A`. It can be either `Just A` (containing a value) or `Nothing` (no value).

```juvix
import Stdlib.Data.Maybe as Maybe public;
open Maybe using {
    Maybe;
    just;
    nothing
  } public;
```

## Map K V

The type `Map K V` represents a collection of key-value pairs, sometimes called dictionary, where keys are of type `K` and values are of type `V`.

```juvix
import Data.Map as Map public;
open Map using {
    Map
  } public;
```

For example,

```juvix
codeToken : Map Nat String := Map.fromList [ (1 , "BTC") ; (2 , "ETH") ; (3, "ANM")];
```

## Set A

The type `Set A` represents a collection of unique elements of type `A`. Used for sets of values.

```juvix
import Data.Set as Set public;
open Set using {
    Set
  } public;
```

For example,

```juvix
uniqueNumbers : Set Nat := Set.fromList [1 ; 2 ; 2 ; 2; 3];
```

## Undefined values

The term `undef` is a placeholder for unspecified values.

```juvix
axiom undef : {A : Type} -> A;
```

For example,

```juvix
undefinedNat : Nat := undef;
```
