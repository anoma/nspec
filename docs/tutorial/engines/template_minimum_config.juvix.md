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
    module tutorial.engines.template_minimum_config;

    import tutorial.engines.template_minimum_messages open;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.identities open;
    ```

# Template Minimum Configuration

## Overview

The [[Engine configuration|static configuration]] of the engine.

## Local Configuration

### `TemplateMinimumLocalCfg`

The type for engine-specific local configuration.

<!-- --8<-- [start:TemplateMinimumLocalCfg] -->
```juvix
type TemplateMinimumLocalCfg :=
  mkTemplateMinimumLocalCfg;
```
<!-- --8<-- [end:TemplateMinimumLocalCfg] -->

## Engine Configuration

### `TemplateMinimumCfg`

<!-- --8<-- [start:TemplateMinimumCfg] -->
```juvix
TemplateMinimumCfg : Type :=
  EngineCfg
    TemplateMinimumLocalCfg;
```
<!-- --8<-- [end:TemplateMinimumCfg] -->

## Instantiation

<!-- --8<-- [start:exTemplateMinimumCfg] -->
```juvix extract-module-statements
module template_minimum_config_example;

  exTemplateMinimumCfg : TemplateMinimumCfg :=
    mkEngineCfg@{
      node := Curve25519PubKey "0xabcd1234";
      name := "template-minimum";
      cfg := mkTemplateMinimumLocalCfg;
    };
end;
```
<!-- --8<-- [end:exTemplateMinimumCfg] -->
