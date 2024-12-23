---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- reads-for-engine
- engine-environment
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for_config;

    import prelude open;
    import arch.node.engines.reads_for_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Reads For Configuration

## Overview

The Reads For engine configuration contains static information for Reads For engine instances.

## The Reads For Configuration

### `ReadsForCfg`

<!-- --8<-- [start:ReadsForCfg] -->
```juvix
type ReadsForCfg := mkReadsForCfg
```
<!-- --8<-- [end:ReadsForCfg] -->

#### Instantiation

<!-- --8<-- [start:readsForCfg] -->
```juvix extract-module-statements
module reads_for_config_example;

  readsForCfg : EngineCfg ReadsForCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "reads for";
      cfg := mkReadsForCfg
    }
  ;
end;
```
<!-- --8<-- [end:readsForCfg] -->
