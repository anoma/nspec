---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- wall-clock-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.wall_clock_environment;

    import prelude open;
    import arch.node.engines.wall_clock_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    import arch.node.types.anoma_message as Anoma open;
    ```

# Wall Clock Environment

## Overview

The Local Wall Clock Engine provides and keeps track of a local
time.

## Mailbox states

The wall clock engine does not require complex mailbox states. We define the mailbox state as `Unit`.

```juvix
syntax alias WallClockMailboxState := Unit;
```

## Local state

```juvix
type WallClockLocalState := mkWallClockLocalState@{
  currentTime : EpochTimestamp
};
```

???+ quote "Arguments"

    `currentTime`
    : The current epoch time value

## Timer Handle

The wall clock engine does not require a timer handle type.
Therefore, we define the timer handle type as `Unit`.

```juvix
syntax alias WallClockTimerHandle := Unit;
```

## The Wall Clock Environment

### Auxiliary abstraction Functions

```juvix
axiom advanceTime : EpochTimestamp -> EpochTimestamp;
```

### `WallClockEnv`

<!-- --8<-- [start:WallClockEnv] -->
```juvix
WallClockEnv : Type :=
  EngineEnv
    WallClockLocalState
    WallClockMailboxState
    WallClockTimerHandle
    Anoma.Msg;
```
<!-- --8<-- [end:WallClockEnv] -->

#### Instantiation

<!-- --8<-- [start:wallClockEnv] -->
```juvix extract-module-statements
module wall_clock_environment_example;

  wallClockEnv : WallClockEnv :=
    mkEngineEnv@{
      localState := mkWallClockLocalState@{
        currentTime := 0
      };
      mailboxCluster := Map.empty;
      acquaintances := Set.empty;
      timers := []
    }
  ;
end;
```
<!-- --8<-- [end:wallClockEnv] -->
