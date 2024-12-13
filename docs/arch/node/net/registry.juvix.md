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
    module arch.node.net.registry;

    import arch.node.net.registry_messages open public;
    import arch.node.net.registry_config open public;
    import arch.node.net.registry_environment open public;
    import arch.node.net.registry_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open registry_config_example;
    open registry_environment_example;
    open registry_behaviour_example;
    ```

# Network Registry Engine

## Purpose

The *Network Registry* engine
maintains a database of `NodeAdvert` and `TopicAdvert` messages
that arrive from the network,
and for each of these it spawns a [[Router Engine]]
or [[Pub/Sub Topic Engine]] instance, respectively.

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

--8<-- "./registry_config.juvix.md:exNetworkRegistryCfg"

`exNetworkRegistryEnv` is defined as follows:

--8<-- "./registry_environment.juvix.md:exNetworkRegistryEnv"

and `exNetworkRegistryBehaviour` is defined as follows:

--8<-- "./registry_behaviour.juvix.md:exNetworkRegistryBehaviour"
