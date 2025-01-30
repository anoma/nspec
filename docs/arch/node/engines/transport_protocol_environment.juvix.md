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
    module arch.node.engines.transport_protocol_environment;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Transport Protocol Environment

## Overview

The [[dynamic environment|Engine environment]] of the engine.

## Mailbox states

```juvix
syntax alias TransportProtocolMailboxState := Unit;
```

## Local state

```juvix
type TransportProtocolLocalState := mkTransportProtocolLocalState;
```

## Timer Handle

```juvix
TransportProtocolTimerHandle : Type := Unit;
```

The [[TransportProtocol Engine Overview|TransportProtocol]] does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

## Timestamped Trigger

<!-- --8<-- [start:TemplateTimestampedTrigger] -->
```juvix
TransportProtocolTimestampedTrigger : Type :=
  TimestampedTrigger
    TransportProtocolTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TemplateTimestampedTrigger] -->

## The Transport Protocol Environment

### `TransportProtocolEnv`

<!-- --8<-- [start:TransportProtocolEnv] -->
```juvix
TransportProtocolEnv : Type :=
  EngineEnv
    TransportProtocolLocalState
    TransportProtocolMailboxState
    TransportProtocolTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:TransportProtocolEnv] -->

#### Instantiation

<!-- --8<-- [start:exTransportProtocolEnv] -->
```juvix extract-module-statements
module transport_protocol_environment_example;

exTransportProtocolEnv : TransportProtocolEnv :=
  mkEngineEnv@{
    localState := mkTransportProtocolLocalState;
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };

end;
```
<!-- --8<-- [end:exTransportProtocolEnv] -->
