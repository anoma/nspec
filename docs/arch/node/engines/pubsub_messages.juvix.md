# Juvix imports

??? quote "Juvix imports"

    ```juvix
    module node_architecture.engines.network_messages;
    import node_architecture.types.basics open;
    import node_architecture.types.crypto open;
    import node_architecture.types.identities open;
    import node_architecture.types.messages open;
    import node_architecture.types.network open;
    import prelude open public;
    ```

# PubSub Engine

## `TopicEvent`

An event published in a topic by a publisher.

```juvix
type TopicEvent : Type :=
  mkTopicEvent {
    publisher : PublisherID;
    seq : Nat;
    deps : List Digest;
    seen : List Digest;
    msg : TopicMessage;
    sig : Commitment;
  }
```

`publisher`
: Publisher identity.

`seq`
: Sequence number of publisher.

`deps`
: Events this event depends on.

`seen`
: Independent events recently seen.

`msg`:
: Encrypted `TopicMessage`.

`sig`
: Signature by `publisher` over the above fields.

## `BlockRequest`

Request a remote node for a storage block.

```juvix
type BlockRequest : Type :=
  mkBlockRequest {
    block : BlockID;
    include_children : Bool;
  }
```

## `BlockOk`

Subscription successful.

```juvix
type BlockOk : Type :=
  | BlockOkFound Byte
```

## `SubError`

Subscription failed.

```juvix
type SubError : Type :=
  | SubErrorDenied
  ;
```

## `SubReply`

Reply to a `SubRequest`

```juvix
SubReply : Type := Result SubOk SubError;
```

-- ------

## `SubRequest`

Pub/sub topic subscription request at a remote node.

```juvix
type SubRequest : Type :=
  mkSubRequest {
    topic : TopicID;
  }
```

## `SubOk`

Subscription successful.

```juvix
type SubOk : Type :=
  | SubOkSuccess
```

## `SubError`

Subscription failed.

```juvix
type SubError : Type :=
  | SubErrorDenied
  ;
```

## `SubReply`

Reply to a `SubRequest`

```juvix
SubReply : Type := Result SubOk SubError;
```

## `UnsubRequest`

Pub/sub topic unsubscription request at a remote node.

```juvix
type UnsubRequest : Type :=
  mkUnsubRequest {
    topic : TopicID;
  }
```

## `UnsubOk`

Unsubscription successful.

```juvix
type UnsubOk : Type :=
  | UnsubOkSuccess
```

## `UnsubError`

Unsubscription failed.

```juvix
type UnsubError : Type :=
  | UnsubErrorNotSubscribed
  ;
```

## `UnsubReply`

Reply to an `UnsubRequest`

```juvix
--- Reply to a UnsubRequest
UnsubReply : Type := Result UnsubOk UnsubError;
```

## `LocalSubRequest`

Pub/sub topic subscription request by a local engine.

```juvix
type LocalSubRequest : Type :=
  mkLocalSubRequest {
    topic : TopicID;
  }
```

## `LocalSubOk`

Subscription successful.

```juvix
type LocalSubOk : Type :=
  | LocalSubOkSuccess
```

## `LocalSubError`

Subscription failed.

```juvix
type LocalSubError : Type :=
  | LocalSubErrorDenied
  ;
```

## `LocalSubReply`

Reply to a `LocalSubRequest`

```juvix
LocalSubReply : Type := Result LocalSubOk LocalSubError;
```

## `LocalUnsubRequest`

Pub/sub topic subscription request by a local engine.

```juvix
type LocalUnsubRequest : Type :=
  mkLocalUnsubRequest {
    topic : TopicID;
  }
```

## `LocalUnsubOk`

Unsubscription successful.

```juvix
type LocalUnsubOk : Type :=
  | LocalUnsubOkSuccess
```

## `LocalUnsubError`

Unsubscription failed.

```juvix
type LocalUnsubError : Type :=
  | LocalUnsubErrorNotSubscribed
  ;
```

## `LocalUnsubReply`

Reply to a `LocalUnsubRequest`

```juvix
--- Reply to a LocalUnsubRequest
LocalUnsubReply : Type := Result LocalUnsubOk LocalUnsubError;
```

## `PubsubMsg`

All pub/sub protocol messages.

```juvix
type PubsubMsg :=
  | MsgSubRequest SubRequest
  | MsgSubOk SubOk
--  | MsgSubError SubError
  | MsgSubReply SubReply
  | MsgUnsubRequest UnsubRequest
  | MsgUnsubOk UnsubOk
  | MsgUnsubError UnsubError
  | MsgUnsubReply UnsubReply

  | MsgLocalSubRequest LocalSubRequest
  | MsgLocalSubOk LocalSubOk
  | MsgLocalSubError LocalSubError
  | MsgLocalSubReply LocalSubReply
  | MsgLocalUnsubRequest LocalUnsubRequest
  | MsgLocalUnsubOk LocalUnsubOk
  | MsgLocalUnsubError LocalUnsubError
  | MsgLocalUnsubReply LocalUnsubReply
  ;
```