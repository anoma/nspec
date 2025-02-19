---
icon: octicons/gear-24
search:
  exclude: false
tags:
  - tutorial
  - example
---

??? code "Juvix imports"

    ```juvix
    module tutorial.engines.template_minimum;

    import tutorial.engines.template_minimum_messages open public;
    import tutorial.engines.template_minimum_config open public;
    import tutorial.engines.template_minimum_environment open public;
    import tutorial.engines.template_minimum_behaviour open public;

    import arch.node.types.basics open;
    import arch.node.types.engine open;
    import arch.node.types.anoma as Anoma open;

    open template_minimum_config_example;
    open template_minimum_environment_example;
    open template_minimum_behaviour_example;
    ```

# Template Minimum Engine

## Purpose

Brief summary of the purpose of the engine.

## Subsystems

- [[Template Minimum Messages]]
- [[Template Minimum Configuration]]
- [[Template Minimum Environment]]
- [[Template Minimum Behaviour]]

## Useful links

- Some
- Useful
- Links

## Type

<!-- --8<-- [start:TemplateMinimumEngine] -->
```juvix
TemplateMinimumEngine : Type :=
  Engine
    TemplateMinimumLocalCfg
    TemplateMinimumLocalState
    TemplateMinimumMailboxState
    TemplateMinimumTimerHandle
    TemplateMinimumActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:TemplateMinimumEngine] -->

### Instantiation

<!-- --8<-- [start:exTemplateMinimumEngine] -->
```juvix
exTemplateMinimumEngine : TemplateMinimumEngine :=
  mkEngine@{
    cfg := exTemplateMinimumCfg;
    env := exTemplateMinimumEnv;
    behaviour := exTemplateMinimumBehaviour;
  };
```
<!-- --8<-- [end:exTemplateMinimumEngine] -->

Where `exTemplateMinimumCfg` is defined as follows:

--8<-- "./docs/tutorial/engines/template_minimum_config.juvix.md:exTemplateMinimumCfg"

`exTemplateMinimumEnv` is defined as follows:

--8<-- "./docs/tutorial/engines/template_minimum_environment.juvix.md:exTemplateMinimumEnv"

and `exTemplateMinimumBehaviour` is defined as follows:

--8<-- "./docs/tutorial/engines/template_minimum_behaviour.juvix.md:exTemplateMinimumBehaviour"
