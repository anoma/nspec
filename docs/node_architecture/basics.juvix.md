---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

??? info "Juvix imports"

    ```juvix
    module node_architecture.basics;
    import prelude open public;
    import prelude open using {Hash} public;
    ```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[Juvix Base Prelude](./../prelude.juvix.md). (1)
{ .annotate }

1. :woman_raising_hand: If you are unfamiliar with Juvix,
please refer to the [Juvix documentation](https://docs.juvix.org/latest/tutorials/learn.html).

## Types for network identities

<!-- This section needs to be reworked. --><!--ᚦ: in which ways?-->

Types in this section are used to represent [[Identity|identities]] within the network.

### ExternalID

A unique identifier, such as a public key, represented as a natural number.

```juvix
syntax alias ExternalID := Nat;
```

### InternalID

A unique identifier, such as a private key, used internally within the network,
represented as a natural number.

```juvix
syntax alias InternalID := Nat;
```

### Identity

A pair combining an `ExternalID` and an `InternalID`, representing the complete
identity of an entity within the network.

```juvix
Identity : Type := Pair ExternalID InternalID;
```

### Name

A name could be a simple string without any particular meaning in the system or
an external identity.

```juvix p
Name : Type := Either String ExternalID;
```

### Address

An address is a name used for forwarding messages to the correct destination.

```juvix
syntax alias Address := Name;
```

## Types for messages and communication

A message is a piece of data dispatched from one engine, termed the _sender_, to
another engine, referred to as the _target_. When a message is sent, it is
enveloped with additional metadata such as the _target address_ and potentially
the _sender address_, in case the sender wants to be identified. Upon arrival at
the target engine, the message is stored in the target engine's mailboxes. These
mailboxes are indexed by an identifier that are only unique to their engine. If
the target engine has only one mailbox, the mailbox identifier is redundant.

The following types are used to represent these messages and mailboxes.

### MailboxID

A mailbox identifier is a natural number used to index mailboxes.

??? info "Where do mailbox identifiers come from?"

    The concept of mailbox identifier is taken from
    the paper
    [@fowler2023specialdeliveryprogrammingmailbox]
    (see also [[Mailbox Cluster]] and [@SelectorsACM]).

```juvix
syntax alias MailboxID := Nat;
```

### MessagePacket M

A message packet consists of a target address, a mailbox identifier, and
the message itself of a specific type given as a type parameter, `MessageType`.

```juvix
type MessagePacket (MessageType : Type) : Type := mkMessagePacket {
  target : Address;
  mailbox : Maybe Nat;
  message : MessageType;
};
```

### EnvelopedMessage M

An enveloped message consists of a possible sender address if the sender wishes
to be identified, along with a message packet.

```juvix
type EnvelopedMessage (MessageType : Type) : Type :=
  mkEnvelopedMessage {
    sender : Maybe Address;
    packet : MessagePacket MessageType;
  };
```

For convenience, here are some handy functions for enveloped messages:

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

### Mailbox M S

A mailbox is a container for messages and optionally a mailbox state. The
mailbox state could be used to store additional information about the mailbox,
such as the priority of the messages in the mailbox.

??? info "Where does mailbox state come from?"

    The mailbox state is related to the capabilities of mailboxes of the paper
    [@fowler2023specialdeliveryprogrammingmailbox]. In particular, at any given
    point in time, a mailbox will have a capability for receiving messages (in
    later versions of the specs). As mailbox state can be useful in general, we
    already have it now.


```juvix
type Mailbox (MessageType MailboxStateType : Type) : Type := mkMailbox {
  messages : List (EnvelopedMessage MessageType);
  mailboxState : Maybe MailboxStateType;
};
```

### Time

```juvix
syntax alias Time := Nat;
```

### Timer H

```juvix
type Timer (HandleType : Type): Type := mkTimer {
  time : Time;
  handle : HandleType;
};
```

### Trigger M H

```juvix
type Trigger (MessageType : Type) (HandleType : Type) :=
  | MessageArrived { envelope : EnvelopedMessage MessageType; }
  | Elapsed { timers : List (Timer HandleType) };
```

- Extract the actual message from a trigger in case it has one:

    ```juvix
    getMessageFromTrigger : {M H : Type} -> Trigger M H -> Maybe M
      | (MessageArrived@{ envelope := (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ message := m })})}) := just m
      | _ := nothing;
    ```

  - Get the message sender from a trigger:

      ```juvix
      getMessageSenderFromTrigger : {M H : Type} -> Trigger M H -> Maybe Name
        | (MessageArrived@{ envelope := e; }) := EnvelopedMessage.sender e
        | _ := nothing;
      ```

  - Get the target destination from a trigger:

      ```juvix
      getMessageTargetFromTrigger : {M H : Type} -> Trigger M H -> Maybe Name
        | (MessageArrived@{ envelope := mkEnvelopedMessage@{ packet := mkMessagePacket@{ target := t }}}) := just t
      | _ := nothing;
      ```

### TimestampedTrigger M H

```juvix
type TimestampedTrigger (MessageType : Type) (HandleType : Type) :=
  mkTimestampedTrigger {
    time : Time;
    trigger : Trigger MessageType HandleType;
  };
```

- Get the actual message from a `TimestampedTrigger`:

    ```juvix
    getMessageFromTimestampedTrigger {M H} (tr : TimestampedTrigger M H) : Maybe M
      := getMessageFromTrigger (TimestampedTrigger.trigger  tr);
    ```

- Get the sender from a `TimestampedTrigger`:

    ```juvix
    getMessageSenderFromTimestampedTrigger {M H} 
      (tr : TimestampedTrigger M H) : Maybe Name 
      := getMessageSenderFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the target from 

    ```juvix
    getMessageTargetFromTimestampedTrigger {M H} (tr : TimestampedTrigger M H) : Maybe Name
       := getMessageTargetFromTrigger (TimestampedTrigger.trigger tr);
    ```
