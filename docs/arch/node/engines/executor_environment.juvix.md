---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine-behaviour
tags:
- mempool
- mempool-worker
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.executor_environment;
    import prelude open;
    import arch.node.engines.executor_messages open;
    import arch.node.types.engine_environment open;
    ```

# Executor Environment

## Overview
The local state each executor tracks the ``in progress'' transaction candidates post-ordering execution, along with read and write requests from the shards.


## Mailbox states
!!! todo
    Figure out what a mailbox state is, what makes it special, and if we're just using Unit.

The Executor Engine does not require complex mailbox states.
We define the mailbox state as `Unit`.

### `ExecutorMailboxState`

```juvix
syntax alias ExecutorMailboxState := Unit;
```

## Local state
Each executor  keeps track of:

### `ExecutorLocalState`
```juvix
type ExecutorLocalState := mkExecutorLocalState@{
  executable : Maybe ExecuteTransaction; -- if we've received it, the message that tells us what we're executing
  reads : Map KVSKey KVSDatum; -- reads from the label for which we've received results
  writes: Map KVSKey KVSDatum; -- writes issued by execution
  side_effects : IO (); -- other operations to be issued if the transaction ultimately succeeds.
};
```
!!! todo
    Include some kind of "current continuation", which is part of the state when we are waiting for optional reads to return.

!!! todo
    Include whatever is necessary to facilitate knowing which shards to look up for a read or write



???+ quote "Arguments"

    `executable`:
    : if we've received it, the message that tells us what we're executing

    `reads`:
    : reads from the label for which we've received results

    `writes`:
    : writes issued by execution

    `side_effects`:
    : other operations to be issued if the transaction ultimately succeeds. We may need to more tightly constrain what this can be (e.g. sending specific messages) than just "any IO."

## Timer Handle
!!! todo
    figure out what a Timer Handle is, and if an executor needs one.

The Executor Engine does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

### `ExecutorTimerHandle`

```juvix
syntax alias ExecutorTimerHandle := Unit;
```

## The Executor Environment

### `ExecutorEnvironment`

```juvix
ExecutorEnvironment : Type :=
  EngineEnvironment
    ExecutorLocalState
    ExecutorMailboxState
    ExecutorTimerHandle;
```

### Instantiation
!!! todo
    using the commitment engine template, create a (small) example executor

<!-- --8<-- [start:executorEnvironment] -->
```juvix extract-module-statements
module executor_environment_example;

executorEnvironment : executorEnvironment :=
    mkEngineEnvironment@{
      name := "mempool-worker";
      localState := mkExecutorLocalState@{
        executable : None,
        reads : emptyMap,
        writes: emptyMap,
        side_effects : noOp
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
!!! todo
    figure out how to make an emptyMap

!!! todo
    figure out how to make an IO noOp object

<!-- --8<-- [end:executorEnvironment] -->
