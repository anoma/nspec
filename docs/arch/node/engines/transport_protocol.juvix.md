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
    module arch.node.engines.transport_protocol;

    import arch.node.engines.transport_protocol_messages open;
    import arch.node.engines.transport_protocol_config open;
    import arch.node.engines.transport_protocol_environment open;
    import arch.node.engines.transport_protocol_behaviour open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open transport_protocol_config_example;
    open transport_protocol_environment_example;
    open transport_protocol_behaviour_example;
    ```

# Transport Protocol Engine

## Purpose

A *Transport Protocol* engine is responsible for accepting and initiating
transport connections for one specific transport protocol, such as QUIC or TLS.

## Engine components

- [[Transport Protocol Messages]]
- [[Transport Protocol Configuration]]
- [[Transport Protocol Environment]]
- [[Transport Protocol Behaviour]]

## The type for a transport protocol engine

<!-- --8<-- [start:TransportProtocolEngine] -->
```juvix
TransportProtocolEngine : Type :=
  Engine
    TransportProtocolLocalCfg
    TransportProtocolLocalState
    TransportProtocolMailboxState
    TransportProtocolTimerHandle
    TransportProtocolActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TransportProtocolEngine] -->

### Example of a transport protocol engine

<!-- --8<-- [start:exTransportProtocolEngine] -->
```juvix
exTransportProtocolEngine : TransportProtocolEngine :=
  Engine.mk@{
    cfg := exTransportProtocolCfg;
    env := exTransportProtocolEnv;
    behaviour := exTransportProtocolBehaviour;
  };
```
<!-- --8<-- [end:exTransportProtocolEngine] -->

Where [[Transport Protocol Configuration#exTransportProtocolCfg|`exTransportProtocolCfg`]] is defined as follows:

--8<-- "./transport_protocol_config.juvix.md:exTransportProtocolCfg"

[[Transport Protocol Environment#exTransportProtocolEnv|`exTransportProtocolEnv`]] is defined as follows:

--8<-- "./transport_protocol_environment.juvix.md:exTransportProtocolEnv"

and [[Transport Protocol Behaviour#exTransportProtocolBehaviour|`exTransportProtocolBehaviour`]] is defined as follows:

--8<-- "./transport_protocol_behaviour.juvix.md:exTransportProtocolBehaviour"
