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

The Verification Engine is responsible for verifying commitments (signatures) made by external identities. It automatically uses "signs_for" relationship information from the Signs For Engine along with caller preference information to determine how to verify a commitment.

## Purpose

The Verification Engine verifies commitments (signatures) made by external identities. It can use "signs_for" relationship information and caller preferences to determine how to verify a commitment. This engine is designed to be stateless, allowing for efficient implementation by the runtime.

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

```juvix
exampleVerificationEngine : VerificationEngine := mkEngine@{
    name := "verification";
    behaviour := verificationBehaviour;
    initEnv := verificationEnvironmentExample;
  };
```

where `verificationEnvironmentExample` is defined as follows:

--8<-- "./verification_environment.juvix.md:environment-example"
