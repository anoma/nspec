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
import Data.Map as Containers open;
import Data.Set as Containers open;
```

## Common types defined in external libraries

The following are fundamental types provided by the Juvix standard library and others,
which form the building blocks for more complex types in the architecture.

- **Natural**: Represents natural numbers (non-negative integers). Used for
  counting and indexing.

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

or 

```juvix
Label : Type := Prelude.String;
```

and more specific for [[Engines in Anoma]]:

```juvix
EngineLabel : Type := Prelude.String
```

- **Unit**: Represents a type with a single value. Often used when a function
  does not return any meaningful value.

```juvix
Unit : Type := Prelude.Unit;
```

- **Pair A B**: A tuple containing two elements of types `A` and `B`. Useful
  for grouping related values together.
  
```juvix
Pair (A B : Type) : Type := Prelude.Pair A B;
```

- **Either A B**: Represents a value of type `A` or `B`.

```juvix
type Either (A  B : Type) : Type := 
  | Left A
  | Right B;
```

- **List A**: A sequence of elements of type `A`. Used for collections and
  ordered data.

```juvix
List (A : Type) : Type := Prelude.List A;
```

- **Maybe A**: Represents an optional value of type `A`. It can be either
  `Just A` (containing a value) or `Nothing` (no value).

```juvix
Maybe (A : Type) : Type := Prelude.Maybe A;
```

- **Map K V**: Represents a collection of key-value pairs, sometimes called
  dictionary, where keys are of type `K` and values are of type `V`. 

```juvix
Map (K V : Type) : Type := Containers.Map K V;
```

- **Set A**: Represents a collection of unique elements of type `A`. Used for
  sets of values.

```juvix
Set (A : Type) : Type := Containers.Set A;
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

### Network addresses

- **Address**: It is used for forwarding messages to the correct destination.
  An address could be a simple string without any particular meaning in the system or an external identity.

```juvix
Address : Type := Either Name ExternalID;
```

### Enveloped messages

These types are used for message passing within the system, encapsulating the
message content and managing mailboxes.

- **Message**: A pair consisting of a type and a string This represents a
  message with its type and content.

```juvix
MessageContent : Type := String;

Message (MessageType : Type) : Type := Pair MessageType MessageContent;
```

- **Message Packet**: A pair consisting of a target address and a message. It
  represents a message that is ready to be sent to a specific destination.

```juvix
Target : Type := Address;
MessagePacket (MessageType : Type) : Type := Pair Target (Message MessageType);
```

- **Enveloped Message**: A pair consisting of a message packet and a sender
  address.

```juvix
Sender : Type := Address;

EnvelopedMessage (MessageType : Type) : Type := 
  Pair Sender (MessagePacket MessageType);
```

- **Mailbox**: A list of messages. It represents a collection of messages
  waiting to be processed.

```juvix
Mailbox (MessageType : Type) : Type := List (EnvelopedMessage MessageType);
```

Mailboxes are indexed by their unique identifier, for
now represented as a `Name`. This concerns the mailbox of a single engine.

```juvix
MailboxID : Type := Name;
```

### Time and Triggers

- **Time**: A natural number representing time. It is used for scheduling and
  timing events.

```juvix
Time : Type := Natural;
```

Triggers represent events that can occur in the system, such as timers.

- **Handle**: An abstract type representing a handle function or procedure. It
  is used to define what actions should be taken when a trigger occurs.

```juvix
axiom Handle : Type;
```

- **Timer**: A pair consisting of a `Time` and a `Handle`. It represents a
  scheduled event that will invoke the handler at the specified time.

```juvix
Timer : Type := Pair Time Handle;
```

- **Trigger**: An abstract type representing various events in the system, such
as message arrivals, timer expirations, or other significant occurrences. The
following definition is most inspired by the datatype of the same name [trigger in Formanoma](https://github.com/anoma/formanoma/blob/84456645fad5f75c7b382831012d5d7f0d1f1dac/Types/Engine.thy#L8-L17

).


```juvix
type Trigger := 
  | MessageArrived
    { message : {MessageType : Type} -> EnvelopedMessage MessageType;
      boxID : MailboxID 
       } 
  | Elapsed {  timers : List Timer };
```

!!! todo

    Add a better description on the fields of this type.

### Node State

This type is used to represent the node's state and defines the domain for an
engine's state transition functions.

- **State**: An abstract type representing the state of an engine instance. It
  provides the context needed for state transition functions to update the
  engine's state based on events and triggers.

```juvix
axiom State : Type; 
```

