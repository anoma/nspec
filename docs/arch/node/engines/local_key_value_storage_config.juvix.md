---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- local-key-value-storage-engine
- engine-environment
---

??? note "Juvix imports"

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

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Local Key Value Storage Configuration

### `LocalKVStorageCfg`

<!-- --8<-- [start:LocalKVStorageCfg] -->
```juvix
type LocalKVStorageCfg :=
  mkLocalKVStorageCfg@{
    example : Nat;
    value : String;
  }
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
      cfg := mkLocalKVStorageCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:localKVStorageCfg] -->
