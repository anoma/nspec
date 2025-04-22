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

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.transport_connection_environment;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Transport Connection Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox states

```juvix
syntax alias TransportConnectionMailboxState := Unit;
```

## Local state

```juvix
type TransportConnectionLocalState := mk;
```

## Timer Handle

```juvix
TransportConnectionTimerHandle : Type := Unit;
```

The [[TransportConnection Engine Overview|TransportConnection]] does not require
a timer handle type. Therefore, we define the timer handle type as `Unit`.

## Timestamped Trigger

<!-- --8<-- [start:TemplateTimestampedTrigger] -->
```juvix
TransportConnectionTimestampedTrigger : Type :=
  TimestampedTrigger
    TransportConnectionTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateTimestampedTrigger] -->

## The Transport Connection Environment

### `TransportConnectionEnv`

<!-- --8<-- [start:TransportConnectionEnv] -->
```juvix
TransportConnectionEnv : Type :=
  EngineEnv
    TransportConnectionLocalState
    TransportConnectionMailboxState
    TransportConnectionTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TransportConnectionEnv] -->

#### Instantiation

<!-- --8<-- [start:exTransportConnectionEnv] -->
```juvix extract-module-statements
module transport_connection_environment_example;

exTransportConnectionEnv : TransportConnectionEnv :=
  EngineEnv.mk@{
    localState := TransportConnectionLocalState.mk;
    mailboxCluster := Map.empty;
    acquaintances := Set.Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:exTransportConnectionEnv] -->
