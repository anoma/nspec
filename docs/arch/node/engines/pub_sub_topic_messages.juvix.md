---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- pub-sub-topic-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.pub_sub_topic_messages;

    import arch.node.engines.registry_messages open;
    import arch.node.types.storage open;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Pub/Sub Topic Messages

These are the messages that the *Pub/Sub Topic* engine can receive/respond to.

## Message interface

## `PubSubTopicMsgForward TopicMsg`

A message published in a topic by an authorized publisher,
forwarded to the local node.

### `TopicMsgID`

```juvix
syntax alias TopicMsgID := Digest;
```

### `TopicMsg`

```juvix
type TopicMsg := mkTopicMsg {
  publisher : PublisherID;
  seq : Nat;
  deps : List TopicMsgID;
  seen : List TopicMsgID;
  content : TopicMsgContent;
  sig : Commitment;
}
```

`publisher`
: Publisher identity.

`seq`
: Per-publisher sequence number.

`deps`
: Earlier messages this message depends on.

`seen`
: Independent messages recently seen.

`msg`:
: Encrypted `TopicMsg`.

`sig`
: Signature by `publisher` over the topic ID and the above fields.

### `TopicMsgContent`

```juvix
type TopicMsgContent :=
  | TopicMsgContentMsg ByteString -- Encrypted TopicMsg
  | TopicMsgContentChunk (Pair ByteString Chunk)
  | TopicMsgContentChunkRef (Pair ByteString ChunkCommitment)
  | TopicMsgContentAck TopicMsgAck
  ;
```

`TopicMsgContentMsg`
: Encrypted `TopicMsg`.

`TopicMsgContentChunk`
: Chunk of an object.
  Pair of an encrypted `SecretKey` and a `Chunk`.

`TopicMsgContentChunkRef`
: Reference to the root chunk of an object.
  Pair of an encrypted `SecretKey` and a `ChunkCommitment`.

`TopicMsgContentAck`
: Acknowledgement of a `TopicMsg`.

### `TopicMsgAck`

Acknowledgement of a `TopicMsg`
with commitment to store it until the specified expiry date.

```juvix
type TopicMsgAck := mkTopicMsgAck {
  expiry : AbsTime;
}
```

`expiry`
: Expiry date and time until the node commits to store the event.

## `PubSubTopicSubRequest`

Pub/sub topic subscription request by a local engine or a remote node.

```juvix
type TopicSubRequest := mkTopicSubRequest {
  topic : TopicID;
}
```

## `PubSubTopicSubReply`

Reply to a `TopicSubRequest`.

### `TopicSubReplyOk`

Subscription successful.

```juvix
type TopicSubReplyOk :=
  | TopicSubReplyOkSuccess
  ;
```

### `TopicSubReplyError`

Subscription failed.

```juvix
type TopicSubReplyError :=
  | TopicSubReplyErrorDenied
  ;
```

### `TopicSubReply`

```juvix
TopicSubReply : Type := Result TopicSubReplyOk TopicSubReplyError;
```

## `PubSubTopicUnsubRequest`

Pub/sub topic unsubscription request by a local engine or a remote node.

```juvix
type TopicUnsubRequest := mkTopicUnsubRequest {
  topic : TopicID;
}
```

## `PubSubTopicUnsubReply`

Reply to a `TopicUnsubRequest`

### `TopicUnsubReplyOk`

Unsubscription successful.

```juvix
type TopicUnsubReplyOk :=
  | TopicUnsubReplyOkSuccess
```

### `TopicUnsubReplyError`

Unsubscription failed.

```juvix
type TopicUnsubReplyError :=
  | TopicUnsubReplyErrorNotSubscribed
  ;
```

### `TopicUnsubReply`

```juvix
TopicUnsubReply : Type := Result TopicUnsubReplyOk TopicUnsubReplyError;
```

## `PubSubTopicMsg`

All pub/sub topic  messages.

```juvix
type PubSubTopicMsg :=
  | PubSubTopicMsgForward TopicMsg
  | PubSubTopicMsgSubRequest TopicSubRequest
  | PubSubTopicMsgSubReply TopicSubReply
  | PubSubTopicMsgUnsubRequest TopicUnsubRequest
  | PubSubTopicMsgUnsubReply TopicUnsubReply
  ;
```
