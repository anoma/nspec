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

## Purpose

The verification engine is responsible for verifying commitments made by external identities. It automatically uses "signs for" relationship information from the [[Signs For Engine]] along with caller preference information in order to choose how to verify a commitment.

## Components

- [[Verification Messages]]
- [[Verification Environment]]
- [[Verification Behaviour]]

## Useful links

???

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
