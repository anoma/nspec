---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- local-key-value-storage-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.local_key_value_storage;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.local_key_value_storage_messages open public;
    import arch.node.engines.local_key_value_storage_environment open public;
    import arch.node.engines.local_key_value_storage_behaviour open public;
    import arch.node.engines.local_key_value_storage_config open public;

    import arch.node.types.anoma as Anoma open;

    open local_key_value_storage_config_example;
    open local_key_value_storage_environment_example;
    ```

# Local Key-Value Storage Engine

## Purpose

The Local Key-Value Storage Engine provides the local storage and retrieval of data in a key-value format.

## Components

- [[Local Key-Value Storage Messages]]
- [[Local Key-Value Storage Config]]
- [[Local Key-Value Storage Environment]]
- [[Local Key-Value Storage Behaviour]]

## Type

<!-- --8<-- [start:LocalKVStorageEngine] -->
```juvix
LocalKVStorageEngine : Type :=
  Engine
    LocalKVStorageCfg
    LocalKVStorageLocalState
    LocalKVStorageMailboxState
    LocalKVStorageTimerHandle
    LocalKVStorageActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:LocalKVStorageEngine] -->

### Example of a local key-value storage engine

<!-- --8<-- [start:exampleLocalKVStorageEngine] -->
```juvix
exampleLocalKVStorageEngine : LocalKVStorageEngine :=
  mkEngine@{
    cfg := localKVStorageCfg;
    env := localKVStorageEnv;
    behaviour := localKVStorageBehaviour;
  };
```
<!-- --8<-- [end:exampleLocalKVStorageEngine] -->

where `localKVStorageCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/local_key_value_storage_config.juvix.md:localKVStorageCfg"

`localKVStorageEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/local_key_value_storage_environment.juvix.md:localKVStorageEnv"

and `localKVStorageBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/local_key_value_storage_behaviour.juvix.md:localKVStorageBehaviour"