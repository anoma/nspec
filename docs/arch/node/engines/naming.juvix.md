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

## Purpose

The naming engine is responsible for tracking naming information. It supports name resolution, submitting name evidence, and querying name evidence. Ultimately, this means that the Naming Engine tracks which `Name`s correspond with which `ExternalIdentity`s using `IdentityNameEvidence`.

## Components

- [[Naming Messages]]
- [[Naming Environment]]
- [[Naming Behaviour]]

## Useful links

???

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
