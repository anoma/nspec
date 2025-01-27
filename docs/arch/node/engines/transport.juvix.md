---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.transport;

    import arch.node.engines.transport_messages open;
    import arch.node.engines.transport_config open;
    import arch.node.engines.transport_environment open;
    import arch.node.engines.transport_behaviour open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open transport_config_example;
    open transport_environment_example;
    ```

# Transport Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The *Transport* engine is responsible for establishing and accepting transport connections
via one of the *Transport Protocol* engines,
each of which responsible for a specific transport protocol, such as QUIC or TLS.
<!-- --8<-- [end:purpose] -->

## Engine components

- [[Transport Messages]]
- [[Transport Config]]
- [[Transport Environment]]
- [[Transport Behaviour]]

## Type

<!-- --8<-- [start:TransportEngine] -->
```juvix
TransportEngine : Type :=
  Engine
    TransportLocalCfg
    TransportLocalState
    TransportMailboxState
    TransportTimerHandle
    TransportActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TransportEngine] -->

### Instantiation

<!-- --8<-- [start:transportEngine] -->
```juvix
transportEngine : TransportEngine :=
  mkEngine@{
    cfg := transportCfg;
    env := transportEnv;
    behaviour := transportBehaviour;
  };
```
<!-- --8<-- [end:transportEngine] -->

Where `transportCfg` is defined as follows:

--8<-- "./transport_config.juvix.md:transportCfg"

`transportEnv` is defined as follows:

--8<-- "./transport_environment.juvix.md:transportEnv"

and `transportBehaviour` is defined as follows:

--8<-- "./transport_behaviour.juvix.md:transportBehaviour"
