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
    import arch.node.engines.executor_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Executor Configuration

## Overview

The executor configuration contains static information needed for execution: the transaction program, access rights, and notification targets.

## The Executor Configuration

### `ExecutorCfg`

<!-- --8<-- [start:ExecutorCfg] -->
```juvix
type ExecutorCfg :=
  mkExecutorCfg@{
    timestamp : TxFingerprint;
    executable : Executable;
    lazy_read_keys : Set KVSKey;
    eager_read_keys : Set KVSKey;
    will_write_keys : Set KVSKey;
    may_write_keys : Set KVSKey;
    worker : EngineID;
    issuer : EngineID;
  }
```
<!-- --8<-- [end:ExecutorCfg] -->

???+ quote "Arguments"

    `timestamp`
    : The logical timestamp representing when this transaction executes in the ordering
    
    `executable`
    : The transaction executable code
    
    `lazy_read_keys`
    : Keys that may be read during execution

    `eager_read_keys`
    : Keys that will definitely be read
    
    `will_write_keys`
    : Keys that will definitely be written
    
    `may_write_keys`
    : Keys that might be written
    
    `worker`
    : ID of the worker engine to notify on completion
    
    `issuer`
    : ID of the transaction sender

## Instantiation

<!-- --8<-- [start:executorCfg] -->
```juvix extract-module-statements
module executor_config_example;

  executorCfg : EngineCfg ExecutorCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "executor";
      cfg := mkExecutorCfg@{
        timestamp := 0;
        executable := "";
        lazy_read_keys := Set.empty;
        eager_read_keys := Set.empty;
        will_write_keys := Set.empty;
        may_write_keys := Set.empty;
        worker := mkPair none "";
        issuer := mkPair none "";
      };
    }
  ;
end;
```
<!-- --8<-- [end:executorCfg] -->
