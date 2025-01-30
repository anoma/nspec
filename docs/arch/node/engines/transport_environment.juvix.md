---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - transport
  - environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.transport_environment;

    import arch.node.engines.transport_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Transport Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox state

### `TransportMailboxState`

<!-- --8<-- [start:TransportMailboxState] -->
```juvix
TransportMailboxState : Type := Unit;
```
<!-- --8<-- [end:TransportMailboxState] -->

## Local state

### `TransportLocalState`

<!-- --8<-- [start:TransportLocalState] -->
```juvix
type TransportLocalState :=
  mkTransportLocalState;
```
<!-- --8<-- [end:TransportLocalState] -->

## Timer handles

### `TransportTimerHandle`

<!-- --8<-- [start:TransportTimerHandle] -->
```juvix
TransportTimerHandle : Type := Unit;
```
<!-- --8<-- [end:TransportTimerHandle] -->

### `TransportTimestampedTrigger`

<!-- --8<-- [start:TransportTimestampedTrigger] -->
```juvix
TransportTimestampedTrigger : Type :=
  TimestampedTrigger
    TransportTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TransportTimestampedTrigger] -->

## The Transport Environment

### `TransportEnv`

<!-- --8<-- [start:TransportEnv] -->
```juvix
TransportEnv : Type :=
  EngineEnv
    TransportLocalState
    TransportMailboxState
    TransportTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TransportEnv] -->

#### Instantiation

<!-- --8<-- [start:transportEnv] -->
```juvix extract-module-statements
module transport_environment_example;

  transportEnv : TransportEnv :=
    mkEngineEnv@{
      localState := mkTransportLocalState;
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:transportEnv] -->
