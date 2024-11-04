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

???

## Purpose

???

## Components

- [[Encryption Messages]]
- [[Encryption Environment]]
- [[Encryption Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

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

```juvix extract-module-statements
exampleEncryptionEngine : EncryptionEngine := mkEngine@{
    name := "encryption";
    behaviour := encryptionBehaviour;
    initEnv := encryptionEnvironmentExample;
  };
```

where `encryptionEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/encryption_environment.juvix.md:environment-example"
