---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- registry-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.registry_config;

    import arch.node.net.registry_messages open;

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
  mkNetworkRegistryLocalCfg;
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
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "net-registry";
      cfg := mkNetworkRegistryLocalCfg;
    };
end;
```
<!-- --8<-- [end:exNetworkRegistryCfg] -->
