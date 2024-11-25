icon: octicons/container-24
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-environment
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.template_config;

    import prelude open;
    import arch.node.engines.template_messages open;
    import arch.node.types.engine open;
    import arch.node.types.messages open;
    import arch.node.types.identities open;
    ```

# Template Configuration

## Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## The Template Configuration

### `TemplateCfg`

<!-- --8<-- [start:TemplateCfg] -->
```juvix
type TemplateCfg :=
  mkTemplateCfg@{
    example : Nat;
    value : String;
  }
```
<!-- --8<-- [end:TemplateCfg] -->

#### Instantiation

<!-- --8<-- [start:templateCfg] -->
```juvix extract-module-statements
module template_environment_example;

  templateCfg : EngineCfg TemplateCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "template";
      cfg := mkTemplateCfg@{
        example := 1;
        value := "hello world";
      };
    }
  ;
end;
```
<!-- --8<-- [end:templateCfg] -->
