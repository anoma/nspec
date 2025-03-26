---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - wall-clock-engine
  - engine-definition
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.wall_clock;

    import prelude open;
    import arch.node.types.engine_environment open;
    import arch.node.types.engine_behaviour open;
    import arch.node.types.engine open;

    import arch.node.engines.wall_clock_config open public;
    import arch.node.engines.wall_clock_messages open public;
    import arch.node.engines.wall_clock_environment open public;
    import arch.node.engines.wall_clock_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open wall_clock_config_example;
    open wall_clock_environment_example;
    ```

# Wall Clock Engine

## Purpose

The Wall Clock Engine provides a mechanism for tracking and managing time locally on the physical machine that the Anoma node is running.
It abstracts away the details of the underlying hardware and provides an interface for getting real-time clock functionality.

## Engine components

- [[Wall Clock Messages]]
- [[Wall Clock Configuration]]
- [[Wall Clock Environment]]
- [[Wall Clock Behaviour]]

## Type

<!-- --8<-- [start:WallClockEngine] -->
```juvix
WallClockEngine : Type :=
  Engine
    WallClockLocalCfg
    WallClockLocalState
    WallClockMailboxState
    WallClockTimerHandle
    WallClockActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:WallClockEngine] -->

### Example of a wall clock engine

<!-- --8<-- [start:exampleWallClockEngine] -->
```juvix
exampleWallClockEngine : WallClockEngine :=
  mkEngine@{
    cfg := wallClockCfg;
    env := wallClockEnv;
    behaviour := wallClockBehaviour;
  };
```
<!-- --8<-- [end:exampleWallClockEngine] -->

where `wallClockCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/wall_clock_config.juvix.md:wallClockCfg"

`wallClockEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/wall_clock_environment.juvix.md:wallClockEnv"

and `wallClockBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/wall_clock_behaviour.juvix.md:wallClockBehaviour"
