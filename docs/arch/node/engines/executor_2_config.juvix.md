---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- executor-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.executor_config;

    import prelude open;
    import arch.node.engines.executor_2_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.engines.shard_2_messages open;
    ```

# Executor Configuration

## Overview

The executor configuration contains the transaction information and access lists for keys it intends to read and write.

## The Executor Configuration

### `ExecutorCfg`

<!-- --8<-- [start:ExecutorCfg] -->
```juvix
type ExecutorCfg :=
  mkExecutorCfg@{
    executable : TransactionExecutable;
    read_keys : Set KVSKey;
    write_keys : Set KVSKey;
    timestamp : TxFingerprint;
    curator : EngineID;
    issuer : EngineID
  }
```
<!-- --8<-- [end:ExecutorCfg] -->

???+ quote "Arguments"

    `executable`
    : The transaction code to be executed

    `read_keys`
    : Set of keys this transaction may read

    `write_keys`
    : Set of keys this transaction may write

    `timestamp`
    : Transaction's position in ordering

    `curator`
    : Worker engine to inform when execution completes

    `issuer`
    : Original sender of the transaction request

## Instantiation

<!-- --8<-- [start:executorCfg] -->
```juvix extract-module-statements
module executor_config_example;

  executorCfg : EngineCfg ExecutorCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "executor";
      cfg := mkExecutorCfg@{
        executable := "";
        read_keys := Set.empty;
        write_keys := Set.empty;
        timestamp := 0;
        curator := mkPair none "curator";
        issuer := mkPair none "issuer"
      };
    }
  ;
end;
```
<!-- --8<-- [end:executorCfg] -->
