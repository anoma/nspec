---
icon: octicons/gear-24
search:
  exclude: false
tags:
- engines
- conventions
---

??? quote "Juvix preamble"

    ```juvix
    module arch.node.net.storage;

    import prelude open;
    import arch.node.net.storage_messages open public;
    -- import arch.node.net.storage_environment open public;
    -- import arch.node.net.storage_behaviour open public;
    import arch.node.types.engine open public;
    open template_environment_example;
    ```

# Storage Engine

## Purpose

--8<-- [start:purpose]
The *Storage* engine implements distributed object storage.
Each stored *object* is encrypted using convergent encryption
with a key derived from the hash of the content and a secret key,
then the ciphertext is split into equal-sized parts,
and organized in a Merkle-tree.

A `Chunk` is a Merkle-tree node that is stored by nodes,
with an associated *access control list*
that may limit access to the chunk
to a list of nodes, e.g. publisher or subscribers of a [[Topic]].

Nodes may commit to store a `Chunk` via a `ChunkCommitment` sent to a pub/sub [[Topic]],
and keep track of known commitments by other nodes.
This allows nodes to respond to chunk requests
with either the chunk itself if available locally,
or with a `ChunkCommitment` by a node that stores the requested chunk.
--8<-- [end:purpose]

## Engine Components

- [[Storage Messages]]
- [[Storage Environment]]
- [[Storage Dynamics]]

## Useful links

## Types

### `StorageEngine`

<!-- --8<-- [start:StorageEngine] -->
```juvix
StorageEngine :=
  Engine
    StorageLocalState
    StorageMailboxState
    StorageTimerHandle
    StorageMatchableArgument
    StorageActionLabel
    StoragePrecomputation;
```
<!-- --8<-- [end:StorageEngine] -->

#### Example of a Storage engine

<!-- --8<-- [start:StorageEngine] -->
```juvix
exampleStorageEngine : StorageEngine := mkEngine@{
  name := "storage";
  behaviour := storageBehaviour;
  initEnv := storageEnvironmentExample;
};
```
<!-- --8<-- [end:StorageEngine] -->

where `storageEnvironmentExample` is defined as follows:

--8 TODO <-- "./storage_environment.juvix.md:environment-example"
