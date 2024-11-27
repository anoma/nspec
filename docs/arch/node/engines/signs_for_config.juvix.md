---
icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- signs-for-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.signs_for_config;

    import prelude open;
    import arch.node.engines.signs_for_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Signs For Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Signs For Configuration

### `SignsForCfg`

<!-- --8<-- [start:SignsForCfg] -->
```juvix
type SignsForCfg :=
  mkSignsForCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:SignsForCfg] -->

#### Instantiation

<!-- --8<-- [start:signsForCfg] -->
```juvix extract-module-statements
module signs_for_config_example;

  signsForCfg : EngineCfg SignsForCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "signs for";
      cfg := mkSignsForCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:signsForCfg] -->
