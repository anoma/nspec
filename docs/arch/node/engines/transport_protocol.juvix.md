  ---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-protocol-engine
- engine-definition
---

??? quote "Juvix imports"

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

<!-- --8<-- [start:purpose] -->
A *Transport Protocol* engine is responsible for accepting and initiating transport connections
for one specific transport protocol, such as QUIC or TLS.
<!-- --8<-- [end:purpose] -->

## Engine Components

- [[Transport Protocol Messages]]
- [[Transport Protocol Configuration]]
- [[Transport Protocol Environment]]
- [[Transport Protocol Behaviour]]

## Type

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

### Instantiation

<!-- --8<-- [start:exTransportProtocolEngine] -->
```juvix
exTransportProtocolEngine : TransportProtocolEngine :=
  mkEngine@{
    cfg := exTransportProtocolCfg;
    env := exTransportProtocolEnv;
    behaviour := exTransportProtocolBehaviour;
  };
```
<!-- --8<-- [end:exTransportProtocolEngine] -->

Where `exTransportProtocolCfg` is defined as follows:

--8<-- "./transport_protocol_config.juvix.md:exTransportProtocolCfg"

`exTransportProtocolEnv` is defined as follows:

--8<-- "./transport_protocol_environment.juvix.md:exTransportProtocolEnv"

and `exTransportProtocolBehaviour` is defined as follows:

--8<-- "./transport_protocol_behaviour.juvix.md:exTransportProtocolBehaviour"
