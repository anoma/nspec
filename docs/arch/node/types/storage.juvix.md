---
icon: material/file-document-outline
search:
  exclude: false
  boost: 2
tags:
  - node-architecture
  - types
  - network-subsystem
  - storage
  - prelude
---

??? code "Juvix imports"

    ```juvix
    module arch.node.types.storage;

    import prelude open;

    import arch.node.types.basics open;
    import arch.node.types.crypto open;
    import arch.node.types.identities open;
    ```

# Storage Types

---

## `ACL`

Access control list stored in a [[Storage]] object.

Contains `ExternalID`s that are members of the list,
the version of the ACL, which is incremented at each update,
and a signature by the ACL owner.

The ACL may be updated by sending an updated version
to a pub/sub topic identified by the ACL owner's `ExternalID`.

```juvix
type ACL := mkACL@{
  members : Set ExternalID;
  version : Nat;
  sig : Commitment;
}
```

???+ code "Arguments"

    `members`
    : Set of `ExternalID`s that are members of the ACL.

    `version`
    : Version of the ACL.

    `sig`
    : Signature of the ACL by the ACL owner.

---

## `Chunk`

A chunk of a storage object.

```juvix
type Chunk := mkChunk@{
  children : List ChunkID;
  expiry : AbsTime;
  acl : Option ACL;
  content : ByteString;
};
```

???+ code "Arguments"

    `children`
    : List of chunk IDs of children in the Merkle tree.

    `expiry`
    : Expiration time after which the chunk must be deleted by each node storing it.

    `content`
    : Encrypted `ChunkContent`.

    `acl`
    : Nodes that are allowed to request the chunk.

---

## `ChunkContent`

The content of a `Chunk`.

```juvix
type ChunkContent :=
  | InternalNode (List SecretKey)
  | LeafNode ByteString
  ;
```

???+ code "`ChunkContent` constructors"

    `InternalNode`
    : An internal node of the Merkle tree. Contains decryption keys of its children.

    `LeafNode`
    : A leaf node of the Merkle tree. Contains a data chunk.

---

## `ChunkCommitment`

Commitment by a node to store a chunk for a certain period of time.

Contains a reference to a `Chunk`,
along with the `NodeID` where it is stored,
and an expiry time

```juvix
type ChunkCommitment := mkChunkCommitment {
  chunk : ChunkID;
  node : NodeID;
  expiry : AbsTime;
  sig : Commitment;
};
```

???+ code "Arguments"

    `id`
    : `ChunkID` to commit to.

    `node`
    : `NodeID` where the `Chunk` can be found.

    `expiry`
    : Expiration time, until `node` guarantees storage.

    `sig`
    : Cryptographic signature of the above fields by `node`.

---