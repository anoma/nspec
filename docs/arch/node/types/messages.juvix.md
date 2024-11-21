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
    import arch.node.types.crypto open;
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

### `EngineMsg`

An *engine message* is a message between engines.
It consists of a sender, a target, an optional *mailbox identifier*, and the message itself.

```juvix
type EngineMsg := mkEngineMsg {
  sender : EngineID;
  target : EngineID;
  mailbox : Option MailboxID;
  msg : Msg;
};
```

### `EngineMsgID`

An *engine message identifier*.
The cryptographic hash of the corresponding `EngineMsg`.

```juvix
syntax alias EngineMsgID := Digest;
```

### `Mailbox S`

A *mailbox* is a container for *engine messages* and optionally a *mailbox state*.
The mailbox state could be used to store additional information about the mailbox,
such as the priority of the messages in the mailbox.

??? info "Where does mailbox state come from?"

    The mailbox state is related to the capabilities of mailboxes of the paper
    [@special-delivery-mailbox-types-2023].
    In particular, at any given point in time,
    a mailbox will have a capability for receiving messages (in later versions of the specs).
    As mailbox state can be useful in general, we already have it now.

```juvix
type Mailbox S := mkMailbox@{
  messages : List EngineMsg;
  mailboxState : Option S;
};
```

### `MailboxID`

A *mailbox identifier* is a natural number used to index mailboxes.

??? info "Where do mailbox identifiers come from?"

    The concept of mailbox identifier is taken from
    the paper
    [@special-delivery-mailbox-types-2023]
    (see also [[Mailbox Cluster]] and [@selectors-actors-2014]).

```juvix
syntax alias MailboxID := Nat;
```

### `Timer H`

```juvix
type Timer H := mkTimer@{
  time : Time;
  handle : H;
};
```

### `Trigger H`

```juvix
type Trigger H :=
  | MessageArrived { msg : EngineMsg; }
  | Elapsed { timers : List (Timer H) };
```

- Extract the `EngineMsg` from a trigger in case it has one:

    ```juvix
    getEngineMsgFromTrigger {H} (tr : Trigger H) : Option EngineMsg
      := case tr of {
      | MessageArrived@{msg} := some msg
      | Elapsed@{} := none
      };
    ```

- Extract the `Msg` from a trigger in case it has one:

    ```juvix
    getMsgFromTrigger {H} (tr : Trigger H) : Option Msg
      := case tr of {
      | MessageArrived@{msg} := some (EngineMsg.msg msg)
      | Elapsed@{} := none
      };
    ```

- Get the message sender from a trigger:

    ```juvix
    getSenderFromTrigger {H} (tr : Trigger H) : Option EngineID
      := case tr of {
      | MessageArrived@{msg} := some (EngineMsg.sender msg)
      | Elapsed@{} := none
      };
    ```

- Get the target destination from a trigger:

    ```juvix
    getTargetFromTrigger {H} (tr : Trigger H) : Option EngineID
      := case tr of {
      | MessageArrived@{msg} := some (EngineMsg.target msg)
      | Elapsed@{} := none
      };
    ```

### `TimestampedTrigger H`

```juvix
type TimestampedTrigger H :=
  mkTimestampedTrigger@{
    time : Time;
    trigger : Trigger H;
  };
```

- Get the `EngineMsg` from a `TimestampedTrigger`:

    ```juvix
    getEngineMsgFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option EngineMsg
      := getEngineMsgFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the `Msg` from a `TimestampedTrigger`:

    ```juvix
    getMsgFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option Msg
      := getMsgFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the sender from a `TimestampedTrigger`:

    ```juvix
    getSenderFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option EngineID
      := getSenderFromTrigger (TimestampedTrigger.trigger tr);
    ```

- Get the target from a `TimestampedTrigger`:

    ```juvix
    getTargetFromTimestampedTrigger {H} (tr : TimestampedTrigger H) : Option EngineID
      := getTargetFromTrigger (TimestampedTrigger.trigger tr);
    ```
