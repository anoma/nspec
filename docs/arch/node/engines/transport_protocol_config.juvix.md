---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - transport
  - configuration
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.transport_protocol_config;

    import arch.node.types.basics open;
    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Transport Protocol Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## The Transport Protocol Local Configuration

### `TransportProtocolLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TransportProtocolLocalCfg] -->
```juvix
type TransportProtocolLocalCfg :=
  mkTransportProtocolLocalCfg;
```
<!-- --8<-- [end:TransportProtocolLocalCfg] -->

## The Transport Protocol Configuration

### `TransportProtocolCfg`

<!-- --8<-- [start:TransportProtocolCfg] -->
```juvix
TransportProtocolCfg : Type :=
  EngineCfg
    TransportProtocolLocalCfg;
```
<!-- --8<-- [end:TransportProtocolCfg] -->

## Instantiation

<!-- --8<-- [start:exTransportProtocolCfg] -->
```juvix extract-module-statements
module transport_protocol_config_example;

exTransportProtocolCfg : TransportProtocolCfg :=
  mkEngineCfg@{
    node := Curve25519PubKey "0xabcd1234";
    name := "transport-protocol";
    cfg := mkTransportProtocolLocalCfg;
  };

end;
```
<!-- --8<-- [end:exTransportProtocolCfg] -->
