---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
- Juvix-types
- Types
- Message
- Mailbox
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.types.messages;
    import prelude open public;
    import arch.node.types.basics open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message open;
    ```

# Messages and mailboxes

## Types

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

### EngineMessage

A message between engines. Consists of a sender, a target, an optional mailbox
identifier, and the message itself.

```juvix
type EngineMessage : Type := mkEngineMessage {
  sender : EngineID;
  target : EngineID;
  mailbox : Option MailboxID;
  msg : Msg;
};
```

### MessageID

Message identifier. Cryptographic hash of an `EngineMessage`.

```juvix
syntax alias MessageID := Hash;
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
  messages : List EngineMessage;
  mailboxState : Option MailboxStateType;
};
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
  | MessageArrived { msg : EngineMessage; }
  | Elapsed { timers : List (Timer HandleType) };
```

- Extract the actual message from a trigger in case it has one:

    ```juvix
    getMessageFromTrigger : {H : Type} -> Trigger H -> Option Msg
      | MessageArrived@{msg} := some (EngineMessage.msg msg)
      | Elapsed@{} := none;
    ```

- Get the message sender from a trigger:

    ```juvix
    getSenderFromTrigger : {H : Type} -> Trigger H -> Option EngineID
      | MessageArrived@{msg} := some (EngineMessage.sender msg)
      | Elapsed@{} := none;
    ```

- Get the target destination from a trigger:

    ```juvix
    getTargetFromTrigger : {H : Type} -> Trigger H -> Option EngineID
      | MessageArrived@{msg} := some (EngineMessage.target msg)
      | Elapsed@{} := none;
    ```

### TimestampedTrigger H

```juvix
type TimestampedTrigger (HandleType : Type) :=
  mkTimestampedTrigger {
    time : Time;
    trigger : Trigger HandleType;
  };
```

- Get the actual message from a `TimestampedTrigger`:

    ```juvix
    getMessageFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option Msg
      := getMessageFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the sender from a `TimestampedTrigger`:

    ```juvix
    getSenderFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option EngineID
      := getSenderFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the target from a `TImestampedTrigger`:

    ```juvix
    getTargetFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option EngineID
      := getTargetFromTrigger (TimestampedTrigger.trigger tr);
    ```

