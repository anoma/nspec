---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- router-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.router_config;

    import arch.node.net.router_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Router Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Router Local Configuration

### `RouterLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:RouterLocalCfg] -->
```juvix
type RouterLocalCfg :=
  mkRouterLocalCfg;
```
<!-- --8<-- [end:RouterLocalCfg] -->

## The Router Configuration

### `RouterCfg`

<!-- --8<-- [start:RouterCfg] -->
```juvix
RouterCfg : Type :=
  EngineCfg
    RouterLocalCfg;
```
<!-- --8<-- [end:RouterCfg] -->

## Instantiation

<!-- --8<-- [start:exRouterCfg] -->
```juvix extract-module-statements
module router_config_example;

exRouterCfg : RouterCfg :=
  mkEngineCfg@{
    node := Curve25519PubKey "0xabcd1234";
    name := "router";
    cfg := mkRouterLocalCfg;
  };

end;
```
<!-- --8<-- [end:exRouterCfg] -->
