---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- local-ts-storage-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.local_time_series_storage_config;

    import prelude open;
    import arch.node.engines.local_time_series_storage_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Local Time Series Storage Configuration

## Overview

The Local Time Series Storage engine configuration contains static information for Local Time Series Storage engine instances.

## The Local Time Series Storage Configuration

### `LocalTSStorageCfg`

<!-- --8<-- [start:LocalTSStorageCfg] -->
```juvix
type LocalTSStorageCfg := mkLocalTSStorageCfg;
```
<!-- --8<-- [end:LocalTSStorageCfg] -->

## Instantiation

<!-- --8<-- [start:localTSStorageCfg] -->
```juvix extract-module-statements
module local_ts_storage_config_example;

  localTSStorageCfg : EngineCfg LocalTSStorageCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "local time series storage";
      cfg := mkLocalTSStorageCfg;
    }
  ;
end;
```
<!-- --8<-- [end:localTSStorageCfg] -->