---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - ordering-subsystem
  - engine
  - shard
  - configuration
---

??? code "Juvix imports"

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

## The Shard Local Configuration

### `ShardLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:ShardLocalCfg] -->
```juvix
type ShardLocalCfg := mkShardLocalCfg;
```
<!-- --8<-- [end:ShardLocalCfg] -->

## The Shard Configuration

### `ShardCfg`

<!-- --8<-- [start:ShardCfg] -->
```juvix
ShardCfg : Type :=
  EngineCfg
    ShardLocalCfg;
```
<!-- --8<-- [end:ShardCfg] -->

#### Instantiation

<!-- --8<-- [start:shardCfg] -->
```juvix extract-module-statements
module shard_config_example;

  shardCfg : ShardCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "shard";
      cfg := ShardCfg.mk;
    }
  ;
end;
```
<!-- --8<-- [end:shardCfg] -->
