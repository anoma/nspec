---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - signsfor
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for_config;

    import prelude open;
    import arch.node.engines.signs_for_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# SignsFor Configuration

## Overview

The SignsFor engine configuration contains static information for SignsFor engine instances.

## The SignsFor Local Configuration

### `SignsForLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:SignsForLocalCfg] -->
```juvix
type SignsForLocalCfg := mkSignsForLocalCfg;
```
<!-- --8<-- [end:SignsForLocalCfg] -->

## The SignsFor Configuration

### `SignsForCfg`

<!-- --8<-- [start:SignsForCfg] -->
```juvix
SignsForCfg : Type :=
  EngineCfg
    SignsForLocalCfg;
```
<!-- --8<-- [end:SignsForCfg] -->

#### Instantiation

<!-- --8<-- [start:signsForCfg] -->
```juvix extract-module-statements
module signs_for_config_example;

  signsForCfg : SignsForCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "signs for";
      cfg := mkSignsForLocalCfg;
    }
  ;
end;
```
<!-- --8<-- [end:signsForCfg] -->
