---
icon: material/file-document-outline
search:
  exclude: false
tags:
- Juvix-Types
- Juvix-Prelude
---

??? note "Juvix imports"

    ```juvix
    module prelude;
    import Stdlib.Trait open public;
    import Stdlib.Trait.Ord open using {Ordering; mkOrd; Equal; isEqual} public;
    import Stdlib.Trait.Eq open using {==} public;
    ```

# Common Types - Juvix Base Prelude

The following are frequent and basic abstractions used in the Anoma
specification. Most of them are defined in the Juvix standard library and are
used to define more complex types in the Anoma Specification.

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
    *;
    <=;
  } public;
```

For example,

```juvix
ten : Nat := 10;
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
    and
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
} public;
```

For example,

```juvix
numbers : List Nat := 1 :: 2 :: 3 :: nil;
-- alternative syntax:
niceNumbers : List Nat := [1 ; 2 ; 3];
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


## Undefined values

The term `undef` is a placeholder for unspecified values.

```juvix
axiom undef : {A : Type} -> A;
axiom TODO : {A : Type} -> A;
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
