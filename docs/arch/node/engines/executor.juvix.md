---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- execution
- executor
- engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.executor;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.executor_messages open public;
    import arch.node.engines.executor_environment open public;
    import arch.node.engines.executor_behaviour open public;
    ```

# Executor


Conceptually, Executors  run the
 [executor function](./../ordering/execution/index.md#executor-function) in order to
 compute transaction outputs, including state updates
 (see [[Execution Engines|here]] for more on the executor function).
Executors may be co-located with [[Shard|shards]], or with
 [[Worker Engine|mempool workers]].
The [[Execution Engines]] might keep a pool of Executors,
 or spin a new one up with each [[TransactionCandidate]].
## Purpose

## Components

- [[Executor Messages]]
- [[Executor Environment]]
- [[Executor Behaviour]]

## Type
!!! todo
    Add an element to the executor Engine (perhaps in the behaviour?) that specifises the transaction candidate (and its label) that we're executing. 
    I think currently these are specified in `ExecuteTransaction` message, but they don't need to be a message.
<!-- --8<-- [start:ExecutorEngine] -->
```juvix
ExecutorEngine : Type := Engine
  ExecutorLocalState
  ExecutorMailboxState
  ExecutorTimerHandle
  ExecutorMatchableArgument
  ExecutorActionLabel
  ExecutorPrecomputation;
```
<!-- --8<-- [end:ExecutorEngine] -->

### Example of an execution engine

<!-- --8<-- [start:exampleExecutorEngine] -->
```juvix
exampleMempoolWorkerEngine : MempoolWorkerEngine := mkEngine@{
    name := "executor";
    initEnv := commitmentEnvironment;
    behaviour := executorBehaviour;
  };
```
<!-- --8<-- [end:exampleExecutorEngine] -->

where `executorEnvironment` is defined as follows:

--8<-- "./docs/arch/node/engines/executor_environment.juvix.md:executorEnvironment"

and `executorBehaviour` is defined as follows:

!!! todo
    Figure out what it means to define behaviour and put it here