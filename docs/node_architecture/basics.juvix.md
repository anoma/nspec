---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
---

??? quote "Juvix imports"

    ```juvix
    module node_architecture.basics;
    import prelude open public;
    import prelude open using {Hash} public;
    import node_architecture.types.anoma_message as Anoma;
    import node_architecture.identity_types open;
    ```

# Juvix Prelude of the Anoma Node Architecture

This document describes the basic types and functions used in the node
architecture prelude. For a more general prelude, please refer to
[Juvix Base Prelude](./../prelude.juvix.md). (1)
{ .annotate }

1. :woman_raising_hand: If you are unfamiliar with Juvix,
please refer to the [Juvix documentation](https://docs.juvix.org/latest/tutorials/learn.html).

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
    [@special-delivery-mailbox-types-2023]
    (see also [[Mailbox Cluster]] and [@selectors-actors-2014]).

```juvix
syntax alias MailboxID := Nat;
```

### MessagePacket

A message packet consists of a target address, a mailbox identifier, and
the message itself.

```juvix
type MessagePacket : Type := mkMessagePacket {
  target : Address;
  mailbox : Maybe Nat;
  message : Anoma.Msg;
};
```

### EnvelopedMessage

An enveloped message consists of a possible sender address if the sender wishes
to be identified, along with a message packet.

```juvix
type EnvelopedMessage : Type :=
  mkEnvelopedMessage {
    sender : Maybe Address;
    packet : MessagePacket;
  };
```

For convenience, here are some handy functions for enveloped messages:

```juvix
getMessageType : EnvelopedMessage -> Anoma.Msg
  | (mkEnvelopedMessage@{ packet :=
      (mkMessagePacket@{ message := mt })}) := mt;
```

```juvix
getMessageSender : EnvelopedMessage -> Maybe Address
  | (mkEnvelopedMessage@{ sender := s }) := s;
```

```juvix
getMessageTarget : EnvelopedMessage -> Address
  | (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ target := t }) }) := t;
```

### Mailbox S

A mailbox is a container for messages and optionally a mailbox state. The
mailbox state could be used to store additional information about the mailbox,
such as the priority of the messages in the mailbox.

??? info "Where does mailbox state come from?"

    The mailbox state is related to the capabilities of mailboxes of the paper
    [@special-delivery-mailbox-types-2023]. In particular, at any given
    point in time, a mailbox will have a capability for receiving messages (in
    later versions of the specs). As mailbox state can be useful in general, we
    already have it now.


```juvix
type Mailbox (MailboxStateType : Type) : Type := mkMailbox {
  messages : List EnvelopedMessage;
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

### Trigger H

```juvix
type Trigger (HandleType : Type) :=
  | MessageArrived { envelope : EnvelopedMessage; }
  | Elapsed { timers : List (Timer HandleType) };
```

- Extract the actual message from a trigger in case it has one:

    ```juvix
    getMessageFromTrigger : {H : Type} -> Trigger H -> Maybe Anoma.Msg
      | (MessageArrived@{ envelope := (mkEnvelopedMessage@{ packet := (mkMessagePacket@{ message := m })})}) := just m
      | _ := nothing;
    ```

  - Get the message sender from a trigger:

      ```juvix
      getMessageSenderFromTrigger : {H : Type} -> Trigger H -> Maybe Name
        | (MessageArrived@{ envelope := e; }) := EnvelopedMessage.sender e
        | _ := nothing;
      ```

  - Get the target destination from a trigger:

      ```juvix
      getMessageTargetFromTrigger : {H : Type} -> Trigger H -> Maybe Name
        | (MessageArrived@{ envelope := mkEnvelopedMessage@{ packet := mkMessagePacket@{ target := t }}}) := just t
      | _ := nothing;
      ```

### TimestampedTrigger M H

```juvix
type TimestampedTrigger (HandleType : Type) :=
  mkTimestampedTrigger {
    time : Time;
    trigger : Trigger HandleType;
  };
```

- Get the actual message from a `TimestampedTrigger`:

    ```juvix
    getMessageFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Maybe Anoma.Msg
      := getMessageFromTrigger (TimestampedTrigger.trigger  tr);
    ```

- Get the sender from a `TimestampedTrigger`:

    ```juvix
    getMessageSenderFromTimestampedTrigger {H}
      (tr : TimestampedTrigger H) : Maybe Name
      := getMessageSenderFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the target from

    ```juvix
    getMessageTargetFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Maybe Name
       := getMessageTargetFromTrigger (TimestampedTrigger.trigger tr);
    ```
