---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
- node
tags:
- local-ts-storage-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.local_time_series_storage;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.local_time_series_storage_messages open public;
    import arch.node.engines.local_time_series_storage_config open public;
    import arch.node.engines.local_time_series_storage_environment open public;
    import arch.node.engines.local_time_series_storage_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open local_ts_storage_config_example;
    open local_ts_storage_environment_example;
    ```

# Local Time Series Storage Engine

The Local Time Series Storage Engine provides local storage and
retrieval of time series data.

## Purpose

The Local Time Series Storage Engine manages local storage and
retrieval of time series data. It provides functions for recording
new data, retrieving existing data, and deleting data when needed.

!!! todo

    look into synchronous interaction for storage in future versions:

    > It provides functions

    That's technically not correct, though intuitively true.

## Engine components

- [[Local Time Series Storage Messages]]
- [[Local Time Series Storage Configuration]]
- [[Local Time Series Storage Environment]]
- [[Local Time Series Storage Behaviour]]

## Type

<!-- --8<-- [start:LocalTSStorageEngine] -->
```juvix
LocalTSStorageEngine : Type :=
  Engine
    LocalTSStorageCfg
    LocalTSStorageLocalState
    LocalTSStorageMailboxState
    LocalTSStorageTimerHandle
    LocalTSStorageActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:LocalTSStorageEngine] -->

### Example of a local time series storage engine

<!-- --8<-- [start:exampleLocalTSStorageEngine] -->
```juvix
exampleLocalTSStorageEngine : LocalTSStorageEngine :=
  mkEngine@{
    cfg := localTSStorageCfg;
    env := localTSStorageEnv;
    behaviour := localTSStorageBehaviour;
  };
```
<!-- --8<-- [end:exampleLocalTSStorageEngine] -->

where `localTSStorageCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/local_time_series_storage_config.juvix.md:localTSStorageCfg"

`localTSStorageEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/local_time_series_storage_environment.juvix.md:localTSStorageEnv"

and `localTSStorageBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/local_time_series_storage_behaviour.juvix.md:localTSStorageBehaviour"
