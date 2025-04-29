---
icon: octicons/container-24
search:
  exclude: false
tags:
  - tutorial
  - example
---

??? code "Juvix imports"

    ```juvix
    module tutorial.engines.template_config;

    import tutorial.engines.template_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Template Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## Local Configuration

### `TemplateLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TemplateLocalCfg] -->
```juvix
type TemplateLocalCfg :=
  mk@{
    example : Nat;
    value : String;
  };
```
<!-- --8<-- [end:TemplateLocalCfg] -->

## Engine Configuration

### `TemplateCfg`

<!-- --8<-- [start:TemplateCfg] -->
```juvix
TemplateCfg : Type :=
  EngineCfg
    TemplateLocalCfg;
```
<!-- --8<-- [end:TemplateCfg] -->

## Instantiation

<!-- --8<-- [start:exTemplateCfg] -->
```juvix extract-module-statements
module template_config_example;

  exTemplateCfg : TemplateCfg :=
    EngineCfg.mk@{
      node := PublicKey.Curve25519PubKey "0xabcd1234";
      name := "template";
      cfg := TemplateLocalCfg.mk@{
        example := 1;
        value := "hello world";
      };
    };
end;
```
<!-- --8<-- [end:exTemplateCfg] -->
