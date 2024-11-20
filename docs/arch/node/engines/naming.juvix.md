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

The Naming Engine is responsible for tracking naming information as described in *Identity Names*. It supports name resolution, submitting name evidence, and querying name evidence.

## Purpose

The Naming Engine tracks which `IdentityName`s correspond with which `ExternalIdentity`s using `IdentityNameEvidence`. It provides functionality for resolving names, submitting name evidence, and querying name evidence.

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

```juvix
exampleNamingEngine : NamingEngine := mkEngine@{
    behaviour := namingBehaviour;
    initEnv := namingEnvironmentExample;
  };
```

where `namingEnvironmentExample` is defined as follows:

--8<-- "./naming_environment.juvix.md:environment-example"
