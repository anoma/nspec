---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
---

```juvix
module architecture-2.engines.basic-types;

import Stdlib.Trait open public;
```

## Common types defined in external libraries

The following are fundamental types provided by the Juvix standard library and others,
which form the building blocks for more complex types in the architecture.

- **Nat**: Represents natural numbers (non-negative integers). Used for
  counting and indexing. 

```juvix
import Stdlib.Data.Nat as Nat
  open using
  { Nat; 
    zero; 
    suc
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
import Stdlib.Data.Pair as Pair 
  open using {
    Pair;
    ,
  } public;
```

For example,

```juvix
pair : Pair Nat Bool := (10 Pair., true);
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
import Stdlib.Data.Maybe as Maybe
  open using {
    Maybe;
    just;
    nothing
  } public;
```

- **Map K V**: Represents a collection of key-value pairs, sometimes called
  dictionary, where keys are of type `K` and values are of type `V`.

```juvix
import Data.Map as Map
  open using {
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
import Data.Set as Set
  open using {
    Set
  } public;
```

For example,

```juvix
uniqueNumbers : Set Nat := Set.fromList [1 ; 2 ; 2 ; 2; 3];
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
ExternalID : Type := Nat;
```

- **InternalID**: A unique identifier for entities within the system, also
  represented as a natural number.

```juvix
InternalID : Type := Nat;
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
Name : Type := Either String ExternalID;
Address : Type := Name;
```

### Enveloped messages

These types are used for message passing within the system, encapsulating the
message content and managing mailboxes.

- **Message**: A record type consisting of a type and a string. This represents a
  message with its type and content.

```juvix
MessagePayload : Type := String;

type Message (MessageType : Type) : Type := mkMessage {
  messageType : MessageType;
  payload : String;
};
```

- **Message Packet**: A record consisting of a target address and a message.

```juvix
type MessagePacket (MessageType : Type) : Type := mkMessagePacket {
  target : Address;
  message : Message MessageType;
};
```

- **Enveloped Message**: A record consisting of a message packet and a sender
  address.

```juvix
type EnvelopedMessage (MessageType : Type) : Type :=
  mkEnvelopedMessage {
    sender : Address;
    packet : MessagePacket MessageType;
  };
```


For convenience, let's define some handy functions for enveloped messages:

```juvix
getMessageType : {M : Type} -> EnvelopedMessage M -> M
  | (mkEnvelopedMessage@{ packet := 
      (mkMessagePacket@{ message := 
        (mkMessage@{ messageType := mt })})}) := mt;
```

```juvix
getMessagePayload : {M : Type} -> EnvelopedMessage M -> MessagePayload
  | (mkEnvelopedMessage@{ packet := 
      (mkMessagePacket@{ message :=
        (mkMessage@{ payload := p })})}) := p;
```

```juvix
getMessageSender : {M : Type} -> EnvelopedMessage M -> Address
  | (mkEnvelopedMessage@{ sender := s }) := s;
```

```juvix
getMessageTarget : {M : Type} -> EnvelopedMessage M -> Address
  | (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ target := t }) }) := t;
```

- **Mailbox**: A list of messages. It represents a collection of messages
  waiting to be processed.

```juvix
type Mailbox (MessageType : Type) : Type := mkMailBox {
  mailboxState : {State : Type} -> Maybe State;
  messages : List (EnvelopedMessage MessageType);
};
```

Mailboxes are indexed by their unique identifier, for now represented as
a number. This concerns the mailbox cluster of a single engine

```juvix
MailboxID : Type := Nat;
```


### Time and Triggers

- **Time**: A natural number representing time. It is used for scheduling and
  timing events.

```juvix
Time : Type := Nat;
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

- **Trigger**: An abstract type representing the nature of an events in the system, such
as message arrivals, timer expirations.

```juvix
type Trigger (MessageType : Type) :=
  | MessageArrived
    {
      MID : Maybe MailboxID;
      envelope : EnvelopedMessage MessageType;
    }
  | Elapsed { timers : List Timer };
```

One can define a function to extract the message from a trigger:
 
```juvix
getMessagePayloadFromTrigger : {M : Type} -> Trigger M -> Maybe MessagePayload
  | (MessageArrived@{ 
      envelope := (mkEnvelopedMessage@{ 
        packet := (mkMessagePacket@{ 
          message := (mkMessage@{ payload := p }) })})}) 
          := just p
  | _ := nothing;
```

Update the mailbox cluser with the messaged received by the trigger:

```
updateMailboxCluster : {M : Type} -> Trigger M -> Map MailboxID (Mailbox M) -> Map MailboxID (Mailbox M)
  | (MessageArrived@{ MID := just mid ; envelope := m }) mcluster := 
      case Map.lookup mid mcluster of {
        | just mailbox := Map.insert mid (mcluster@mkMailBox{ messages := m :: mb.messages}) mcluster
        | _ := mcluster
      }
  | _ mc := mc;
```

