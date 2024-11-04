---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- naming
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.naming_messages open public;
    import arch.node.engines.naming_environment open public;
    import arch.node.engines.naming_behaviour open public;
    open naming_environment_example;
    ```

# Naming Engine

???

## Purpose

???

## Components

- [[Naming Messages]]
- [[Naming Environment]]
- [[Naming Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:NamingEngine] -->
```juvix
NamingEngine : Type := Engine
  NamingLocalState
  NamingMailboxState
  NamingTimerHandle
  NamingMatchableArgument
  NamingActionLabel
  NamingPrecomputation;
```
<!-- --8<-- [end:NamingEngine] -->

### Example of a naming engine

```juvix extract-module-statements
exampleNamingEngine : NamingEngine := mkEngine@{
    name := "naming";
    behaviour := namingBehaviour;
    initEnv := namingEnvironmentExample;
  };
```

where `namingEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_environment.juvix.md:environment-example"
