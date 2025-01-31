---
icon: octicons/project-template-24
search:
  exclude: false
tags:
  - node-architecture
  - identity-subsystem
  - engine
  - encryption
  - engine-definition
---

??? code "Juvix imports"

    ```juvix
    module arch.node.engines.encryption;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.encryption_messages open public;
    import arch.node.engines.encryption_environment open public;
    import arch.node.engines.encryption_behaviour open public;

    import arch.node.engines.encryption_config open public;
    import arch.node.engines.encryption_messages open public;
    import arch.node.engines.encryption_environment open public;
    import arch.node.engines.encryption_behaviour open public;

    import arch.node.types.anoma as Anoma open;

    open encryption_config_example;
    open encryption_environment_example;
    ```

# Encryption Engine

The Encryption engine is responsible for encrypting data to external identities,
possibly using known `reads_for` relationships. It automatically utilizes
"reads_for" relationship information from the [[ReadFor Engine]] along with caller
preference information to choose which identity to encrypt to.

## Purpose

The Encryption Engine encrypts data to external identities, optionally using
known `reads_for` relationships. It is a stateless function, and calls to it do
not need to be ordered. The runtime should implement this intelligently for
efficiency.

## Engine components

- [[Encryption Messages]]
- [[Encryption Configuration]]
- [[Encryption Environment]]
- [[Encryption Behaviour]]

## Type

<!-- --8<-- [start:EncryptionEngine] -->
```juvix
EncryptionEngine : Type :=
  Engine
    EncryptionCfg
    EncryptionLocalState
    EncryptionMailboxState
    EncryptionTimerHandle
    EncryptionActionArguments
    Anoma.Msg
    Anoma.Cfg
    Anoma.Env;
```
<!-- --8<-- [end:EncryptionEngine] -->

### Example of a encryption engine

<!-- --8<-- [start:exampleEncryptionEngine] -->
```juvix
exampleEncryptionEngine : EncryptionEngine :=
  mkEngine@{
    cfg := encryptionCfg;
    env := encryptionEnv;
    behaviour := encryptionBehaviour;
  };
```
<!-- --8<-- [end:exampleEncryptionEngine] -->

where `encryptionCfg` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_config.juvix.md:encryptionCfg"

`encryptionEnv` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_environment.juvix.md:encryptionEnv"

and `encryptionBehaviour` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_behaviour.juvix.md:encryptionBehaviour"
