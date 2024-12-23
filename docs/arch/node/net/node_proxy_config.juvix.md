---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- node-proxy-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.node_proxy_config;

    import arch.node.net.node_proxy_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Node Proxy Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Node Proxy Local Configuration

### `NodeProxyLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:NodeProxyLocalCfg] -->
```juvix
type NodeProxyLocalCfg :=
  mkNodeProxyLocalCfg;
```
<!-- --8<-- [end:NodeProxyLocalCfg] -->

## The Node Proxy Configuration

### `NodeProxyCfg`

<!-- --8<-- [start:NodeProxyCfg] -->
```juvix
NodeProxyCfg : Type :=
  EngineCfg
    NodeProxyLocalCfg;
```
<!-- --8<-- [end:NodeProxyCfg] -->

## Instantiation

<!-- --8<-- [start:exNodeProxyCfg] -->
```juvix extract-module-statements
module node_proxy_config_example;

exNodeProxyCfg : NodeProxyCfg :=
  mkEngineCfg@{
    node := Curve25519PubKey "0xabcd1234";
    name := "node-proxy";
    cfg := mkNodeProxyLocalCfg;
  };

end;
```
<!-- --8<-- [end:exNodeProxyCfg] -->
