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
    import arch.node.engines.template_environment open public;
    import arch.node.engines.template_behaviour open public;
    import arch.node.types.engine open public;
    open template_environment_example;
    ```

# Template Engine

## Purpose

Brief summary of the purpose of the engine.

## Components

- [[Template Messages]]
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
    TemplateMatchableArgument
    TemplateActionLabel
    TemplatePrecomputationList;
```
<!-- --8<-- [end:TemplateEngine] -->

### Example of a template engine

<!-- --8<-- [start:exampleTemplateEngine] -->
```juvix
exampleTemplateEngine : TemplateEngine := mkEngine@{
  initEnv := templateEnvironment;
  behaviour := templateBehaviour;
};
```
<!-- --8<-- [end:exampleTemplateEngine] -->

where `templateEnvironment` is defined as follows:

--8<-- "./docs/arch/node/engines/template_environment.juvix.md:templateEnvironment"

and `templateBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/template_behaviour.juvix.md:templateBehaviour"
