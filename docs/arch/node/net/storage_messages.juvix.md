# Juvix imports

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.storage_messages;

    import arch.node.net.storage_types open;
    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    -- import arch.node.types.messages open;
    import prelude open public;
    ```

# Storage Engine

## Types

### `MsgStorageChunkGetRequest`

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

### `MsgStorageChunkGetReply`

Reply to a `ChunkGetRequest`.

#### `ChunkGetReplyOk`

Chunk found.

When available, the chunk contents are returned,
otherwise a list of commitments by nodes that store the chunk.

```juvix
type ChunkGetReplyOk :=
  | ChunkGetReplyOkContent Chunk
  | ChunkGetReplyOkCommitment (List ChunkCommitment)
  ;
```

#### `ChunkGetReplyError`

Chunk not found.

```juvix
type ChunkGetReplyError :=
  | ChunkGetReplyErrorNotFound
  ;
```

```juvix
ChunkGetReply := Result ChunkGetReplyOk ChunkGetReplyError;
```

### `MsgStorageChunkPutRequest`

Request to store a chunk.
May be restricted to local engines.

### `MsgStorageChunkPutReply`

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
ChunkPutReply := Result ChunkPutReplyOk ChunkPutReplyError;
```

### `MsgStorage`

All storage protocol messages.

```juvix
type MsgStorage :=
  | MsgStorageChunkGetRequest ChunkGetRequest
  | MsgStorageChunkGetReply ChunkGetReply
  | MsgStorageChunkPutRequest Chunk
  | MsgStorageChunkPutReply ChunkPutReply
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
