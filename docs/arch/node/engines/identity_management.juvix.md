---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- identityManagement
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.identityManagement;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.identity_management_messages open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_behaviour open public;
    open identity_management_environment_example;
    ```

# IdentityManagement Engine

???

## Purpose

???

## Components

- [[IdentityManagement Messages]]
- [[IdentityManagement Environment]]
- [[IdentityManagement Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:IdentityManagementEngine] -->
```juvix
IdentityManagementEngine : Type := Engine
  IdentityManagementLocalState
  IdentityManagementMailboxState
  IdentityManagementTimerHandle
  IdentityManagementMatchableArgument
  IdentityManagementActionLabel
  IdentityManagementPrecomputation;
```
<!-- --8<-- [end:IdentityManagementEngine] -->

### Example of a identityManagement engine

```juvix extract-module-statements
exampleIdentityManagementEngine : IdentityManagementEngine := mkEngine@{
    name := "identityManagement";
    behaviour := identityManagementBehaviour;
    initEnv := identityManagementEnvironmentExample;
  };
```

where `identityManagementEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/identityManagement_environment.juvix.md:environment-example"
