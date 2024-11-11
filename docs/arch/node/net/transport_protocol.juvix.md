---
icon: octicons/gear-24
search:
  exclude: false
tags:
- engines
- conventions
---

??? quote "Juvix preamble"

    ```juvix
    module arch.node.net.transport;

    import prelude open;
    import arch.node.net.transport_messages open;
    -- import arch.node.net.transport_environment open;
    -- import arch.node.net.transport_behaviour open;
    import arch.node.types.engine open;
    open template_environment_example;
    ```

# Transport Protocol Engine

## Purpose

--8<-- [start:purpose]
A *Transport Protocol* engine is responsible for accepting and initiating transport connections
for one specific transport protocol, such as QUIC or TLS.
--8<-- [end:purpose]

## Engine Components

- [[Transport Protocol Messages]]
- [[Transport Protocol Environment]]
- [[Transport Protocol Dynamics]]

## Useful links

## Types

### `TransportProtocolEngine`

<!-- --8<-- [start:TransportProtocolEngine] -->
```juvix
TransportProtocolEngine : Type :=
  Engine
    TransportProtocolLocalState
    TransportProtocolMailboxState
    TransportProtocolTimerHandle
    TransportProtocolMatchableArgument
    TransportProtocolActionLabel
    TransportProtocolPrecomputation;
```
<!-- --8<-- [end:TransportProtocolEngine] -->

#### Example of a transport engine

<!-- --8<-- [start:TransportProtocolEngine] -->
```juvix
exampleTransportProtocolEngine : TransportProtocolEngine := mkEngine@{
  name := "transport-protocol-quic";
  behaviour := transportBehaviour;
  initEnv := transportEnvironmentExample;
};
```
<!-- --8<-- [end:TransportProtocolEngine] -->

where `transportprotocolEnvironmentExample` is defined as follows:

--8 TODO <-- "./transport_protocol_environment.juvix.md:environment-example"
