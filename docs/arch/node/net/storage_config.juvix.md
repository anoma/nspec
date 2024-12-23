---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- storage-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.net.storage_config;

    import arch.node.net.storage_messages open;

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
  mkStorageLocalCfg;
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
  mkEngineCfg@{
    node := Curve25519PubKey "0xabcd1234";
    name := "storage";
    cfg := mkStorageLocalCfg;
  };

end;
```
<!-- --8<-- [end:exStorageCfg] -->
