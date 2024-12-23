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
    module arch.node.net.storage_messages;

    import arch.node.net.storage_types open;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    import arch.node.types.messages open;
    ```

# Storage Engine

## Types

### `StorageMsgChunkGetRequest`

Request for a *chunk* of an *object*.

```juvix
type ChunkGetRequest := mkChunkRequest {
  chunk : ChunkID;
  children : Either Bool Nat;
}
```

`chunk`
: Chunk ID

`children`
: Request children recursively:
  `False`: none, `True`: all, `Nat`: up to nth level.

### `StorageMsgChunkGetReply`

Reply to a `ChunkGetRequest`.

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

`ChunkGetReplyOkContent`
Reply with chunk content.

`ChunkGetReplyOkCommitment`
Reply with a set of known storage commitments.
Each such commitment contains a `NodeID` that stores the chunk until the time specified.
To retrieve the chunk, the requestor should issue another `ChunkGetRequest` to one of these nodes,
trying them in the order of most recently successfully contacted.

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

### `StorageMsgChunkPutRequest`

Request to store a chunk.
May be restricted to local engines.

### `StorageMsgChunkPutReply`

Reply to a `ChunkPutRequest`.

#### `ChunkPutReplyOk`

Chunk stored successfully or already exists.

```juvix
type ChunkPutReplyOk :=
  | ChunkPutReplyOkStored
  | ChunkPutReplyOkExists
  ;
```

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

### `StorageMsg`

All storage protocol messages.

```juvix
type StorageMsg :=
  | StorageMsgChunkGetRequest ChunkGetRequest
  | StorageMsgChunkGetReply ChunkGetReply
  | StorageMsgChunkPutRequest Chunk
  | StorageMsgChunkPutReply ChunkPutReply
  ;
```

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
