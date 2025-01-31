---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - local-time-series-storage
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.local_time_series_storage_environment;

    import prelude open;
    import arch.node.engines.local_time_series_storage_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Local Time Series Storage Environment

## Overview

The Local Time Series Storage Engine maintains a database of time series data with query and update capabilities.

## Mailbox state

```juvix
syntax alias LocalTSStorageMailboxState := Unit;
```

## Local state

??? quote "Auxiliary Juvix code"

    ```juvix
    syntax alias Database := String; -- Abstract DB type

    axiom updateDB : Database -> TSStorageDBQuery -> TSStorageDBData -> Database;
    axiom queryDB : Database -> TSStorageDBQuery -> Option TSStorageDBData;
    axiom getNotificationTargets : TSStorageDBQuery -> List EngineID;
    axiom advanceTime : EpochTimestamp -> EpochTimestamp;
    ```

### `LocalTSStorageLocalState`

<!-- --8<-- [start:LocalTSStorageLocalState] -->
```juvix
type LocalTSStorageLocalState :=
  mkLocalTSStorageLocalState {
    db : Database;
    localClock : EpochTimestamp
  };
```
<!-- --8<-- [end:LocalTSStorageLocalState] -->

???+ quote "Arguments"

    `db`
    : The database storing the time series data.

    `localClock`
    : The local time of the engine, used to make timestamps.

## Timer Handle

```juvix
syntax alias LocalTSStorageTimerHandle := Unit;
```

### `LocalTSStorageTimestampedTrigger`

<!-- --8<-- [start:LocalTSStorageTimestampedTrigger] -->
```juvix
LocalTSStorageTimestampedTrigger : Type :=
  TimestampedTrigger
    LocalTSStorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LocalTSStorageTimestampedTrigger] -->

## The Local Time Series Storage Environment

### `LocalTSStorageEnv`

<!-- --8<-- [start:LocalTSStorageEnv] -->
```juvix
LocalTSStorageEnv : Type :=
  EngineEnv
    LocalTSStorageLocalState
    LocalTSStorageMailboxState
    LocalTSStorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LocalTSStorageEnv] -->

#### Instantiation

<!-- --8<-- [start:localTSStorageEnv] -->
```juvix extract-module-statements
module local_ts_storage_environment_example;

  localTSStorageEnv : LocalTSStorageEnv :=
    mkEngineEnv@{
      localState := mkLocalTSStorageLocalState@{
        db := "";
        localClock := 0
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:localTSStorageEnv] -->
