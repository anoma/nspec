---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - readsfor
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.reads_for_config;

    import prelude open;
    import arch.node.engines.reads_for_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# ReadFor Configuration

## Overview

The ReadFor engine configuration contains static information for ReadFor engine instances.

## The ReadFor Local Configuration

### `ReadsForLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:ReadsForLocalCfg] -->
```juvix
type ReadsForLocalCfg := mk;
```
<!-- --8<-- [end:ReadsForLocalCfg] -->

## The ReadFor Configuration

### `ReadsForCfg`

<!-- --8<-- [start:ReadsForCfg] -->
```juvix
ReadsForCfg : Type :=
  EngineCfg
    ReadsForLocalCfg;
```
<!-- --8<-- [end:ReadsForCfg] -->

#### Instantiation

<!-- --8<-- [start:readsForCfg] -->
```juvix extract-module-statements
module reads_for_config_example;

  readsForCfg : ReadsForCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "reads for";
      cfg := ReadsForLocalCfg.mk
    }
  ;
end;
```
<!-- --8<-- [end:readsForCfg] -->
