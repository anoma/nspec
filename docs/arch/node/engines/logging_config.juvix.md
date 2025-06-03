---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - hardware-subsystem
  - engine
  - logging
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.logging_config;

    import prelude open;
    import arch.node.engines.logging_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Logging Configuration

## Overview

The logging engine configuration contains static information for logging engine instances.

## The Logging Local Configuration

### `LoggingLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:LoggingLocalCfg] -->
```juvix
type LoggingLocalCfg := mk;
```
<!-- --8<-- [end:LoggingLocalCfg] -->

## The Logging Configuration

### `LoggingCfg`

<!-- --8<-- [start:LoggingCfg] -->
```juvix
LoggingCfg : Type :=
  EngineCfg
    LoggingLocalCfg;
```
<!-- --8<-- [end:LoggingCfg] -->

#### Instantiation

<!-- --8<-- [start:loggingCfg] -->
```juvix extract-module-statements
module logging_config_example;

  loggingCfg : LoggingCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "logging";
      cfg := LoggingLocalCfg.mk;
    }
  ;
end;
```
<!-- --8<-- [end:loggingCfg] -->
