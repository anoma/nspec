---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- storage-engine
- engine-definition
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.storage;

    import arch.node.net.storage_messages open public;
    import arch.node.net.storage_config open public;
    import arch.node.net.storage_environment open public;
    import arch.node.net.storage_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open storage_config_example;
    open storage_environment_example;
    open storage_behaviour_example;
    ```

# Storage Engine

## Purpose

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
Brief summary of the purpose of the engine.

## Components

- [[Storage Messages]]
- [[Storage Configuration]]
- [[Storage Environment]]
- [[Storage Behaviour]]

## Useful links

- Some
- Useful
- Links

## Type

<!-- --8<-- [start:StorageEngine] -->
```juvix
StorageEngine : Type :=
  Engine
    StorageLocalCfg
    StorageLocalState
    StorageMailboxState
    StorageTimerHandle
    StorageActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:StorageEngine] -->

### Instantiation

<!-- --8<-- [start:exStorageEngine] -->
```juvix
exStorageEngine : StorageEngine :=
  mkEngine@{
    cfg := exStorageCfg;
    env := exStorageEnv;
    behaviour := exStorageBehaviour;
  };
```
<!-- --8<-- [end:exStorageEngine] -->

Where `exStorageCfg` is defined as follows:

--8<-- "./docs/arch/node/net/storage_config.juvix.md:exStorageCfg"

`exStorageEnv` is defined as follows:

--8<-- "./docs/arch/node/net/storage_environment.juvix.md:exStorageEnv"

and `exStorageBehaviour` is defined as follows:

--8<-- "./docs/arch/node/net/storage_behaviour.juvix.md:exStorageBehaviour"
