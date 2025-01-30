---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network
  - registry
  - environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.net_registry_environment;

    import arch.node.engines.net_registry_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Network Registry Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

### `NetworkRegistryMailboxState`

<!-- --8<-- [start:NetworkRegistryMailboxState] -->
```juvix
NetworkRegistryMailboxState : Type := Unit;
```
<!-- --8<-- [end:NetworkRegistryMailboxState] -->

## Local state

### `NetworkRegistryLocalState`

<!-- --8<-- [start:NetworkRegistryLocalState] -->
```juvix
type NetworkRegistryLocalState :=
  mkNetworkRegistryLocalState;
```
<!-- --8<-- [end:NetworkRegistryLocalState] -->

## Timer handles

### `NetworkRegistryTimerHandle`

<!-- --8<-- [start:NetworkRegistryTimerHandle] -->
```juvix
NetworkRegistryTimerHandle : Type := Unit;
```
<!-- --8<-- [end:NetworkRegistryTimerHandle] -->

### `NetworkRegistryTimestampedTrigger`

<!-- --8<-- [start:NetworkRegistryTimestampedTrigger] -->
```juvix
NetworkRegistryTimestampedTrigger : Type :=
  TimestampedTrigger
    NetworkRegistryTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:NetworkRegistryTimestampedTrigger] -->

## Engine Environment

### `NetworkRegistryEnv`

<!-- --8<-- [start:NetworkRegistryEnv] -->
```juvix
NetworkRegistryEnv : Type :=
  EngineEnv
    NetworkRegistryLocalState
    NetworkRegistryMailboxState
    NetworkRegistryTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:NetworkRegistryEnv] -->

#### Instantiation

<!-- --8<-- [start:exNetworkRegistryEnv] -->
```juvix extract-module-statements
module registry_environment_example;

  exNetworkRegistryEnv : NetworkRegistryEnv :=
    mkEngineEnv@{
      localState := mkNetworkRegistryLocalState;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    };
end;
```
<!-- --8<-- [end:exNetworkRegistryEnv] -->
