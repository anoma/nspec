---
icon: material/file-document-outline
search:
  exclude: false
  boost: 
tags:
- Juvix-Types
- Juvix-Prelude
---

```juvix
module Prelude;

import Stdlib.Trait open public;
```

## Anoma Specification - Juvix Base Prelude

The following are fundamental types provided by the Juvix standard library and others,
used to define more complex types in Anoma Specification.

- **Nat**: Represents natural numbers (non-negative integers). Used for
  counting and indexing.

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

- **Bool**: Represents boolean values (`true` or `false`). Used for logical
  operations and conditions.

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

- **String**: Represents sequences of characters. Used for text and
  communication.

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

- **Unit**: Represents a type with a single value. Often used when a function
  does not return any meaningful value.

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

- **Pair A B**: A tuple containing two elements of types `A` and `B`. Useful
  for grouping related values together.

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

- **Either A B**: Represents a value of type `A` or `B`.

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


- **List A**: A sequence of elements of type `A`. Used for collections and
  ordered data.

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

- **Maybe A**: Represents an optional value of type `A`. It can be either
  `Just A` (containing a value) or `Nothing` (no value).

```juvix
import Stdlib.Data.Maybe as Maybe public;
open Maybe using {
    Maybe;
    just;
    nothing
  } public;
```

- **Map K V**: Represents a collection of key-value pairs, sometimes called
  dictionary, where keys are of type `K` and values are of type `V`.

```juvix
import Data.Map as Map public;
open Map using {
    Map
  } public;
```

For example,

```juvix
codeToken : Map Nat String :=
  Map.fromList [ (1 , "BTC") ; (2 , "ETH") ; (3, "ANM")];
```

- **Set A**: Represents a collection of unique elements of type `A`. Used for
  sets of values.

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

- **Undefined** is a placeholder for an undefined value. It is used to indicate
  that a value is not yet defined or not applicable.

```juvix
axiom undef : {A : Type} -> A;
```