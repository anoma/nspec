---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - ordering-subsystem
  - engine
  - executor
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.executor_environment;
    import prelude open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.engine_environment open;
    import arch.node.engines.executor_messages open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Executor Environment

---

## Overview

The executor environment maintains state needed during transaction execution including completed reads/writes and program state.

??? quote "Auxiliary Juvix code"

    ```juvix
    trait
    type Runnable KVSKey KVSDatum Executable ProgramState :=
      mkRunnable@{
        executeStep : Executable -> ProgramState -> Pair KVSKey KVSDatum -> Result String (Pair ProgramState (List (Either KVSKey (Pair KVSKey KVSDatum))));
        halted : ProgramState -> Bool;
        startingState : ProgramState;
      };
    ```

    `executeStep`:
    : Takes the executable code, current program state, and read key-value pair and returns either:
      - Error string on failure
      - New program state and list of either:
        - Left key for read requests
        - Right (key, value) for write requests

## Mailbox states

The executor engine does not require complex mailbox states.

### `ExecutorMailboxState`

```juvix
syntax alias ExecutorMailboxState := Unit;
```

## Local state

### `ExecutorLocalState`

```juvix
type ExecutorLocalState KVSKey KVSDatum ProgramState :=
  mkExecutorLocalState@{
    program_state : ProgramState;
    completed_reads : Map KVSKey KVSDatum;
    completed_writes : Map KVSKey KVSDatum
  };
```

???+ quote "Arguments"

    `program_state`
    : Current state of the executing program

    `completed_reads`
    : Map of keys to values that have been successfully read

    `completed_writes`
    : Map of keys to values that have been successfully written

## Timer Handle

The executor engine does not require timer handles.

### `ExecutorTimerHandle`

```juvix
syntax alias ExecutorTimerHandle := Unit;
```

## The Executor Environment

### `ExecutorEnv`

```juvix
ExecutorEnv (KVSKey KVSDatum ProgramState : Type) : Type :=
  EngineEnv
    (ExecutorLocalState KVSKey KVSDatum ProgramState)
    ExecutorMailboxState
    ExecutorTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:executorEnv] -->
```juvix extract-module-statements
module executor_environment_example;

executorEnv {KVSKey KVSDatum} : ExecutorEnv KVSKey KVSDatum String :=
  mkEngineEnv@{
    localState := mkExecutorLocalState@{
      program_state := "";
      completed_reads := Map.empty;
      completed_writes := Map.empty
    };
    mailboxCluster := Map.empty;
    acquaintances := Set.empty;
    timers := []
  };
end;
```
<!-- --8<-- [end:executorEnv] -->
