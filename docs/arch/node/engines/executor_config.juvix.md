---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - ordering-subsystem
  - engine
  - executor
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.executor_config;

    import prelude open;
    import arch.node.engines.executor_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.system.state.resource_machine.notes.nockma open;
    ```

# Executor Configuration

## Overview

The executor configuration contains static information needed for execution: the transaction program, access rights, and notification targets.

## The Executor Local Configuration

### `ExecutorLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:ExecutorLocalCfg] -->
```juvix
type ExecutorLocalCfg :=
  mk@{
    timestamp : TxFingerprint;
    executable : Executable;
    lazy_read_keys : Set KVSKey;
    eager_read_keys : Set KVSKey;
    will_write_keys : Set KVSKey;
    may_write_keys : Set KVSKey;
    worker : EngineID;
    issuer : EngineID;
    keyToShard : KVSKey -> EngineID
  }
```
<!-- --8<-- [end:ExecutorLocalCfg] -->

???+ code "Arguments"

    `timestamp`
    : The logical timestamp representing when this transaction executes in the
    ordering

    `executable`
    : The transaction's executable code

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
    : ID of the transaction sender to notify on completion

## The Executor Configuration

### `ExecutorCfg`

<!-- --8<-- [start:ExecutorCfg] -->
```juvix
ExecutorCfg : Type :=
  EngineCfg
    ExecutorLocalCfg;
```
<!-- --8<-- [end:ExecutorCfg] -->

#### Instantiation

<!-- --8<-- [start:executorCfg] -->
```juvix extract-module-statements
module executor_config_example;

  executorCfg : ExecutorCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "executor";
      cfg := ExecutorLocalCfg.mk@{
        timestamp := 0;
        executable := Noun.Atom 0;
        lazy_read_keys := Set.Set.empty;
        eager_read_keys := Set.Set.empty;
        will_write_keys := Set.Set.empty;
        may_write_keys := Set.Set.empty;
        worker := mkPair none "";
        issuer := mkPair none "";
        keyToShard := \{_ := mkPair none "shard"}
      };
    }
  ;
end;
```
<!-- --8<-- [end:executorCfg] -->
