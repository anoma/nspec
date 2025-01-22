---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- transport-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.transport_config;

    import arch.node.engines.transport_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Transport Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Transport Local Configuration

### `TransportLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TransportLocalCfg] -->
```juvix
type TransportLocalCfg :=
  mkTransportLocalCfg;
```
<!-- --8<-- [end:TransportLocalCfg] -->

## The Transport Configuration

### `TransportCfg`

<!-- --8<-- [start:TransportCfg] -->
```juvix
TransportCfg : Type :=
  EngineCfg
    TransportLocalCfg;
```
<!-- --8<-- [end:TransportCfg] -->

## Instantiation

<!-- --8<-- [start:transportCfg] -->
```juvix extract-module-statements
module transport_config_example;

  transportCfg : TransportCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "transport";
      cfg := mkTransportLocalCfg;
    }
  ;
end;
```
<!-- --8<-- [end:transportCfg] -->
