---
icon: octicons/gear-16
search:
  exclude: false
tags:
  - node-architecture
  - identity
  - engine
  - naming
  - engine-definition
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.naming;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.naming_config open public;
    import arch.node.engines.naming_messages open public;
    import arch.node.engines.naming_environment open public;
    import arch.node.engines.naming_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open naming_config_example;
    open naming_environment_example;
    ```

# Naming Engine

The Naming Engine is responsible for tracking naming information. It supports name
resolution, submitting name evidence, and querying name evidence.

## Purpose

The Naming Engine tracks which `IdentityName`s correspond with which `ExternalIdentity`s
using `IdentityNameEvidence`. It provides functionality for resolving names, submitting
name evidence, and querying name evidence.

## Engine components

- [[Naming Messages]]
- [[Naming Configuration]]
- [[Naming Environment]]
- [[Naming Behaviour]]

## Type

<!-- --8<-- [start:NamingEngine] -->
```juvix
NamingEngine : Type :=
  Engine
    NamingCfg
    NamingLocalState
    NamingMailboxState
    NamingTimerHandle
    NamingActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:NamingEngine] -->

### Example of a naming engine

<!-- --8<-- [start:exampleNamingEngine] -->
```juvix
exampleNamingEngine : NamingEngine :=
  mkEngine@{
    cfg := namingCfg;
    env := namingEnv;
    behaviour := namingBehaviour;
  };
```
<!-- --8<-- [start:exampleNamingEngine] -->

where `namingCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_config.juvix.md:namingCfg"

where `namingEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_environment.juvix.md:namingEnv"

and `namingBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/naming_behaviour.juvix.md:namingBehaviour"
