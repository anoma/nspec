---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - registry
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.net_registry_config;

    import arch.node.engines.net_registry_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Network Registry Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## Local Configuration

### `NetworkRegistryLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:NetworkRegistryLocalCfg] -->
```juvix
type NetworkRegistryLocalCfg :=
  mk;
```
<!-- --8<-- [end:NetworkRegistryLocalCfg] -->

## Engine Configuration

### `NetworkRegistryCfg`

<!-- --8<-- [start:NetworkRegistryCfg] -->
```juvix
NetworkRegistryCfg : Type :=
  EngineCfg
    NetworkRegistryLocalCfg;
```
<!-- --8<-- [end:NetworkRegistryCfg] -->

## Instantiation

<!-- --8<-- [start:exNetworkRegistryCfg] -->
```juvix extract-module-statements
module registry_config_example;

  exNetworkRegistryCfg : NetworkRegistryCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "net-registry";
      cfg := NetworkRegistryLocalCfg.mk;
    };
end;
```
<!-- --8<-- [end:exNetworkRegistryCfg] -->
