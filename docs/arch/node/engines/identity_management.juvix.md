---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- identity_management
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.identity_management;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.identity_management_messages open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_behaviour open public;
    open identity_management_environment_example;
    ```

# IdentityManagement Engine

## Purpose

The identity management engine is responsible for generating, connecting, and deleting identities. It abstracts a uniform interface over identities created with different "backends", including, for example:

- internal identities stored in local memory

- internal identities stored in a hardware device, e.g. Ledger

- internal identities stored in a browser extension

- internal identities stored in another machine accessible over the network

When an identity is generated or connected, the identity management engine does not return the internal identity directly, but rather returns handles to the corresponding commitment and decryption engine instances, which can be used to generate commitments by and decrypt data encrypted to, respectively, the internal identity (which is still kept in whatever backend is in use).

## Components

- [[IdentityManagement Messages]]
- [[IdentityManagement Environment]]
- [[IdentityManagement Behaviour]]

## Useful links

???

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
