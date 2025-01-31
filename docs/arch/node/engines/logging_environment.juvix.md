---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - logging
  - environment
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.logging_environment;

    import prelude open;
    import arch.node.engines.logging_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Logging Environment

## Overview

The logging environment maintains the state necessary for recording logs locally
on the physical machine.

## Mailbox state types

### `LoggingMailboxState`

```juvix
syntax alias LoggingMailboxState := Unit;
```

The logging engine does not require complex mailbox states.

## Local state

### `LoggingLocalState`

<!-- --8<-- [start:LoggingLocalState] -->
```juvix
type LoggingLocalState :=
  mkLoggingLocalState@{
    logbook : List String
  };
```
<!-- --8<-- [end:LoggingLocalState] -->

???+ quote "Arguments"

    `logbook`
    : List of log entries stored as strings.

## Timer handles

### `LoggingTimerHandle`

<!-- --8<-- [start:LoggingTimerHandle] -->
```juvix
syntax alias LoggingTimerHandle := Unit;
```
<!-- --8<-- [end:LoggingTimerHandle] -->

### `LoggingTimestampedTrigger`

<!-- --8<-- [start:LoggingTimestampedTrigger] -->
```juvix
LoggingTimestampedTrigger : Type :=
  TimestampedTrigger
    LoggingTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LoggingTimestampedTrigger] -->

## The Logging Environment

### `LoggingEnv`

<!-- --8<-- [start:LoggingEnv] -->
```juvix
LoggingEnv : Type :=
  EngineEnv
    LoggingLocalState
    LoggingMailboxState
    LoggingTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:LoggingEnv] -->

#### Instantiation

<!-- --8<-- [start:loggingEnv] -->
```juvix extract-module-statements
module logging_environment_example;

  loggingEnv : LoggingEnv :=
    mkEngineEnv@{
      localState := mkLoggingLocalState@{
        logbook := []
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:loggingEnv] -->
