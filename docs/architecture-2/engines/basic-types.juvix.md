---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

!!! todo

    This module should be probably move to architecture-2.basic-types folder (?)
    Also, we might need to split it in two: Prelude and BaseTypes modules.


```juvix
module architecture-2.engines.basic-types;

import Stdlib.Prelude as Prelude;
import Stdlib.Data.Product as Product;
import Data.Map as Containers open;
```

## Common types defined in external libraries

The following are fundamental types provided by the Juvix standard library and others,
which form the building blocks for more complex types in the architecture.

- **Nat**: Represents natural numbers (non-negative integers). Used for counting
  and indexing.

```juvix
Natural : Type := Prelude.Nat;
```

- **Bool**: Represents boolean values (`true` or `false`). Used for logical
  operations and conditions.

```juvix
Bool : Type := Prelude.Bool;
```

- **String**: Represents sequences of characters. Used sending actual messages
  and data.

```juvix
String : Type := Prelude.String;
```

As a synonym for `String`, we have:

```juvix
Name : Type := Prelude.String;
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

- **Map (K V)**: Represents a collection of key-value pairs, sometimes called
  dictionary, where keys are of type `K` and values are of type `V`. 

```juvix
Map (K V : Type) : Type := Containers.Map K V;
```

## Proper terms and types for the Anoma Specification

- **Undefined** is a placeholder for an undefined value. It is used to indicate
  that a value is not yet defined or not applicable.

```juvix
axiom !undefined : {A : Type} -> A;
```


### Network Identity types

These types are used to represent identities within the network, both external
and internal. 

!!! warning

    There is an ongoing discussion about cryptographic identities and how they
    should be represented in the system, and used for representing entities in
    the network, such as engines. So, the following types are subject to change.
    The main reference in the specs is precisely the section on [[Identity]].


- **ExternalID**: A unique identifier for entities outside the system,
  represented as a natural number.

```juvix
ExternalID : Type := Natural;
```


- **InternalID**: A unique identifier for entities within the system, also
  represented as a natural number.

```juvix
InternalID : Type := Natural;
```

- **Identity**: A pair combining an `ExternalID` and an `InternalID`,
  representing the complete identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Enveloped messages

These types are used for message passing within the system, encapsulating the
message content and managing mailboxes.

- **Message**: A pair consisting of a type and a string This represents a
  message with its type and content[@special-delivery-mailbox-types-2023].

```juvix
MessageContent : Type := String;

Message (MessageType : Type) : Type := Pair MessageType MessageContent;
```

- **Mailbox**: A list of messages. It represents a collection of messages
  waiting to be processed.

```juvix
Mailbox (MessageType : Type) : Type := List (Message MessageType);
```

Mailboxes are indexed by their unique identifier, for
now represented as a `Name`. This concerns the mailbox of a single engine.

```juvix
MailboxID : Type := Name;
```

### Time and Triggers

- **Time**: An abstract type representing time. It is used for scheduling and
  timing events.

```juvix
axiom Time : Type;
```

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
as message arrivals, timer expirations, or other significant occurrences. The
following definition is most inspired by the datatype of the same name [trigger in Formanoma](https://github.com/anoma/formanoma/blob/84456645fad5f75c7b382831012d5d7f0d1f1dac/Types/Engine.thy#L8-L17

).
!!! todo

    The `Trigger` type should be defined in more detail, as briefly explained in
    https://anoma.github.io/nspec/pr-84/tutorial/engines/index.html#inputs-of-a-transition-function 


```juvix
type Trigger (MessageType : Type)  := 
  | MessageArrived
    { message : Message MessageType;
      boxID : MailboxID ;
      extID : ExternalID } 
  | Elapsed {  timers : List Timer };
```

### Node State

This type is used to represent the node's state and defines the domain for an
engine's state transition functions.

- **State**: An abstract type representing the state of an engine instance. It
  provides the context needed for state transition functions to update the
  engine's state based on events and triggers.

```juvix
axiom State : Type; 
```
