  ---
icon: octicons/gear-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - transport
  - engine-definition
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.transport_connection;

    import arch.node.engines.transport_connection_messages open;
    import arch.node.engines.transport_connection_config open;
    import arch.node.engines.transport_connection_environment open;
    import arch.node.engines.transport_connection_behaviour open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open transport_connection_config_example;
    open transport_connection_environment_example;
    open transport_connection_behaviour_example;
    ```

# Transport Connection Engine

## Purpose

A *Transport Protocol* engine is responsible for accepting and initiating
transport connections for one specific transport protocol, such as QUIC or TLS.

## Engine components

- [[Transport Connection Messages]]
- [[Transport Connection Configuration]]
- [[Transport Connection Environment]]
- [[Transport Connection Behaviour]]

## The type for a transport connection engine

<!-- --8<-- [start:TransportConnectionEngine] -->
```juvix
TransportConnectionEngine : Type :=
  Engine
    TransportConnectionLocalCfg
    TransportConnectionLocalState
    TransportConnectionMailboxState
    TransportConnectionTimerHandle
    TransportConnectionActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TransportConnectionEngine] -->

### Example of a transport connection engine

<!-- --8<-- [start:exTransportConnectionEngine] -->
```juvix
exTransportConnectionEngine : TransportConnectionEngine :=
  Engine.mk@{
    cfg := exTransportConnectionCfg;
    env := exTransportConnectionEnv;
    behaviour := exTransportConnectionBehaviour;
  };
```
<!-- --8<-- [end:exTransportConnectionEngine] -->

Where [[Transport Connection Configuration#exTransportConnectionCfg|`exTransportConnectionCfg`]] is defined as follows:

--8<-- "./transport_connection_config.juvix.md:exTransportConnectionCfg"

[[Transport Connection Environment#exTransportConnectionEnv|`exTransportConnectionEnv`]] is defined as follows:

--8<-- "./transport_connection_environment.juvix.md:exTransportConnectionEnv"

and [[Transport Connection Behaviour#exTransportConnectionBehaviour|`exTransportConnectionBehaviour`]] is defined as follows:

--8<-- "./transport_connection_behaviour.juvix.md:exTransportConnectionBehaviour"
