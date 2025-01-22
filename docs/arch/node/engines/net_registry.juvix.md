---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- registry-engine
- engine-definition
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.net_registry;

    import arch.node.engines.net_registry_messages open public;
    import arch.node.engines.net_registry_config open public;
    import arch.node.engines.net_registry_environment open public;
    import arch.node.engines.net_registry_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open registry_config_example;
    open registry_environment_example;
    open registry_behaviour_example;
    ```

# Network Registry Engine

## Purpose

<!-- --8<-- [start:purpose] -->
The single *Network Registry* engine instance
maintains a database of `NodeAdvert` and `TopicAdvert` messages
that arrive from the network on each node.
For each known node and topic it spawns a [[Router Engine]]
or a [[Pub/Sub Topic Engine]] instance, respectively.
<!-- --8<-- [end:purpose] -->

## Components

- [[Network Registry Messages]]
- [[Network Registry Configuration]]
- [[Network Registry Environment]]
- [[Network Registry Behaviour]]

## Type

<!-- --8<-- [start:NetworkRegistryEngine] -->
```juvix
NetworkRegistryEngine : Type :=
  Engine
    NetworkRegistryLocalCfg
    NetworkRegistryLocalState
    NetworkRegistryMailboxState
    NetworkRegistryTimerHandle
    NetworkRegistryActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:NetworkRegistryEngine] -->

### Instantiation

<!-- --8<-- [start:exNetworkRegistryEngine] -->
```juvix
exNetworkRegistryEngine : NetworkRegistryEngine :=
  mkEngine@{
    cfg := exNetworkRegistryCfg;
    env := exNetworkRegistryEnv;
    behaviour := exNetworkRegistryBehaviour;
  };
```
<!-- --8<-- [end:exNetworkRegistryEngine] -->

Where `exNetworkRegistryCfg` is defined as follows:

--8<-- "./net_registry_config.juvix.md:exNetworkRegistryCfg"

`exNetworkRegistryEnv` is defined as follows:

--8<-- "./net_registry_environment.juvix.md:exNetworkRegistryEnv"

and `exNetworkRegistryBehaviour` is defined as follows:

--8<-- "./net_registry_behaviour.juvix.md:exNetworkRegistryBehaviour"
