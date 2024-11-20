---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- encryption
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.encryption;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.encryption_messages open public;
    import arch.node.engines.encryption_environment open public;
    import arch.node.engines.encryption_behaviour open public;
    open encryption_environment_example;
    ```

# Encryption Engine

The `Encryption` engine is responsible for encrypting data to external identities,
possibly using known `reads_for` relationships. It automatically utilizes
"reads_for" relationship information from the Reads For Engine along with caller
preference information to choose which identity to encrypt to.

## Purpose

The `Encryption` Engine encrypts data to external identities, optionally using
known `reads_for` relationships. It is a stateless function, and calls to it do
not need to be ordered. The runtime should implement this intelligently for
efficiency.

## Components

- [[Encryption Messages]]
- [[Encryption Environment]]
- [[Encryption Behaviour]]

## Useful links

???

## Type

<!-- --8<-- [start:EncryptionEngine] -->
```juvix
EncryptionEngine : Type := Engine
  EncryptionLocalState
  EncryptionMailboxState
  EncryptionTimerHandle
  EncryptionMatchableArgument
  EncryptionActionLabel
  EncryptionPrecomputation;
```
<!-- --8<-- [end:EncryptionEngine] -->

### Example of a encryption engine

```juvix
exampleEncryptionEngine : EncryptionEngine := mkEngine@{
    behaviour := encryptionBehaviour;
    initEnv := encryptionEnvironmentExample;
  };
```

where `encryptionEnvironmentExample` is defined as follows:

--8<-- "./encryption_environment.juvix.md:environment-example"
