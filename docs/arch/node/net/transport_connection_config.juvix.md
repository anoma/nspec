---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-connection-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.net.transport_connection_config;

    import arch.node.net.transport_connection_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Transport Connection Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Transport Connection Local Configuration

### `TransportConnectionLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TransportConnectionLocalCfg] -->
```juvix
type TransportConnectionLocalCfg :=
  mkTransportConnectionLocalCfg;
```
<!-- --8<-- [end:TransportConnectionLocalCfg] -->

## The Transport Connection Configuration

### `TransportConnectionCfg`

<!-- --8<-- [start:TransportConnectionCfg] -->
```juvix
TransportConnectionCfg : Type :=
  EngineCfg
    TransportConnectionLocalCfg;
```
<!-- --8<-- [end:TransportConnectionCfg] -->

## Instantiation

<!-- --8<-- [start:exTransportConnectionCfg] -->
```juvix extract-module-statements
module transport_connection_config_example;

exTransportConnectionCfg : TransportConnectionCfg :=
  mkEngineCfg@{
    node := Curve25519PubKey "0xabcd1234";
    name := "transport-connection";
    cfg := mkTransportConnectionLocalCfg;
  };

end;
```
<!-- --8<-- [end:exTransportConnectionCfg] -->
