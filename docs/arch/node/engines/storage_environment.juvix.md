---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - storage
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.storage_environment;

    import arch.node.engines.storage_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Storage Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

### `StorageMailboxState`

<!-- --8<-- [start:StorageMailboxState] -->
```juvix
StorageMailboxState : Type := Unit;
```
<!-- --8<-- [end:StorageMailboxState] -->

## Local state

### `StorageLocalState`

<!-- --8<-- [start:StorageLocalState] -->
```juvix
type StorageLocalState :=
  mk;
```
<!-- --8<-- [end:StorageLocalState] -->

## Timer handles

### `StorageTimerHandle`

<!-- --8<-- [start:StorageTimerHandle] -->
```juvix
StorageTimerHandle : Type := Unit;
```
<!-- --8<-- [end:StorageTimerHandle] -->

### `StorageTimestampedTrigger`

<!-- --8<-- [start:StorageTimestampedTrigger] -->
```juvix
StorageTimestampedTrigger : Type :=
  TimestampedTrigger
    StorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:StorageTimestampedTrigger] -->

## Engine Environment

### `StorageEnv`

<!-- --8<-- [start:StorageEnv] -->
```juvix
StorageEnv : Type :=
  EngineEnv
    StorageLocalState
    StorageMailboxState
    StorageTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:StorageEnv] -->

#### Instantiation

<!-- --8<-- [start:exStorageEnv] -->
```juvix extract-module-statements
module storage_environment_example;

exStorageEnv : StorageEnv :=
  EngineEnv.mk@{
    localState := StorageLocalState.mk;
    mailboxCluster := Map.empty;
    acquaintances := Set.Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:exStorageEnv] -->
