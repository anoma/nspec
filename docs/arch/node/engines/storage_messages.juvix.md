---
icon: material/message-draw
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-messages
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.storage_messages;

    import arch.node.types.storage open;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Storage Engine

## Message interface

--8<-- "./storage_messages.juvix.md:StorageMsg"

## Message sequence diagrams

---


## Message sequence diagrams

### Storage

<!-- --8<-- [start:message-sequence-diagram] -->
<figure markdown="span">

```mermaid
sequenceDiagram
```

<figcaption markdown="span">
Chunk request & response.
</figcaption>
</figure>
<!-- --8<-- [end:message-sequence-diagram] -->

## Message types

---

### `ChunkGetRequest`

Request for a *chunk* of an *object*.

Source: any local engine or remote [[Storage]] engine.

```juvix
type ChunkGetRequest := mkChunkRequest {
  chunk : ChunkID;
  children : Either Bool Nat;
}
```

???+ quote "Arguments"

    `chunk`
    : Chunk ID

    `children`
    : Request children recursively:

      - `False`: none,
      - `True`: all,
      - `Nat`: up to nth level.

### `ChunkGetReply`

Reply to a `ChunkGetRequest`.

---

#### `ChunkGetReplyOk`

Chunk found.

When available, the chunk contents are returned,
otherwise a list of commitments by nodes that store the chunk.

```juvix
type ChunkGetReplyOk :=
  | ChunkGetReplyOkContent Chunk
  | ChunkGetReplyOkCommitment (Set ChunkCommitment)
  ;
```

???+ quote "`ChunkGetReplyOk` constructors"

    `ChunkGetReplyOkContent`
    : Reply with chunk content.

    `ChunkGetReplyOkCommitment`
    : Reply with a set of known storage commitments.
    Each such commitment contains a `NodeID` that stores the chunk until the time specified.
    To retrieve the chunk, the requestor should issue another `ChunkGetRequest` to one of these nodes,
    trying them in the order of most recently successfully contacted.

---

#### `ChunkGetReplyError`

Chunk not found.

```juvix
type ChunkGetReplyError :=
  | ChunkGetReplyErrorNotFound
  ;
```

```juvix
ChunkGetReply : Type := Result ChunkGetReplyOk ChunkGetReplyError;
```

---

### `ChunkPutRequest`

Request to store a chunk.
May be restricted to local engines.

---

### `ChunkPutReply`

Reply to a `ChunkPutRequest`.

---

#### `ChunkPutReplyOk`

Chunk stored successfully or already exists.

```juvix
type ChunkPutReplyOk :=
  | ChunkPutReplyOkStored
  | ChunkPutReplyOkExists
  ;
```

---

#### `ChunkPutReplyError`

Failed to store chunk.

```juvix
type ChunkPutReplyError :=
  | ChunkPutReplyErrorFailed
  ;
```

```juvix
ChunkPutReply : Type := Result ChunkPutReplyOk ChunkPutReplyError;
```

---

### `StorageMsg`

All storage protocol messages.

<!-- --8<-- [start:StorageMsg] -->
```juvix
type StorageMsg :=
  | StorageMsgChunkGetRequest ChunkGetRequest
  | StorageMsgChunkGetReply ChunkGetReply
  | StorageMsgChunkPutRequest Chunk
  | StorageMsgChunkPutReply ChunkPutReply
  ;
```
<!-- --8<-- [end:StorageMsg] -->

## Engine components

- [[Storage Configuration]]
- [[Storage Environment]]
- [[Storage Behaviour]]
