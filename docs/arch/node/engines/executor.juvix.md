---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- executor-engine
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.executor;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.executor_config open public;
    import arch.node.engines.executor_messages open public;
    import arch.node.engines.executor_environment open public;
    import arch.node.engines.executor_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open executor_config_example;
    open executor_environment_example;
    ```

# Executor Engine

The Executor Engine is responsible for executing transaction programs in Anoma,
serving as the computational core that processes state transitions within the
system. It operates as part of a distributed execution system, working in concert
with [[Shard Engine]]s that manage state access and [[Mempool Worker]] engines that
take orders and spawn Executor engines based on those orders. Each Executor Engine
instance is spawned to handle the execution of a single transaction in the form of
a program which it is spawned with, making them ephemeral components that exist
solely for the duration of their assigned transaction's lifecycle.

At its core, an Executor Engine receives read responses from shards and uses these
to step through the transaction program's execution. Each transaction program
defines a sequence of operations that may read from or write to various keys in
the system's state. The Executor doesn't directly access this state - instead, it
coordinates with Shard engines that manage actual state access.

The primary interface for the Executor Engine consists of three main message types
that facilitate its operation. It receives `ShardMsgKVSRead` messages from Shards
containing the data for requested state reads. For each read, the Executor applies
this data to advance the transaction program's execution, potentially generating
new read requests (`ShardMsgKVSReadRequest`) or write operations (`ShardMsgKVSWrite`)
that are sent to the appropriate Shards. Once execution is complete, it sends
an `ExecutorMsgExecutorFinished` message to both the Worker that spawned it and the
transaction's issuer, containing a summary of all reads and writes performed during
execution.

## Components

- [[Executor Messages]]
- [[Executor Config]]
- [[Executor Environment]]
- [[Executor Behaviour]]

## The type for an executor engine

<!-- --8<-- [start:ExecutorEngine] -->
```juvix
ExecutorEngine : Type :=
  Engine
    ExecutorCfg
    ExecutorLocalState
    ExecutorMailboxState
    ExecutorTimerHandle
    ExecutorActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:ExecutorEngine] -->

### Example of an executor engine

<!-- --8<-- [start:exampleExecutorEngine] -->
```juvix
exampleExecutorEngine : ExecutorEngine :=
  mkEngine@{
    cfg := executorCfg;
    env := executorEnv;
    behaviour := executorBehaviour;
  };
```
<!-- --8<-- [end:exampleExecutorEngine] -->

where [[Executor Configuration#executorCfg|`executorCfg`]] is defined as follows:

--8<-- "./docs/arch/node/engines/executor_config.juvix.md:executorCfg"

[[Executor Environment#executorEnv|`executorEnv`]] is defined as follows:

--8<-- "./docs/arch/node/engines/executor_environment.juvix.md:executorEnv"

and [[Executor Behaviour#executorBehaviour|`executorBehaviour`]] is defined as follows:

--8<-- "./docs/arch/node/engines/executor_behaviour.juvix.md:executorBehaviour"
