---
icon: octicons/container-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - naming
  - configuration
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.naming_config;

    import prelude open;
    import arch.node.engines.naming_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Naming Configuration

## Overview

The Naming engine configuration contains static information for Naming engine instances.

## The Naming Configuration

### `NamingCfg`

<!-- --8<-- [start:NamingCfg] -->
```juvix
type NamingCfg := mk
```
<!-- --8<-- [end:NamingCfg] -->

#### Instantiation

<!-- --8<-- [start:namingCfg] -->
```juvix extract-module-statements
module naming_config_example;

  namingCfg : EngineCfg NamingCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "naming";
      cfg := NamingCfg.mk
    }
  ;
end;
```
<!-- --8<-- [end:namingCfg] -->
