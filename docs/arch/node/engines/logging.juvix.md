---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - logging
  - engine-definition
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.logging;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.logging_messages open public;
    import arch.node.engines.logging_environment open public;
    import arch.node.engines.logging_behaviour open public;
    import arch.node.engines.logging_config open public;

    import arch.node.types.anoma as Anoma open;

    open logging_config_example;
    open logging_environment_example;
    ```

# Logging Engine

## Purpose

The Logging Engine provides capabilities for recording, monitoring,
analyzing, and managing events and activities locally on the physical
machine that the Anoma node is running. It supports diagnostic efforts,
security monitoring, performance optimization, and historical analysis
to ensure stability, security, and efficiency.

## Engine components

- [[Logging Messages]]
- [[Logging Configuration]]
- [[Logging Environment]]
- [[Logging Behaviour]]

## Type

<!-- --8<-- [start:LoggingEngine] -->
```juvix
LoggingEngine : Type :=
  Engine
    LoggingLocalCfg
    LoggingLocalState
    LoggingMailboxState
    LoggingTimerHandle
    LoggingActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:LoggingEngine] -->

### Example of a logging engine

<!-- --8<-- [start:exampleLoggingEngine] -->
```juvix
exampleLoggingEngine : LoggingEngine :=
  mkEngine@{
    cfg := loggingCfg;
    env := loggingEnv;
    behaviour := loggingBehaviour;
  };
```
<!-- --8<-- [end:exampleLoggingEngine] -->

where `loggingCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/logging_config.juvix.md:loggingCfg"

`loggingEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/logging_environment.juvix.md:loggingEnv"

and `loggingBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/logging_behaviour.juvix.md:loggingBehaviour"