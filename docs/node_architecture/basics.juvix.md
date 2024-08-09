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
import prelude open using {Hash} public;
```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[Juvix Base Prelude](./../prelude.juvix.md).

### Network identity types

These types are used to represent identities within the network, both external
and internal.

!!! info

    There is an ongoing discussion about cryptographic identities and how they
    should be represented in the system, and used for representing entities in the
    network, such as engines. So, the following types are subject to change. The
    main reference in the specs is [[Identity]].

#### ExternalID

A unique identifier for entities outside the system, represented as a natural
number. In practice, it could be a public key.

```juvix
syntax alias ExternalID := Nat;
```

#### InternalID

A unique identifier for entities within the system, also represented as a
natural number. In practice, it could be a private key.

```juvix
syntax alias InternalID := Nat;
```

#### Identity

A pair combining an `ExternalID` and an `InternalID`, representing the complete
identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Types for messages and communication

#### Address

It is used for forwarding messages to the correct destination. An address could
be a simple string without any particular meaning in the system or an external
identity.

```juvix
Name : Type := Either String ExternalID;
syntax alias Address := Name;
```

### Messages

Messages send between engines in the system are represented by the following
types. When a message is sent, it is enveloped with additional information such
as the sender and the target address. These messages go through the network and
end up in a mailbox of the target engine. Mailboxes are indexed by their unique
identifier, for now represented as a number.

```juvix
syntax alias MailboxID := Nat;
```


#### MessagePacket

A message packet consists of a target address, a mailbox identifier, and
the message itself of a specific type given as a type parameter, `MessageType`.

```juvix
type MessagePacket (MessageType : Type) : Type := mkMessagePacket {
  --- the `target` is an engine instance
  target : Address;
  --- there may be a `mailbox` or otherwise the default mailbox is used
  mailbox : Maybe Nat;
  message : MessageType;
};
```

#### EnvelopedMessage

An enveloped message consists of a possibly a sender address in case the sender
wants to be identified, and a message packet.

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

getMessageSender : {M : Type} -> EnvelopedMessage M -> Maybe Address
  | (mkEnvelopedMessage@{ sender := s }) := s;

getMessageTarget : {M : Type} -> EnvelopedMessage M -> Address
  | (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ target := t }) }) := t;
```

#### Mailbox M S

A mailbox is a container for messages and a mailbox state. The mailbox state
could be used to store additional information about the mailbox.

```juvix
type Mailbox (MessageType MailboxStateType : Type) : Type := mkMailbox {
  messages : List (EnvelopedMessage MessageType);
  mailboxState : Maybe MailboxStateType;
};
```

### Trigger related types

#### Time

Times is represented as natural numbers. It is used for scheduling and timing events.

```juvix
syntax alias Time := Nat;
```

#### Timer H

A timer is a pair of a time and a handle. The handle is used to identify the
timer and can be used to cancel the timer or notify the engine when the timer
expires.

```juvix
type Timer (HandleType : Type): Type := mkTimer {
  time : Time;
  handle : HandleType;
};
```

### Trigger M H

An abstract type representing the nature of events in the system, such as
message arrivals, timer expirations.

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
