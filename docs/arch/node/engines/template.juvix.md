---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
- node
tags:
- template-engine
- engine-definition
---

??? quote "Juvix preamble"

    ```juvix
    module arch.node.engines.template;

    import prelude open;
    import arch.node.engines.template_messages open public;
    import arch.node.engines.template_config open public;
    import arch.node.engines.template_environment open public;
    import arch.node.engines.template_behaviour open public;
    import arch.node.types.engine open public;

    open template_config_example;
    open template_environment_example;
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
    TemplateLocalState
    TemplateMailboxState
    TemplateTimerHandle
    TemplateActionArguments;
```
<!-- --8<-- [end:TemplateEngine] -->

### Example of a template engine

<!-- --8<-- [start:exampleTemplateEngine] -->
```juvix
exampleTemplateEngine : TemplateEngine :=
  mkEngine@{
    cfg := templateCfg;
    env := templateEnv;
    behaviour := templateBehaviour;
  };
```
<!-- --8<-- [end:exampleTemplateEngine] -->

where `templateCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/template_config.juvix.md:templateCfg"

`templateEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/template_environment.juvix.md:templateEnv"

and `templateBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/template_behaviour.juvix.md:templateBehaviour"
