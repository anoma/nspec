---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- naming-engine
- engine-environment
---

??? note "Juvix imports"

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

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Naming Configuration

### `NamingCfg`

<!-- --8<-- [start:NamingCfg] -->
```juvix
type NamingCfg :=
  mkNamingCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:NamingCfg] -->

#### Instantiation

<!-- --8<-- [start:namingCfg] -->
```juvix extract-module-statements
module naming_config_example;

  namingCfg : EngineCfg NamingCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "naming";
      cfg := mkNamingCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:namingCfg] -->
