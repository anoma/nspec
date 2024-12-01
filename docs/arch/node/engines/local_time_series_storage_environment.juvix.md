---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- local-ts-storage-engine
- engine-environment
---

??? note "Juvix imports"

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

The environment contains the state and context needed for the time series storage engine to operate, including its mailbox states, local state, and timer handles.

## Mailbox state types

### `LocalTSStorageMailboxState`

<!-- --8<-- [start:LocalTSStorageMailboxState] -->
```juvix
type LocalTSStorageMailboxState := Unit;
```
<!-- --8<-- [end:LocalTSStorageMailboxState] -->

## Local state

### `LocalTSStorageLocalState`

<!-- --8<-- [start:LocalTSStorageLocalState] -->
```juvix
type LocalTSStorageLocalState :=
  mkLocalTSStorageLocalState {
    database : Map TSStorageDBQuery TSStorageDBData
};
```
<!-- --8<-- [end:LocalTSStorageLocalState] -->

???+ quote "Arguments"

    `database`
    : The key-value store mapping queries to time series data.

## Timer handles

??? quote "Auxiliary Juvix code"

    <!-- --8<-- [start:ArgOne] -->
    ```juvix
    syntax alias ArgOne := Nat;
    ```
    <!-- --8<-- [end:ArgOne] -->

### `LocalTSStorageTimerHandleFirstOption FirstOptionTimerHandle`

<!-- --8<-- [start:FirstOptionTimerHandle] -->
```juvix
type FirstOptionTimerHandle := mkFirstOptionTimerHandle {
  argOne : ArgOne
};
```
<!-- --8<-- [end:FirstOptionTimerHandle] -->

A basic timer handle used for scheduling data maintenance tasks.

???+ quote "Arguments"

    `argOne`

    : The scheduled time for the maintenance task.

### `LocalTSStorageTimerHandleSecondOption SecondOptionTimerHandle`

<!-- --8<-- [start:SecondOptionTimerHandle] -->
```juvix
type SecondOptionTimerHandle := mkSecondOptionTimerHandle {
  argOne : String;
  argTwo : Bool
};
```
<!-- --8<-- [end:SecondOptionTimerHandle] -->

???+ quote "Arguments"

    `argOne`

    : The identifier for the scheduled operation.

    `argTwo`

    : Whether the operation is a recurring task.

### `LocalTSStorageTimerHandle`

<!-- --8<-- [start:LocalTSStorageTimerHandle] -->
```juvix
type LocalTSStorageTimerHandle :=
  | LocalTSStorageTimerHandleFirstOption FirstOptionTimerHandle
  | LocalTSStorageTimerHandleSecondOption SecondOptionTimerHandle;
```
<!-- --8<-- [end:LocalTSStorageTimerHandle] -->

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
        database := Map.empty
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:localTSStorageEnv] -->
