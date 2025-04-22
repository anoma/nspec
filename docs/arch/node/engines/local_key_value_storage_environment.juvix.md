---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - local-key-value-storage
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.local_key_value_storage_environment;

    import prelude open;
    import arch.node.engines.local_key_value_storage_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Local Key-Value Storage Environment

## Overview

The Local Key-Value Storage Engine provides local storage and
retrieval of data in a key-value format.

??? code "Auxiliary Juvix code"

    ```juvix
    axiom getNotificationTargets : StorageKey -> List EngineID;
    axiom advanceTime : EpochTimestamp -> EpochTimestamp;
    ```

## Mailbox state types

### `LocalKVStorageMailboxState`

<!-- --8<-- [start:LocalKVStorageMailboxState] -->
```juvix
syntax alias LocalKVStorageMailboxState := Unit;
```
<!-- --8<-- [end:LocalKVStorageMailboxState] -->

## Local state

### `LocalKVStorageLocalState`

<!-- --8<-- [start:LocalKVStorageLocalState] -->
```juvix
type LocalKVStorageLocalState := mk {
  storage : Map StorageKey StorageValue;
  localClock : EpochTimestamp
};
```
<!-- --8<-- [end:LocalKVStorageLocalState] -->

???+ code "Arguments"

    `storage`
    : The key-value store mapping keys to values.

    `localClock`
    : The local time of the engine, used to make timestamps.

## Timer handles

### `LocalKVStorageTimerHandle`

<!-- --8<-- [start:LocalKVStorageTimerHandle] -->
```juvix
syntax alias LocalKVStorageTimerHandle := Unit;
```
<!-- --8<-- [end:LocalKVStorageTimerHandle] -->

### `LocalKVStorageTimestampedTrigger`

<!-- --8<-- [start:LocalKVStorageTimestampedTrigger] -->
```juvix
LocalKVStorageTimestampedTrigger : Type :=
  TimestampedTrigger
    LocalKVStorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LocalKVStorageTimestampedTrigger] -->

## The Local Key-Value Storage Environment

### `LocalKVStorageEnv`

<!-- --8<-- [start:LocalKVStorageEnv] -->
```juvix
LocalKVStorageEnv : Type :=
  EngineEnv
    LocalKVStorageLocalState
    LocalKVStorageMailboxState
    LocalKVStorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LocalKVStorageEnv] -->

#### Instantiation

<!-- --8<-- [start:localKVStorageEnv] -->
```juvix extract-module-statements
module local_key_value_storage_environment_example;

  localKVStorageEnv : LocalKVStorageEnv :=
    EngineEnv.mk@{
      localState := LocalKVStorageLocalState.mk@{
        storage := Map.empty;
        localClock := 0;
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:localKVStorageEnv] -->