---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- shard-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.shard_config;

    import prelude open;
    import arch.node.engines.shard_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Shard Configuration

## Overview

The shard configuration contains static information for shard engine instances.

## The Shard Configuration

### `ShardCfg`

<!-- --8<-- [start:ShardCfg] -->
```juvix
type ShardCfg := mkShardCfg;
```
<!-- --8<-- [end:ShardCfg] -->

## Instantiation

<!-- --8<-- [start:shardCfg] -->
```juvix extract-module-statements
module shard_config_example;

  shardCfg : EngineCfg ShardCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "shard";
      cfg := mkShardCfg;
    }
  ;
end;
```
<!-- --8<-- [end:shardCfg] -->
