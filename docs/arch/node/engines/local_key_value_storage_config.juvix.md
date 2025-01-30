---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - hardware
  - engine
  - local-key-value-storage
  - configuration
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.local_key_value_storage_config;

    import prelude open;
    import arch.node.engines.local_key_value_storage_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Local Key Value Storage Configuration

## Overview

The Local Key Value Storage engine configuration contains static information for Local Key Value Storage engine instances.

## The Local Key Value Storage Configuration

### `LocalKVStorageCfg`

<!-- --8<-- [start:LocalKVStorageCfg] -->
```juvix
type LocalKVStorageCfg := mkLocalKVStorageCfg;
```
<!-- --8<-- [end:LocalKVStorageCfg] -->

#### Instantiation

<!-- --8<-- [start:localKVStorageCfg] -->
```juvix extract-module-statements
module local_key_value_storage_config_example;

  localKVStorageCfg : EngineCfg LocalKVStorageCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "key value storage";
      cfg := mkLocalKVStorageCfg;
    }
  ;
end;
```
<!-- --8<-- [end:localKVStorageCfg] -->
