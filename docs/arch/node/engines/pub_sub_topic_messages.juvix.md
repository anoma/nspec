---
icon: material/message-draw
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - pub-sub-topic
  - message-types
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.pub_sub_topic_messages;

    import arch.node.engines.net_registry_messages open;
    import arch.node.types.storage open;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Pub/Sub Topic Messages

These are the messages that the *Pub/Sub Topic* engine can receive/respond to.

## Message interface

--8<-- "./pub_sub_topic_messages.juvix.md:PubSubTopicMsg"

<!-- TODO: add message sequence diagrams -->

## Message types

---

### `TopicMsg`

A message published in a topic by an authorized publisher,
forwarded to the local node.

???+ code "Auxiliary type"

    #### `TopicMsgID`

    ```juvix
    syntax alias TopicMsgID := Digest;
    ```


```juvix
type TopicMsg := mkTopicMsg@{
  publisher : PublisherID;
  seq : Nat;
  deps : List TopicMsgID;
  seen : List TopicMsgID;
  content : TopicMsgContent;
  sig : Commitment;
}
```

???+ code "Arguments"

    `publisher`
    : Publisher identity.

    `seq`
    : Per-publisher sequence number.

    `deps`
    : Earlier messages this message depends on.

    `seen`
    : Independent messages recently seen.

    `content`:
    : Encrypted `TopicMsg`.

    `sig`
    : Signature by `publisher` over the topic ID and the above fields.

---

### `TopicMsgContent`

```juvix
type TopicMsgContent :=
  | TopicMsgContentMsg ByteString
  | TopicMsgContentChunk (Pair ByteString Chunk)
  | TopicMsgContentChunkRef (Pair ByteString ChunkCommitment)
  | TopicMsgContentAck TopicMsgAck
  ;
```

???+ code "TopicMsgContent constructors"

    `TopicMsgContentMsg`
    : Encrypted `TopicMsg`.

    `TopicMsgContentChunk`
    : Chunk of an object. Pair of an encrypted `SecretKey` and a `Chunk`.

    `TopicMsgContentChunkRef`
    : Reference to the root chunk of an object. Pair of an encrypted `SecretKey`
    and a `ChunkCommitment`.

    `TopicMsgContentAck`
    : Acknowledgement of a `TopicMsg`.

---

### `TopicMsgAck`

Acknowledgement of a `TopicMsg` with commitment to store it until the specified
expiry date.

```juvix
type TopicMsgAck := mkTopicMsgAck@{
  expiry : AbsTime;
}
```

???+ code "Arguments"

    `expiry`
    : Expiry date and time until the node commits to store the event.

---

### `TopicSubRequest`

Pub/sub topic subscription request by a local engine or a remote node.

```juvix
type TopicSubRequest := mkTopicSubRequest@{
  topic : TopicID;
}
```

---

### `TopicSubReply`

Reply to a `TopicSubRequest`.

???+ code "Auxiliary type"

    #### `TopicSubReplyOk`

    Subscription successful.

    ```juvix
    type TopicSubReplyOk :=
      | TopicSubReplyOkSuccess
      ;
    ```

    #### `TopicSubReplyError`

    Subscription failed.

    ```juvix
    type TopicSubReplyError :=
      | TopicSubReplyErrorDenied
      ;
    ```

```juvix
TopicSubReply : Type := Result TopicSubReplyOk TopicSubReplyError;
```
---

### `TopicUnsubRequest`

Pub/sub topic unsubscription request by a local engine or a remote node.

```juvix
type TopicUnsubRequest := mkTopicUnsubRequest@{
  topic : TopicID;
}
```

---

### `TopicUnsubReply`

Unsubscription successful.

???+ code "Auxiliary type"

    #### `TopicUnsubReplyOk`

    ```juvix
    type TopicUnsubReplyOk :=
      | TopicUnsubReplyOkSuccess
      ;
    ```

    #### `TopicUnsubReplyError`

    Unsubscription failed.

    ```juvix
    type TopicUnsubReplyError :=
      | TopicUnsubReplyErrorNotSubscribed
      ;
    ```

```juvix
TopicUnsubReply : Type := Result TopicUnsubReplyOk TopicUnsubReplyError;
```

---

### `PubSubTopicMsg`

All pub/sub topic  messages.

<!-- --8<-- [start:PubSubTopicMsg] -->
```juvix
type PubSubTopicMsg :=
  | PubSubTopicMsgForward TopicMsg
  | PubSubTopicMsgSubRequest TopicSubRequest
  | PubSubTopicMsgSubReply TopicSubReply
  | PubSubTopicMsgUnsubRequest TopicUnsubRequest
  | PubSubTopicMsgUnsubReply TopicUnsubReply
  ;
```
<!-- --8<-- [end:PubSubTopicMsg] -->
---

## Engine components

- [[Pub/Sub Topic Configuration]]
- [[Pub/Sub Topic Environment]]
- [[Pub/Sub Topic Behaviour]]
