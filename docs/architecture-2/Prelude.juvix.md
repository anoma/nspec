---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

```juvix
module architecture-2.Prelude;
import Prelude open public;
```

# Architecture Node - Juvix Prelude

This document describes the basic types and functions used in the node architecture prelude.
For a more general prelude, please refer to [Juvix Base Prelude](./../Prelude.juvix.md).


### Network Identity types

These types are used to represent identities within the network, both external
and internal.

!!! warning

    There is an ongoing discussion about cryptographic identities and how they
    should be represented in the system, and used for representing entities in
    the network, such as engines. So, the following types are subject to change.
    The main reference in the specs is precisely the section on [[Identity]].


- **ExternalID**: A unique identifier for entities outside the system,
  represented as a natural number. In practice, it could be a public key.

```juvix
syntax alias ExternalID := Nat;
```

- **InternalID**: A unique identifier for entities within the system, also
  represented as a natural number. In practice, it could be a private key.

```juvix
syntax alias InternalID := Nat;
```

- **Identity**: A pair combining an `ExternalID` and an `InternalID`,
  representing the complete identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Addresses

- **Address**: It is used for forwarding messages to the correct destination. An
  address could be a simple string without any particular meaning in the system
  or an external identity.

```juvix
Name : Type := Either String ExternalID;
syntax alias Address := Name;
```

### Messages

These types are used for message passing within the system, encapsulating the
message content and managing mailboxes.

- **Message**: A record type consisting of a type and a string. This represents a
  message with its type and content.

```juvix
syntax alias MessagePayload := String;

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
type Mailbox (MessageType MailboxStateType : Type) : Type := mkMailBox {
  messages : List (EnvelopedMessage MessageType);
  mailboxState : Maybe MailboxStateType;
};
```

Mailboxes are indexed by their unique identifier, for now represented as
a number. This concerns the mailbox cluster of a single engine

```juvix
syntax alias MailboxID := Nat;
```

### Timers

- **Time**: A natural number representing time. It is used for scheduling and
  timing events.

```juvix
syntax alias Time := Nat;
```
- **Timer**: A record consisting of a time and a handle. It is used for scheduling
  events to occur at a specific time.

```juvix
type Timer (HandleType : Type): Type := mkTimer {
  time : Time;
  handle : HandleType;
};
```

### Triggers

- **Trigger**: An abstract type representing the nature of an events in the system, such
as message arrivals, timer expirations.

```juvix
type Trigger (MessageType : Type) (HandleType : Type) :=
  | MessageArrived
    {
      MID : Maybe MailboxID;
      envelope : EnvelopedMessage MessageType;
    }
  | Elapsed { timers : List (Timer HandleType) };
```

One can define a function to extract the message from a trigger:

```juvix
getMessagePayloadFromTrigger : {M H : Type} -> Trigger M H -> Maybe MessagePayload
  | (MessageArrived@{
      envelope := (mkEnvelopedMessage@{
        packet := (mkMessagePacket@{
          message := (mkMessage@{ payload := p }) })})})
          := just p
  | _ := nothing;
```