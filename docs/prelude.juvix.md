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
    ```

# Common Types - Juvix Base Prelude

The following are frequent and basic abstractions used in the Anoma
specification. Most of them are defined in the Juvix standard library and are
used to define more complex types in the Anoma Specification.

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

## Bool

The type `Bool` represents boolean values (`true` or `false`). Used for logical operations and conditions.

```juvix
import Stdlib.Data.Bool as Bool
  open using
  { Bool;
    true;
    false;
    ite;
    &&;
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

## Result A B

The `Result` type represents either a success with a value of `ok` or an error
with value `error`.

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
-- alias for Result
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
  ::
} public;
```

For example,

```juvix
numbers : List Nat := 1 :: 2 :: 3 :: nil;
-- alternative syntax:
niceNumbers : List Nat := [1 ; 2 ; 3];
```

## Optional A

The type `Optional A` represents an optional value of type `A`. It can be either
`Some A` (containing a value) or `None` (no value).

```juvix
import Stdlib.Data.Maybe as Maybe;
open Maybe using {
    Maybe;
    just;
    nothing
  };
```

```juvix
syntax alias Optional := Maybe;
syntax alias some := just;
syntax alias none := nothing;
```

- Check if an optional value is `none`:

    ```juvix
    isNone {A} (x : Optional A) : Bool
      := case x of {
      | none := true
      | some _ := false
      }
    ```

- Check if an optional value is `some`:

    ```juvix
    isSome {A} (x : Optional A) : Bool := not (isNone x);
    ```

- Extract the value from an `Optional` term:

    ```juvix
    fromOptional {A} (x : Optional A) (default : A) : A := case x of {
      | none := default
      | some x := x
    };
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

-- TODO: perhaps remove the following sections once the stdlib is updated
## Functor

```juvix
import Stdlib.Trait.Functor.Polymorphic as Functor;
```

## Applicative

```juvix
import Stdlib.Data.Fixity open public;
trait
type Applicative (f : Type -> Type) :=
  mkApplicative {
    {{ApplicativeFunctor}} : Functor f;
    pure : {A : Type} -> A -> f A;
    ap : {A B : Type} -> f (A -> B) -> f A -> f B
  };
```

For example, the `Optional` type is an instance of `Applicative`.

```juvix
instance
maybeApplicative : Applicative Optional :=
  mkApplicative@{
    pure := some;
    ap {A B} : Optional (A -> B) -> Optional A -> Optional B
      | (some f) (some x) := some (f x)
      | _ _ := none
  };
```

## Monad

```juvix
trait
type Monad (f : Type -> Type) :=
  mkMonad {
    {{MonadApplicative}} : Applicative f;

    builtin monad-bind
    bind : {A B : Type} -> f A -> (A -> f B) -> f B
  };
```

```juvix
syntax operator >>= seq;
>>= {A B} {f : Type -> Type} {{Monad f}} (x : f A) (g : A -> f B) : f B := Monad.bind x g;
```

```juvix
monadMap {A B} {f : Type -> Type} {{Monad f}} (g : A -> B) (x : f A) : f B := map g x;
```

For example, the `Optional` type is an instance of `Monad`.

```juvix
instance
maybeMonad : Monad Optional :=
  mkMonad@{
    bind {A B} : Optional A -> (A -> Optional B) -> Optional B
      | none _ := none
      | (some a) f := f a
  };
```

```juvix
open Applicative public;
open Monad public;
```
