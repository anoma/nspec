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

# Transport Engine

## Purpose

--8<-- [start:purpose]
The *Transport* engine is responsible for accepting and initiating transport connections
via one of the *Transport Protocol* engines,
each of which responsible for a specific transport protocol, such as QUIC or TLS.
--8<-- [end:purpose]

## Engine Components

- [[Transport Messages]]
- [[Transport Environment]]
- [[Transport Dynamics]]

## Useful links

## Types

### `TransportEngine`

<!-- --8<-- [start:TransportEngine] -->
```juvix
TransportEngine : Type :=
  Engine
    TransportLocalState
    TransportMailboxState
    TransportTimerHandle
    TransportMatchableArgument
    TransportActionLabel
    TransportPrecomputation;
```
<!-- --8<-- [end:TransportEngine] -->

#### Example of a transport engine

<!-- --8<-- [start:TransportEngine] -->
```juvix
exampleTransportEngine : TransportEngine := mkEngine@{
  name := "transport";
  behaviour := transportBehaviour;
  initEnv := transportEnvironmentExample;
};
```
<!-- --8<-- [end:TransportEngine] -->

where `transportEnvironmentExample` is defined as follows:

--8 TODO <-- "./transport_environment.juvix.md:environment-example"
