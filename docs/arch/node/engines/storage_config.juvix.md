---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - network-subsystem
  - engine
  - storage
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.storage_config;

    import arch.node.engines.storage_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Storage Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## Local Configuration

### `StorageLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:StorageLocalCfg] -->
```juvix
type StorageLocalCfg :=
  mk;
```
<!-- --8<-- [end:StorageLocalCfg] -->

## Engine Configuration

### `StorageCfg`

<!-- --8<-- [start:StorageCfg] -->
```juvix
StorageCfg : Type :=
  EngineCfg
    StorageLocalCfg;
```
<!-- --8<-- [end:StorageCfg] -->

## Instantiation

<!-- --8<-- [start:exStorageCfg] -->
```juvix extract-module-statements
module storage_config_example;

exStorageCfg : StorageCfg :=
  EngineCfg.mk@{
    node := PublicKey.Curve25519PubKey "0xabcd1234";
    name := "storage";
    cfg := StorageLocalCfg.mk;
  };

end;
```
<!-- --8<-- [end:exStorageCfg] -->
