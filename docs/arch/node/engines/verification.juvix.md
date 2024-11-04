---
icon: octicons/project-template-24
search:
  exclude: false
tags:
- verification
- engines
---

??? quote "Juvix imports"

    ```juvix
    module arch.node.engines.verification;

    import prelude open;
    import arch.node.types.engine open;

    import arch.node.engines.verification_messages open public;
    import arch.node.engines.verification_environment open public;
    import arch.node.engines.verification_behaviour open public;
    open verification_environment_example;
    ```

# Verification Engine

???

## Purpose

???

## Components

- [[Verification Messages]]
- [[Verification Environment]]
- [[Verification Behaviour]]

## Useful links

- [Composable Semantic Models for Actor Theories](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=18475015c7c46d38292833ddda32dc88b5655160)

## Type

<!-- --8<-- [start:VerificationEngine] -->
```juvix
VerificationEngine : Type := Engine
  VerificationLocalState
  VerificationMailboxState
  VerificationTimerHandle
  VerificationMatchableArgument
  VerificationActionLabel
  VerificationPrecomputation;
```
<!-- --8<-- [end:VerificationEngine] -->

### Example of a verification engine

```juvix extract-module-statements
exampleVerificationEngine : VerificationEngine := mkEngine@{
    name := "verification";
    behaviour := verificationBehaviour;
    initEnv := verificationEnvironmentExample;
  };
```

where `verificationEnvironmentExample` is defined as follows:

--8<-- "./docs/arch/node/engines/verification_environment.juvix.md:environment-example"
