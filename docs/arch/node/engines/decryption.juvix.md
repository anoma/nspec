---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- decryption
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.decryption;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.decryption_messages open public;
    import arch.node.engines.decryption_environment open public;
    import arch.node.engines.decryption_behaviour open public;
    open decryption_environment_example;
    ```

# Decryption Engine

???

## Purpose

???

## Components

- [[Decryption Messages]]
- [[Decryption Environment]]
- [[Decryption Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:DecryptionEngine] -->
```juvix
DecryptionEngine : Type := Engine
  DecryptionLocalState
  DecryptionMailboxState
  DecryptionTimerHandle
  DecryptionMatchableArgument
  DecryptionActionLabel
  DecryptionPrecomputation;
```
<!-- --8<-- [end:DecryptionEngine] -->

### Example of a decryption engine

```juvix extract-module-statements
exampleDecryptionEngine : DecryptionEngine := mkEngine@{
    name := "decryption";
    behaviour := decryptionBehaviour;
    initEnv := decryptionEnvironmentExample;
  };
```

where `decryptionEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/decryption_environment.juvix.md:environment-example"
