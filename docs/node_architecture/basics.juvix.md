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
module node_architecture.basics;
import prelude open public;
import prelude open using {Hash} public; -- TODO: review this, in principle, it should be imported with the previous import
```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node architecture prelude.
For a more general prelude, please refer to [Juvix Base Prelude](./../prelude.juvix.md).


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

In principle, messages can have any type,
and thus we have a simple type parameter,
which we call `MessageType`.

- **Message Packet**: A record consisting of a target address, and mailbox ID, and a message.

```juvix
type MessagePacket (MessageType : Type) : Type := mkMessagePacket {
  --- the `target` is an engine instance     
  target : Address;
  --- there may be a `mailbox` or otherwise the default mailbox is used
  mailbox : Maybe Nat;
  message : MessageType;
};
```

- **Enveloped Message**: A record consisting of a message packet and a sender
  address.

```juvix
type EnvelopedMessage (MessageType : Type) : Type :=
  mkEnvelopedMessage {
    sender : Maybe Address;
    packet : MessagePacket MessageType;
  };
```

For convenience, let's define some handy functions for enveloped messages:

```juvix
getMessageType : {M : Type} -> EnvelopedMessage M -> M
  | (mkEnvelopedMessage@{ packet :=
      (mkMessagePacket@{ message := mt })}) := mt;
```

```juvix
getMessageSender : {M : Type} -> EnvelopedMessage M -> Maybe Address
  | (mkEnvelopedMessage@{ sender := s }) := s;
```

```juvix
getMessageTarget : {M : Type} -> EnvelopedMessage M -> Address
  | (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ target := t }) }) := t;
```

- **Mailbox**: A list of messages. It represents a collection of messages
  waiting to be processed.

```juvix
type Mailbox (MessageType MailboxStateType : Type) : Type := mkMailbox {
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
  | MessageArrived { envelope : EnvelopedMessage MessageType; }
  | Elapsed { timers : List (Timer HandleType) };
```

One can define a function to extract the message from a trigger:

```juvix
getMessagePayloadFromTrigger : {M H : Type} -> Trigger M H -> Maybe M
  | (MessageArrived@{
      envelope := (mkEnvelopedMessage@{
        packet := (mkMessagePacket@{
          message := m })})})
          := just m
  | _ := nothing;
```
