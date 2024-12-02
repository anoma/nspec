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
    module arch.node.engines.wall_clock_config;

    import prelude open;
    import arch.node.engines.wall_clock_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Wall Clock Configuration

## Overview

The wall clock engine configuration contains the static configuration needed for
the wall clock engine to function.

## The Wall Clock Configuration

### `WallClockCfg`

<!-- --8<-- [start:WallClockCfg] -->
```juvix
type WallClockCfg := mkWallClockCfg;
```
<!-- --8<-- [end:WallClockCfg] -->

#### Instantiation

<!-- --8<-- [start:wallClockCfg] -->
```juvix extract-module-statements
module wall_clock_config_example;

  wallClockCfg : EngineCfg WallClockCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "wall clock";
      cfg := mkWallClockCfg;
    }
  ;
end;
```
<!-- --8<-- [end:wallClockCfg] -->
