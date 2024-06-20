---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module architecture-2.engines.basic-types;

import Stdlib.Prelude as Prelude;
import Stdlib.Data.Product as Product;
import Data.Map as Containers;
```

## Common types defined in the standard library

These are fundamental types provided by the standard library, which form the
building blocks for more complex types in the architecture.

- **Nat**: Represents natural numbers (non-negative integers). Used for counting
  and indexing.

```juvix
Nat : Type := Prelude.Nat;
```

- **Bool**: Represents boolean values (`true` or `false`). Used for logical
  operations and conditions.

```juvix
Bool : Type := Prelude.Bool;
```

- **String**: Represents sequences of characters. Used for text manipulation and
  representation.

```juvix
String : Type := Prelude.String;
```

- **Unit**: Represents a type with a single value. Often used when a function
  does not return any meaningful value.

```juvix
Unit : Type := Prelude.Unit;
```

- **Pair (A B)**: A tuple containing two elements of types `A` and `B`. Useful
  for grouping related values together.
  
```juvix
Pair (A B : Type) : Type := A Product.× B;
```
- **List (A)**: A sequence of elements of type `A`. Used for collections and
  ordered data.

```juvix
List (A : Type) : Type := Prelude.List A;
```

- **Maybe (A)**: Represents an optional value of type `A`. It can be either
  `Just A` (containing a value) or `Nothing` (no value).

```juvix
Maybe (A : Type) : Type := Prelude.Maybe A;
```
```juvix
Map (K V : Type) : Type := Containers.Map K V;
```
- **Map (K V)**: Represents a collection of key-value pairs, where keys are of
  type `K` and values are of type `V`. Used for associative arrays or
  dictionaries.

## Common types defined in the architecture

### Network Identity types

These types are used to represent identities within the network, both external
and internal.

```juvix
ExternalID : Type := Nat;
```
- **ExternalID**: A unique identifier for entities outside the system,
  represented as a natural number.

```juvix
InternalID : Type := Nat;
```
- **InternalID**: A unique identifier for entities within the system, also
  represented as a natural number.

```juvix
axiom Time : Type;
```
- **Time**: An abstract type representing time. It is used for scheduling and
  timing events.

```juvix
Identity : Type := Pair ExternalID InternalID;
```
- **Identity**: A pair combining an `ExternalID` and an `InternalID`,
  representing the complete identity of an entity within the network.

### Enveloped messages

These types are used for message passing within the system, encapsulating the
message content and managing mailboxes.

- **Message**: A pair consisting of a type and a string. This represents a
  message with its type and content.
  
```juvix
Message : Type := Pair Type Prelude.String;
```

- **Mailbox**: A list of messages. It represents a collection of messages
  waiting to be processed.

```juvix
Mailbox : Type := List Message;
```

### Triggers

Triggers represent events that can occur in the system, such as timers.

- **Handler**: An abstract type representing a handler function or procedure. It
  is used to define what actions should be taken when a trigger occurs.

```juvix
axiom Handler : Type;
```

- **Timer**: A pair consisting of a `Time` and a `Handler`. It represents a
  scheduled event that will invoke the handler at the specified time.

```juvix
Timer : Type := Pair Time Handler;
```

- **Trigger**: An abstract type representing various events in the system, such
as message arrivals, timer expirations, or other significant occurrences.

```juvix
axiom Trigger : Type;
```

### System State

This type is used to represent the system's state and defines the domain for an
engine's state transition functions.

- **State**: An abstract type representing the state of an engine instance. It
  provides the context needed for state transition functions to update the
  engine's state based on events and triggers.

```juvix
axiom State : Type; 
```
