---
icon: octicons/gear-16
search:
  exclude: false
categories:
- engine
tags:
- identity-management-engine
- engine-definition
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

The Identity Management Engine is responsible for generating, connecting, and deleting
identities using various backends. It provides a unified interface over different identity
backends, including internal identities stored in local memory, identities stored in
hardware devices, identities accessed via browser extensions, and identities stored on
remote machines accessible over the network.

## Purpose

The Identity Management Engine manages identities across various backends. When an identity
is generated or connected, it returns handles to the corresponding [[Commitment Engine]] and
[[Decryption Engine]] instances. These handles can be used to generate commitments or decrypt
data associated with the identity.

## Components

- [[Identity Management Messages]]
- [[Identity Management Environment]]
- [[Identity Management Behaviour]]

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

<!-- --8<-- [start:exampleIdentityManagementEngine] -->
```juvix
exampleIdentityManagementEngine : IdentityManagementEngine := mkEngine@{
    name := "identityManagement";
    initEnv := identityManagementEnvironment;
    behaviour := identityManagementBehaviour;
  };
```
<!-- --8<-- [end:exampleIdentityManagementEngine] -->

where `identityManagementEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_environment.juvix.md:identityManagementEnvironment"

and `identityManagementBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_behaviour.juvix.md:identityManagementBehaviour"