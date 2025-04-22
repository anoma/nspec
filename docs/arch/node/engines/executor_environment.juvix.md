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
    import arch.system.state.resource_machine.notes.nockma open;
    import arch.system.state.resource_machine.notes.runnable open;
    import arch.system.state.resource_machine.notes.nockma_runnable open;
    ```

# Executor Environment

## Overview

The executor environment maintains state needed during transaction execution including completed reads/writes and program state.

## Mailbox states

The executor engine does not require complex mailbox states.

### `ExecutorMailboxState`

```juvix
syntax alias ExecutorMailboxState := Unit;
```

## Local state

### `ExecutorLocalState`

```juvix
type ExecutorLocalState :=
  mk@{
    program_state : ProgramState;
    completed_reads : Map KVSKey KVSDatum;
    completed_writes : Map KVSKey KVSDatum
  };
```

???+ code "Arguments"

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
ExecutorEnv : Type :=
  EngineEnv
    ExecutorLocalState
    ExecutorMailboxState
    ExecutorTimerHandle
    Anoma.Msg;
```

### Instantiation

<!-- --8<-- [start:executorEnv] -->
```juvix extract-module-statements
module executor_environment_example;

executorEnv : ExecutorEnv :=
  EngineEnv.mk@{
    localState := ExecutorLocalState.mk@{
      program_state := NockmaProgramState.mk@{ 
          current_noun := Noun.Atom 0;
          storage := emptyStorage;
          gas_limit := 0 };
      completed_reads := Map.empty;
      completed_writes := Map.empty
    };
    mailboxCluster := Map.empty;
    acquaintances := Set.Set.empty;
    timers := []
  };
end;
```
<!-- --8<-- [end:executorEnv] -->
