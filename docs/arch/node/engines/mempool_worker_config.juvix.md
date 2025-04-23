---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - ordering-subsystem
  - engine
  - mempool-worker
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.mempool_worker_config;

    import prelude open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Mempool Worker Configuration

## Overview

The Mempool Worker engine configuration contains static information for Mempool Worker engine instances.

## The Mempool Worker Configuration

### `MempoolWorkerCfg`

<!-- --8<-- [start:MempoolWorkerCfg] -->
```juvix
type MempoolWorkerCfg := mk
```
<!-- --8<-- [end:MempoolWorkerCfg] -->

#### Instantiation

<!-- --8<-- [start:mempoolWorkerCfg] -->
```juvix extract-module-statements
module mempool_worker_config_example;

  mempoolWorkerCfg : EngineCfg MempoolWorkerCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "mempool worker";
      cfg := MempoolWorkerCfg.mk
    }
  ;
end;
```
<!-- --8<-- [end:mempoolWorkerCfg] -->
