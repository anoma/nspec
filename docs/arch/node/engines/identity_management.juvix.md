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

    import arch.node.engines.identity_management_config open public;
    import arch.node.engines.identity_management_messages open public;
    import arch.node.engines.identity_management_environment open public;
    import arch.node.engines.identity_management_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open identity_management_config_example;
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
- [[Identity Management Configuration]]
- [[Identity Management Environment]]
- [[Identity Management Behaviour]]

## Type

<!-- --8<-- [start:IdentityManagementEngine] -->
```juvix
IdentityManagementEngine : Type :=
  Engine
    IdentityManagementCfg
    IdentityManagementLocalState
    IdentityManagementMailboxState
    IdentityManagementTimerHandle
    IdentityManagementActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:IdentityManagementEngine] -->

### Example of a identity management engine

<!-- --8<-- [start:exampleIdentityManagementEngine] -->
```juvix
exampleIdentityManagementEngine : IdentityManagementEngine :=
  mkEngine@{
    cfg := identityManagementCfg;
    env := identityManagementEnv;
    behaviour := identityManagementBehaviour;
  };
```
<!-- --8<-- [end:exampleIdentityManagementEngine] -->

where `identityManagementCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_config.juvix.md:identityManagementCfg"

`identityManagementEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_environment.juvix.md:identityManagementEnv"

and `identityManagementBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/identity_management_behaviour.juvix.md:identityManagementBehaviour"
