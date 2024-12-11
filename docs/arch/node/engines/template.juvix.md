---
icon: octicons/gear-24
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-definition
---

??? note "Juvix imports"

    ```juvix
    module arch.node.engines.template;

    import arch.node.engines.template_messages open public;
    import arch.node.engines.template_config open public;
    import arch.node.engines.template_environment open public;
    import arch.node.engines.template_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open template_config_example;
    open template_environment_example;
    open template_behaviour_example;
    ```

# Template Engine

## Purpose

Brief summary of the purpose of the engine.

## Components

- [[Template Messages]]
- [[Template Configuration]]
- [[Template Environment]]
- [[Template Behaviour]]

## Useful links

- Some
- Useful
- Links

## Type

<!-- --8<-- [start:TemplateEngine] -->
```juvix
TemplateEngine : Type :=
  Engine
    TemplateLocalCfg
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TemplateEngine] -->

### Instantiation

<!-- --8<-- [start:exTemplateEngine] -->
```juvix
exTemplateEngine : TemplateEngine :=
  mkEngine@{
    cfg := exTemplateCfg;
    env := exTemplateEnv;
    behaviour := exTemplateBehaviour;
  };
```
<!-- --8<-- [end:exTemplateEngine] -->

Where `exTemplateCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/template_config.juvix.md:exTemplateCfg"

`exTemplateEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/template_environment.juvix.md:exTemplateEnv"

and `exTemplateBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/template_behaviour.juvix.md:exTemplateBehaviour"
