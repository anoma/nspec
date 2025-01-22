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
    module arch.node.engines.storage;

    import arch.node.engines.storage_messages open public;
    import arch.node.engines.storage_config open public;
    import arch.node.engines.storage_environment open public;
    import arch.node.engines.storage_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open storage_config_example;
    open storage_environment_example;
    open storage_behaviour_example;
    ```

# Storage Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The *Storage* engine implements distributed object storage.
Each stored *object* is encrypted using convergent encryption
with a key derived from the hash of the content and a secret key,
then the ciphertext is split into equal-sized parts,
and organized in a Merkle-tree.

A `Chunk` is a Merkle-tree node that is stored by nodes in the network.
An associated *access control list*
may limit access to the chunk to a set of nodes,
e.g. publisher or subscribers of a [[Topic]].

Nodes may commit to store a `Chunk` via a `ChunkCommitment`
sent to a pub/sub [[Topic]] or shared directly with certain nodes,
and keep track of known commitments by other nodes.
This allows nodes to respond to chunk requests
with either the chunk itself if available locally,
or with a `ChunkCommitment` by a node that stores the requested chunk.
<!-- --8<-- [end:purpose] -->

## Components

- [[Storage Messages]]
- [[Storage Configuration]]
- [[Storage Environment]]
- [[Storage Behaviour]]

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

--8<-- "./storage_config.juvix.md:exStorageCfg"

`exStorageEnv` is defined as follows:

--8<-- "./storage_environment.juvix.md:exStorageEnv"

and `exStorageBehaviour` is defined as follows:

--8<-- "./storage_behaviour.juvix.md:exStorageBehaviour"
