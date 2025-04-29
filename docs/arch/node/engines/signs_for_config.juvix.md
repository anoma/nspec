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

## The SignsFor Configuration

### `SignsForCfg`

<!-- --8<-- [start:SignsForCfg] -->
```juvix
type SignsForCfg := mk;
```
<!-- --8<-- [end:SignsForCfg] -->

#### Instantiation

<!-- --8<-- [start:signsForCfg] -->
```juvix extract-module-statements
module signs_for_config_example;

  signsForCfg : EngineCfg SignsForCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "signs for";
      cfg := SignsForCfg.mk
    }
  ;
end;
```
<!-- --8<-- [end:signsForCfg] -->
