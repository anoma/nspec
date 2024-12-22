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

Conceptually, Executors  run the
 *executor function* in order to
 compute transaction outputs, including state updates
 (see [[Execution Engines|here]] for more on the executor function).
Executors may be co-located with [[Shard|shards]], or with
 [[Worker Engine|mempool workers]].
The [[Execution Engines]] might keep a pool of Executors,
 or spin a new one up with each [[TransactionCandidate]].

## Purpose

The Executor Engine maintains executor capabilities for a specific identity
and handles executor requests for that identity. Only the original caller and
anyone to whom they pass the engine instance reference can send messages to the
instance and decrypt data encrypted to the corresponding identity.

## Components

- [[Executor Messages]]
- [[Executor Config]]
- [[Executor Environment]]
- [[Executor Behaviour]]

## Type

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

### Example of a executor engine


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

where `executorCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/executor_config.juvix.md:executorCfg"

`executorEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/executor_environment.juvix.md:executorEnv"

and `executorBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/executor_behaviour.juvix.md:executorBehaviour"
